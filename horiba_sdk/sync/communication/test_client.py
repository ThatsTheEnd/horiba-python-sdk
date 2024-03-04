# Closing frame is apparently not sent. Here is a minimal example to prove the point:
# 1. First run icl.exe
# 2. Then execute this script:
#    poetry run python ./horiba_sdk/sync/communication/test_client.py
import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

websocket = websockets.sync.client.connect(uri='ws://localhost:25010')
try:
    websocket.send('{"command":"icl_shutdown"}')
    for message in websocket:
        print(message)
except ConnectionClosedOK as e:
    print(f'Connection normally closed: {e}')
except ConnectionClosedError as e:
    print(f'Protocol error or network failure: {e}')
