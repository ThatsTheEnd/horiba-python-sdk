from websocket_communicator import WebsocketCommunicator

from horiba_sdk.communication.messages import Command

command = Command('hello_world', parameters={})

websocket = WebsocketCommunicator(uri='ws://localhost:8765')
websocket.open()
response = websocket.request_with_response(command)
print(response)
print(response.command)
websocket.close()
