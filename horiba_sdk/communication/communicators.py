import telnetlib
from typing import List, Optional

# from .error_codes import RCIError as Error
from .abstracts import AbstractCommunicator


class TelnetCommunicator(AbstractCommunicator):
    """
    Handles Telnet communications. This class uses the metaclass=SingletonMeta to ensure there is only one instance
    of the TelnetCommunicator class.
    """

    host: str
    port: int
    _connection: Optional[telnetlib.Telnet]

    def __init__(self, host: str = 'localhost', port: int = 25000) -> None:
        """
        Initialize a Telnet communicator.

        Args:
            host (str): Host address.
            port (int, optional): Port number. Defaults to 25000.
        """
        self.host = host
        self.port = port
        self._connection = None
        self._connection = self._connect()

    def _connect(self) -> Optional[telnetlib.Telnet]:
        """
        Establish a Telnet connection.

        Returns:
            telnetlib.Telnet: Telnet connection or None if an error occurred.
        """
        try:
            self._connection = telnetlib.Telnet(self.host, self.port)
            self._connection.read_until(b"cmd: ", 10)
            self._connection.write(b"\r\n")
            self._connection.read_until(b"cmd: ", 10)
            return self._connection
        except ConnectionRefusedError as e:
            raise ConnectionError(f"Error connecting to {self.host}: {e}") from e

    def send(self, command: str) -> None:
        """
        Send a Telnet command.

        Args:
            command (str): Command to be sent.
        """
        if self._connection is not None:
            self._connection.write(command.encode("ascii") + b"\r\n")
        else:
            raise ValueError("Connection is not established.")

    def receive(self, timeout: int = 10) -> List[str]:
        """
        Receive a response from the Telnet connection.

        Args:
            timeout (int, optional): Time in seconds to wait for a response. Defaults to 10.

        Returns:
            List[str]: List of response lines.
        """
        if self._connection is None:
            raise ConnectionError("No active connection")

        try:
            response = self._connection.read_until(b"cmd: ", timeout)
            return response.decode("ascii").split("\n")

        except ConnectionRefusedError as e:
            raise ConnectionError(f"Error connecting to {self.host}: {e}") from e

    def send_and_receive(self, command: str) -> list[str]:
        """
        Send a command and immediately attempt to receive a response.

        Args:
            command (str): Command to be sent.

        Returns:
            List[str]: List of response lines.
        """
        self.send(command)
        return self.receive()

    def close(self) -> None:
        """
        Close the Telnet connection.
        """
        if self._connection:
            self._connection.close()
