import time
from queue import Queue
from threading import Thread
from types import TracebackType
from typing import Any, Callable, Optional, final

import websockets
from loguru import logger
from overrides import override
from websockets.sync.client import ClientConnection

from horiba_sdk.communication.communication_exception import CommunicationException
from horiba_sdk.communication.messages import Command, JSONResponse, Response
from horiba_sdk.sync.communication.abstract_communicator import AbstractCommunicator


@final
class WebsocketCommunicator(AbstractCommunicator):
    """
    The WebsocketCommunicator implements the `horiba_sdk.sync.communication.AbstractCommunicator` via websockets.
    A background thread listens continuously for incoming binary data.
    """

    def __init__(self, uri: str = 'ws://127.0.0.1:25010') -> None:
        self.uri: str = uri
        self.websocket: Optional[ClientConnection] = None
        self.running_listen_thread: bool = False
        self.listen_thread: Optional[Thread] = None
        self.running_binary_message_handling_thread: bool = False
        self.binary_message_handling_thread: Optional[Thread] = None
        self.json_message_queue: Queue[str] = Queue()
        self.binary_message_queue: Queue[bytes] = Queue()
        self.binary_message_callback: Optional[Callable[[bytes], Any]] = None
        self.icl_info: dict[str, Any] = {}

    def __enter__(self) -> 'WebsocketCommunicator':
        self.open()
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    @override
    def open(self) -> None:
        """
        Opens the WebSocket connection and starts listening for binary data.

        Raises:
            CommunicationException: When the websocket is already opened or
            there is an issue with the underlying websockets connection attempt.
        """
        if self.opened():
            raise CommunicationException(None, 'websocket already opened')

        try:
            self.websocket = websockets.sync.client.connect(self.uri)
        except websockets.WebSocketException as e:
            raise CommunicationException(None, 'websocket connection issue') from e

        self.running_listen_thread = True
        self.listen_thread = Thread(target=self._receive_data)
        self.listen_thread.start()

        logger.debug(f'Websocket connection established to {self.uri}')

    def send(self, command: Command) -> None:
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
            self.websocket.send(command.json())  # type: ignore
        except websockets.exceptions.ConnectionClosed as e:
            raise CommunicationException(None, 'Trying to send data while websocket is closed') from e

    @override
    def opened(self) -> bool:
        """
        Returns if the websocket connection is open or not

        Returns:
            bool: True if the websocket connection is open, False otherwise
        """
        return self.websocket is not None

    def response(self) -> Response:
        """Fetches the next response

        Returns:
            Response: The response from the server

        Raises:
            CommunicationException: When the connection terminated with an error
        """
        if not self.json_message_queue or self.json_message_queue.empty():
            raise CommunicationException(None, 'No message to be received.')

        logger.debug(f'#{self.json_message_queue.qsize()} messages in the queue, taking first')
        response: str = self.json_message_queue.get()
        logger.debug('retrieved message in queue')
        return JSONResponse(response)

    @override
    def close(self) -> None:
        """
        Closes the WebSocket connection.

        Raises:
            CommunicationException: When the websocket is already closed
        """
        if not self.opened():
            raise CommunicationException(None, 'cannot close already closed websocket')
        if self.websocket:
            logger.debug('Waiting websocket close...')
            self.websocket.close()

        if self.binary_message_handling_thread:
            logger.debug('Canceling binary listening thread...')
            self.running_binary_message_handling_thread = False
            self.binary_message_handling_thread.join()
            self.binary_message_handling_thread = None

        if self.listen_thread:
            logger.debug('Canceling listening thread...')
            self.running_listen_thread = False
            self.listen_thread.join()
            self.listen_thread = None

        self.websocket = None
        logger.debug('Websocket connection closed')

    def register_binary_message_callback(self, callback: Callable[[bytes], Any]) -> None:
        """Registers a callback to be called with every incoming binary message."""
        if self.binary_message_callback:
            raise CommunicationException(None, 'Binary message callback already registered')

        self.binary_message_callback = callback
        logger.info('Binary message callback registered.')
        self.running_binary_message_handling_thread = True
        self.binary_message_handling_thread = Thread(target=self._run_binary_message_callback)
        self.binary_message_handling_thread.start()
        logger.info('Started binary message thread')

    def _receive_data(self) -> None:
        if not self.websocket:
            raise CommunicationException(None, 'Websocket is not open')

        while self.running_listen_thread:
            try:
                for message in self.websocket:
                    logger.debug(f'Received message: {message!r}')
                    if isinstance(message, str):
                        self.json_message_queue.put(message)
                    elif isinstance(message, bytes) and self.binary_message_callback:
                        self.binary_message_queue.put(message)
                    else:
                        raise CommunicationException(None, f'Unknown type of message {type(message)}')
            except websockets.ConnectionClosedOK:
                logger.debug('websocket connection terminated properly')
            except websockets.ConnectionClosedError as e:
                raise CommunicationException(None, 'connection terminated with error') from e
            except Exception as e:
                raise CommunicationException(None, 'failure to process binary data') from e

    def _run_binary_message_callback(self) -> None:
        if not self.binary_message_callback:
            raise CommunicationException(None, 'No binary message callback registered')

        while self.running_binary_message_handling_thread:
            while self.binary_message_queue.empty():
                time.sleep(0.5)
                if not self.running_binary_message_handling_thread:
                    return

            binary_message = self.binary_message_queue.get()
            self.binary_message_callback(binary_message)

    @override
    def request_with_response(self, command: Command, time_to_wait_for_response_in_s: float = 0.1) -> Response:
        """
        Concrete method to fetch a response from a command.

        Args:
            command (Command): Command for which a response is desired
            time_to_wait_for_response_in_s (float, optional): Time, in seconds, to wait between request and response.
            Defaults to 0.1s

        Returns:
            Response: The response corresponding to the sent command.
        """
        self.send(command)
        logger.debug('sent command, waiting for response')
        time.sleep(time_to_wait_for_response_in_s)
        response: Response = self.response()

        return response
