import os

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


# If you want to run the tests manually without a test runner you can do so with the following:
# if __name__ == "__main__":
#     asyncio.run(test_open_and_close_connection())
#     asyncio.run(test_send_command_and_receive_response())
