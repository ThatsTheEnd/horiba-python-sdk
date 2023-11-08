import os
from unittest.mock import AsyncMock, patch

import pytest

from horiba_sdk.communication import WebsocketCommunicator  # Replace with the actual import for your client.


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_open_and_close_connection():
    """
    Test that opens the WebSocket connection to a server and then closes it.
    """
    client = WebsocketCommunicator('ws://127.0.0.1:25010')
    await client.open()  # Assumes the WebSocket server is running on localhost:25010
    assert client.websocket is not None  # Check if the connection is established
    assert client.websocket.open  # Check if the connection is in open state
    await client.close()
    assert client.websocket is None  # After closing, the websocket should be None


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_send_command_and_receive_response():
    """
    Test that opens a WebSocket connection, sends a JSON string command,
    receives a response that starts with a specific string, and then closes the connection.
    """
    client = WebsocketCommunicator('ws://127.0.0.1:25010')
    await client.open()
    command = '{"id": 155, "command": "icl_info", "parameters": {}}'
    response = await client.send_command(command)
    expected_start = '{"command":"icl_info","errors":[],"id":155,"results":{"built":'
    assert response.startswith(expected_start)
    await client.close()


@pytest.mark.asyncio
async def test_open_and_close_connection_mocked():
    with patch('websockets.connect', new_callable=AsyncMock) as mock_ws:
        communicator = WebsocketCommunicator()
        await communicator.open()
        mock_ws.assert_called_once_with('ws://127.0.0.1:25010')
        await communicator.close()


@pytest.mark.asyncio
async def test_send_command_and_receive_response_mocked():
    expected_start = '{"command":"icl_info","errors":[],"id":155,"results":{"built":'
    expected_response = '{"command":"icl_info","errors":[],"id":155,"results":{"built": '

    with patch('websockets.connect', new_callable=AsyncMock) as mock_ws:
        # Mock the websocket to receive a response
        mock_ws.return_value.recv = AsyncMock(return_value=expected_response)

        # Ensure send is also an AsyncMock, even though we do not check its behavior in this test
        mock_ws.return_value.send = AsyncMock()

        communicator = WebsocketCommunicator()
        await communicator.open()

        # Send the command and receive a response
        response = await communicator.send_command('{"id": 155, "command": "icl_info", "parameters": {}}')

        # Assert that the send method was called with the right parameters
        mock_ws.return_value.send.assert_awaited_once_with('{"id": 155, "command": "icl_info", "parameters": {}}')

        # Validate the response starts with the expected text
        assert response.startswith(expected_start), 'Response did not start with expected text'

        await communicator.close()


# If you want to run the tests manually without a test runner you can do so with the following:
# if __name__ == "__main__":
#     asyncio.run(test_open_and_close_connection())
#     asyncio.run(test_send_command_and_receive_response())
