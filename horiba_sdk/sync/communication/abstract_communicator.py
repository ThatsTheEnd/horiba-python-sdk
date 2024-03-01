from abc import ABC, abstractmethod

from horiba_sdk.communication.messages import Command, Response


class AbstractCommunicator(ABC):
    """
    Abstract base class for communication protocols.
    """

    @abstractmethod
    def open(self) -> None:
        """
        Abstract method to establish a connection.
        """
        pass

    @abstractmethod
    def opened(self) -> bool:
        """
        Abstract method that says if the connection is open

        Returns:
            bool: True if the connection is open, False otherwise
        """
        pass

    @abstractmethod
    def request_with_response(self, command: Command) -> Response:
        """
        Abstract method to fetch a response from a command.

        Args:
            command (Command): Command for which a response is desired

        Returns:
            Response: The response corresponding to the sent command.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Abstract method to close the connection.
        """
        pass
