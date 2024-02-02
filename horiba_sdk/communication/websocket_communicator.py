import asyncio
import contextlib
from types import TracebackType
from typing import Any, Optional, final, Callable

import websockets
from loguru import logger
from overrides import override
from websockets.legacy.client import WebSocketClientProtocol

from .abstract_communicator import AbstractCommunicator
from .communication_exception import CommunicationException
from .messages import BinaryResponse, Command, JSONResponse, Response


@final
class WebsocketCommunicator(AbstractCommunicator):
    """
    The WebsocketCommunicator implements the `horiba_sdk.communication.AbstractCommunicator` via websockets.
    A background task listens continuoulsy for incoming binary data.

    It supports Asynchronous Context Managers and can be used like the following::

        websocket_communicator: WebsocketCommunicator = WebsocketCommunicator(uri)
        async with websocket_communicator:
            assert websocket_communicator.opened()

            request: str = '{"command": "some_command"}'
            await websocket_communicator.send(request)
            response = await websocket_communicator.response()
            # do something with the response...

    """

    def __init__(self, uri: str = 'ws://127.0.0.1:25010') -> None:
        self.uri: str = uri
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.listen_task: Optional[asyncio.Task[Any]] = None
        self.json_message_queue: asyncio.Queue[str] = asyncio.Queue()
        self.binary_message_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self.binary_message_callback: Optional[Callable[[bytes], Any]] = None

    async def __aenter__(self) -> 'WebsocketCommunicator':
        await self.open()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException], exc_value: BaseException, traceback: Optional[TracebackType]
    ) -> None:
        await self.close()

    @override
    async def open(self) -> None:
        """
        Opens the WebSocket connection and starts listening for binary data.

        Raises:
            CommunicationException: When the websocket is already opened or
            there is an issue with the underlying websockets connection attempt.
        """
        if self.opened():
            raise CommunicationException(None, 'websocket already opened')

        try:
            self.websocket = await websockets.connect(self.uri)
        except websockets.WebSocketException as e:
            raise CommunicationException(None, 'websocket connection issue') from e

        logger.debug(f'Websocket connection established to {self.uri}')
        self.listen_task = asyncio.create_task(self._receive_binary_data())

    @override
    async def send(self, command: Command) -> None:
        """
        Sends a command to the WebSocket server.

        Args:
            command (Command): The command to send to the server.

        Raises:
            CommunicationException: When trying to send a command while the websocket is closed.

        """
        if not self.opened():
            raise CommunicationException(None, 'WebSocket is not opened.')

        try:
            # mypy cannot infer the check from self.opened() done above
            logger.debug(f'Sending JSON command: {command.json()}')
            await self.websocket.send(command.json())  # type: ignore
        except websockets.exceptions.ConnectionClosed as e:
            raise CommunicationException(None, 'Trying to send data while websocket is closed') from e

    @override
    def opened(self) -> bool:
        """
        Returns if the websocket connection is open or not

        Returns:
            bool: True if the websocket connection is open, False otherwise
        """
        return self.websocket is not None and self.websocket.open

    @override
    async def response(self) -> Response:
        """Fetches the next response

        Returns:
            Response: The response from the server

        Raises:
            CommunicationException: When the connection terminated with an error
        """
        try:
            response: str = await self.json_message_queue.get()
            return JSONResponse(response)
        except asyncio.CancelledError as e:
            raise CommunicationException(None, 'Response reception was canceled') from e

    @override
    async def binary_response(self) -> BinaryResponse:
        """Fetches the next binary response.

        Returns:
            BinaryResponse: The binary response from the server

        Raises:
            CommunicationException: When the connection terminated with an error
            or the binary data failed to be processed.
        """
        try:
            response: bytes = await self.binary_message_queue.get()
            logger.debug(f'Received binary response: {response!r}')
            return BinaryResponse(response)
        except asyncio.CancelledError as e:
            raise CommunicationException(None, 'Response reception was canceled') from e

    @override
    async def close(self) -> None:
        """
        Closes the WebSocket connection.

        Raises:
            CommunicationException: When the websocket is already closed
        """
        if not self.opened():
            raise CommunicationException(None, 'cannot close already closed websocket')
        if self.websocket:
            logger.debug('Waiting websocket close...')
            await self.websocket.close()
            self.websocket = None
        if self.listen_task:
            logger.debug('Canceling listening task...')
            self.listen_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                logger.debug('Await listening task...')
                await self.listen_task

        logger.debug('Websocket connection closed')

    def register_binary_message_callback(self, callback: Callable[[bytes], Any]) -> None:
        """Registers a callback to be called with every incoming binary message."""
        logger.info("Binary message callback registered.")
        self.binary_message_callback = callback

    async def _receive_data(self) -> None:
        try:
            while True:
                message = await self.websocket.recv()  # type: ignore
                logger.info(f'Received message: {message}')
                if isinstance(message, str):
                    await self.json_message_queue.put(message)
                elif isinstance(message, bytes):
                    await self.binary_message_queue.put(message)
                    logger.debug(f"Callback before if statement: {self.binary_message_callback}")
                    if self.binary_message_callback:
                        await asyncio.create_task(self.binary_message_callback(message))  # Call the callback
                else:
                    raise CommunicationException(None, f'Unknown type of message {type(message)}')
        except websockets.ConnectionClosedOK:
            logger.debug('websocket connection terminated properly')
        except websockets.ConnectionClosedError as e:
            raise CommunicationException(None, 'connection terminated with error') from e
        except Exception as e:
            raise CommunicationException(None, 'failure to process binary data') from e

    async def _receive_binary_data(self) -> None:
        await self._receive_data()

    async def execute_command(self, command_name: str, parameters: dict) -> Response:
        """
        Creates a command from the command name, and it's parameters
        Executes a command and handles the response.

        Args:
            command_name (str): The name of the command to execute.
            parameters (dict): The parameters for the command.

        Returns:
            Response: The response from the device.

        Raises:
            Exception: When an error occurred on the device side.
        """
        command: Command = Command(command_name, parameters)  # create command
        await self.send(command)  # send command
        response: Response = await self.response()  # get response
        return response
