from abc import ABC, abstractmethod
from typing import Union


class AbstractCommunicator(ABC):
    """
    Abstract base class for communication protocols.
    """

    @abstractmethod
    def _connect(self):
        """
        Abstract method to establish a connection.
        """
        pass

    @abstractmethod
    def send(self, command: str) -> None:
        """
        Abstract method to send a command.

        Args:
            command (str): Command to be sent.
        """
        pass

    @abstractmethod
    def receive(self, timeout: int = 10) -> Union[str, list[str]]:
        """
        Abstract method to receive a response.

        Args:
            timeout (int, optional): Time in seconds to wait for a response. Defaults to 10.

        Returns:
            str: The received response.
        """
        pass

    @abstractmethod
    def send_and_receive(self, command: str) -> Union[str, list[str]]:
        """
        Send a command and immediately attempt to receive a response.

        Args:
            command (str): Command to be sent.

        Returns:
            List[str]: List of response lines.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Abstract method to close the connection.
        """
        pass
