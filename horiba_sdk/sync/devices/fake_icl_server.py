import importlib.resources
import json
from pathlib import Path
from typing import Optional

from loguru import logger
from websockets.sync.server import WebSocketServer, serve


class FakeICLServer:
    """The FakeICLServer is a synchronous fake ICL server that sends only dummy data.

    It starts a local websocket server and returns the predefined response located in
    `horiba_sdk/devices/fake_responses/*.json`.
    Currently supported devices for fake responses are:
    - The ICL itself
    - The :class:`Monochromator`
    - The :class:`ChargeCoupledDevice`

    For other unsupported devices, it just responds with the sent command.

    """

    def __init__(self, fake_icl_host: str = 'localhost', fake_icl_port: int = 8765):
        self._fake_icl_host: str = fake_icl_host
        self._fake_icl_port: int = fake_icl_port
        self._server: Optional[WebSocketServer] = None

        fake_responses_path: Path = Path(str(importlib.resources.files('horiba_sdk.devices'))) / Path('fake_responses')

        icl_fake_responses_path = fake_responses_path / 'icl.json'
        with open(icl_fake_responses_path) as json_file:
            self.icl_responses = json.load(json_file)

        monochromator_fake_responses_path = fake_responses_path / 'monochromator.json'
        with open(monochromator_fake_responses_path) as json_file:
            self.monochromator_responses = json.load(json_file)

        ccd_fake_responses_path = fake_responses_path / 'ccd.json'
        with open(ccd_fake_responses_path) as json_file:
            self.ccd_responses = json.load(json_file)

    def echo(self, websocket):
        for message in websocket:
            logger.info('received: {message}', message=message)
            command = json.loads(message)
            if 'command' not in command:
                logger.info('unknown message format, responding with message')
                websocket.send(message)
                continue
            if command['command'].startswith('icl_'):
                response = json.dumps(self.icl_responses[command['command']])
                websocket.send(response)
            elif command['command'].startswith('mono_'):
                response = json.dumps(self.monochromator_responses[command['command']])
                websocket.send(response)
            elif command['command'].startswith('ccd_'):
                response = json.dumps(self.ccd_responses[command['command']])
                websocket.send(response)
            else:
                logger.info('unknown command, responding with message')
                websocket.send(message)

    def start(self):
        self._server = serve(self.echo, host=self._fake_icl_host, port=self._fake_icl_port)
        self._server.serve_forever()

    def stop(self):
        if self._server:
            self._server.shutdown()
