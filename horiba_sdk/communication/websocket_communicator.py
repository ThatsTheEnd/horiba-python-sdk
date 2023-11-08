import asyncio
import contextlib
from typing import Optional

import websockets
from websockets.legacy.client import WebSocketClientProtocol


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
        self.listen_task: Optional[asyncio.Task] = None

    async def open(self) -> None:
        """
        Opens the WebSocket connection and starts listening for binary data.
        """
        self.websocket = await websockets.connect(self.uri)
        self.listen_task = asyncio.create_task(self._receive_binary_data())

    async def send_command(self, command: str) -> str:
        """
        Sends a command to the WebSocket server and waits for the response.

        Args:
            command (str): The command to send to the server.

        Returns:
            The response from the server as a string.
        """
        assert self.websocket, 'WebSocket is not connected.'
        await self.websocket.send(command)
        return await self.websocket.recv()

    async def _receive_binary_data(self) -> None:
        """
        Asynchronously listens for binary data from the WebSocket server.
        """
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

    def _process_binary_data(self, data: bytes) -> None:
        """
        Processes the received binary data.

        Args:
            data (bytes): The binary data received from the WebSocket server.
        """
        print('Received binary data:', data)

    async def close(self) -> None:
        """
        Closes the WebSocket connection.
        """
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
        if self.listen_task:
            self.listen_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.listen_task


# Usage example
# async def main() -> None:
#     client = WebSocketClient("ws://example.com")
#     await client.open()
#     try:
#         # Send a command and get the response
#         response = await client.send_command("your_command")
#         print("Response from server:", response)
#
#         # The client will continue to listen for binary data in the background.
#         # You can perform other tasks here, or sleep to keep the program running.
#         await asyncio.sleep(10)
#     finally:
#         # Ensure the connection is properly closed when done.
#         await client.close()
#
# # Run the event loop until the main coroutine completes.
# asyncio.run(main())
