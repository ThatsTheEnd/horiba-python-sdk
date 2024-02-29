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
    async def request_with_response(self, command: Command,  timeout: int = 5) -> Response:
        """
        Abstract method to fetch a response from a command.

        Args:
            command (Command): Command for which a response is desired
            timeout (int): Time in [s] to wait for the response before giving up. Defaults to 5s

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
