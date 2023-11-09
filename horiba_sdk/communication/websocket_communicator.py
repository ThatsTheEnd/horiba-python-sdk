import asyncio
import contextlib
from typing import Any, Optional, Union

import websockets
from websockets.legacy.client import WebSocketClientProtocol
from websockets.protocol import Close


class WebsocketCommunicator:
    """
    A WebSocket client that can send commands and asynchronously listen for binary data.

    Attributes:
        uri (str): The URI of the WebSocket server to connect to.
        websocket (Optional[WebSocketClientProtocol]): The WebSocket connection object.
    """

    def __init__(self, uri: str = 'ws://127.0.0.1:25010') -> None:
        """
        Initializes the WebSocketClient with the server URI.

        Args:
            uri (str): The URI of the WebSocket server to connect to.
        """
        self.uri: str = uri
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.listen_task: Optional[asyncio.Task[Any]] = None

    async def open(self) -> None:
        """
        Opens the WebSocket connection and starts listening for binary data.
        """
        self.websocket = await websockets.connect(self.uri)
        self.listen_task = asyncio.create_task(self._receive_binary_data())

    async def send_command(self, command: str) -> Union[str, bytes]:
        """
        Sends a command to the WebSocket server and waits for a response.

        Args:
            command (str): The command to be sent to the WebSocket server.

        Returns:
            str: The response received from the WebSocket server.

        Raises:
            AssertionError: If the WebSocket is not connected.
        """
        assert self.websocket, 'WebSocket is not connected.'
        await self.websocket.send(command)
        return await self.websocket.recv()

    async def _receive_binary_data(self) -> None:
        """
        Continuously listens for binary data from the WebSocket server until the connection is closed
        or an error occurs.
        Only processes messages that are instances of bytes.
        """
        if self.websocket is not None:
            try:
                while True:
                    message = await self.websocket.recv()
                    if isinstance(message, bytes):
                        # Handle binary message
                        self._process_binary_data(message)
            except websockets.ConnectionClosedOK:
                # Connection has been closed, exit the listener
                return
            except Exception as e:
                # Handle other exceptions that could occur
                print(f'Error receiving data: {e}')
        else:
            print('WebSocket is not connected.')
            raise websockets.exceptions.ConnectionClosedError(Close(1006, 'WebSocket is not connected.'), None)

    def _process_binary_data(self, data: bytes) -> None:
        """
        Prints the received binary data.

        Args:
            data (bytes): The binary data received from the WebSocket server.
        """
        print('Received binary data:', data)

    async def close(self) -> None:
        """
        Closes the WebSocket connection if it is open.
        """
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
        if self.listen_task:
            self.listen_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.listen_task
