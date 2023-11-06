import asyncio
import contextlib
import logging
from types import TracebackType
from typing import Any, Optional, Union, final

import websockets
from websockets.legacy.client import WebSocketClientProtocol

from .abstract_communicator import AbstractCommunicator
from .communication_exception import CommunicationException


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
        self.message_queue: asyncio.Queue[Union[str, bytes]] = asyncio.Queue()

    async def __aenter__(self) -> None:
        return await self.open()

    async def __aexit__(
        self, exc_type: type[BaseException], exc_value: BaseException, traceback: Optional[TracebackType]
    ) -> None:
        await self.close()

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

        self.listen_task = asyncio.create_task(self._receive_binary_data())

    async def send(self, command: str) -> None:
        """
        Sends a command to the WebSocket server.

        Args:
            command (str): The command to send to the server.

        Raises:
            CommunicationException: When trying to send an unsupported data type
            or when trying to send a command while the websocket is closed.

        """
        if not self.opened():
            raise CommunicationException(None, 'WebSocket is not opened.')

        try:
            # mypy cannot infer the check from self.opened() done above
            await self.websocket.send(command)  # type: ignore
        except TypeError as e:
            raise CommunicationException(None, 'Trying to send unsupported type' + str(type(command))) from e
        except websockets.exceptions.ConnectionClosed as e:
            raise CommunicationException(None, 'Trying to send data while websocket is closed') from e

    def opened(self) -> bool:
        """
        Returns if the websocket connection is open or not

        Returns:
            bool: True if the websocket connection is open, False otherwise
        """
        return self.websocket is not None and self.websocket.open

    async def response(self) -> Union[str, bytes]:
        """
        Fetches the next response

        Returns:
            str: String or bytes containing the response

        Raises:
            CommunicationException: When the connection terminated with an error
            or the binary data failed to be processed.
        """
        try:
            return await self.message_queue.get()
        except asyncio.CancelledError as e:
            raise CommunicationException(None, 'Response reception was canceled') from e

    async def send_and_receive(self, command: str) -> Union[str, bytes]:
        """
        Sends a command to the WebSocket server and waits for the response.

        Args:
            command (str): The command to send to the server.

        Returns:
            Union[str, bytes]: The response from the server as a string or bytes.

        Raises:
            CommunicationException: See `send` and `response` functions above.
        """
        await self.send(command)
        return await self.response()

    async def close(self) -> None:
        """
        Closes the WebSocket connection.

        Raises:
            CommunicationException: When the websocket is already closed
        """
        if not self.opened():
            raise CommunicationException(None, 'cannot close already closed websocket')
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
        if self.listen_task:
            self.listen_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.listen_task

    async def _receive_data(self) -> None:
        try:
            while True:
                message = await self.websocket.recv()  # type: ignore
                await self.message_queue.put(message)
        except websockets.ConnectionClosedOK:
            logging.debug('websocket connection terminated properly')
        except websockets.ConnectionClosedError as e:
            raise CommunicationException(None, 'connection terminated with error') from e
        except Exception as e:
            raise CommunicationException(None, 'failure to process binary data') from e

    async def _receive_binary_data(self) -> None:
        await self._receive_data()
