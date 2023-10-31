# pylint: skip-file

import telnetlib
from typing import Union, List

from horiba_sdk.communication import AbstractCommunicator


class MockedTelnetCommunicator(AbstractCommunicator):
    """Mocked class to simulate communication"""

    def __init__(self, host: str="localhost", port: int=25000) -> None:
        self.command = ""

    def _connect(self) -> Union[None, telnetlib.Telnet]:
        pass

    def send(self, command: str) -> None:
        self.command = command

    def receive(self, timeout: int=10) -> Union[str, List[str]]:
        # Just for this example, we'll simulate responses based on specific commands
        if self.command == "bla":
            return ["\r", "Error: Unknown command\r", "-501\r", "cmd: "]
        elif self.command == "help":
            return [
                "\r",
                "\r",
                "Remote Command Interface Commands:\r",
                " Node Commands\r",
                "    exit                        - Disconnect\r",
            ]
        else:
            return ["cmd: "]  # Default response

    def send_and_receive(self, command: str) -> Union[str, List[str]]:
        self.send(command)
        return self.receive()  # Simulate by directly returning a response

    def close(self) -> None:
        pass  # This won't actually close any connection since it's mocked
