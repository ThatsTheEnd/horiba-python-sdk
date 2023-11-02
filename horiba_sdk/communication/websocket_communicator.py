from typing import Union

from .abstract_communicator import AbstractCommunicator


class WebsocketCommunicator(AbstractCommunicator):
    def __init__(self, websocket_ip: str = '127.0.0.1', websocket_port: str = '25010') -> None:
        print(websocket_ip, websocket_port)  # dummy code to make linter pass

    def _connect(self):
        pass

    def send(self, command: str) -> None:
        pass

    def receive(self, timeout: int = 10) -> Union[str, list[str]]:
        pass

    def send_and_receive(self, command: str) -> Union[str, list[str]]:
        pass

    def close(self) -> None:
        pass
