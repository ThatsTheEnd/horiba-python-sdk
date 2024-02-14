from abc import ABC, abstractmethod

from .messages import BinaryResponse, Command, Response


class AbstractCommunicator(ABC):
    """
    Abstract base class for communication protocols.
    """

    @abstractmethod
    async def open(self) -> None:
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
    async def send(self, command: Command) -> None:
        """
        Abstract method to send a command.

        Args:
            command (Command): Command to be sent.
        """
        pass

    @abstractmethod
    async def response(self) -> Response:
        """
        Abstract method that fetches the next response.

        Returns:
            Response: The response from the server
        """
        pass

    @abstractmethod
    async def response_from(self, command: Command) -> Response:
        """
        Abstract method to fetch a response from a command.

        Args:
            command (Command): Command for which a response is desired

        Returns:
            Response: The response corresponding to the sent command.
        """
        pass

    @abstractmethod
    async def binary_response(self) -> BinaryResponse:
        """
        Abstract method that fetches the next binary response.

        Returns:
            BinaryResponse: The binary response from the server

        .. todo:: `[saga]` is this still needed?
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Abstract method to close the connection.
        """
        pass
