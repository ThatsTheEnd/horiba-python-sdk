from abc import ABC, abstractmethod
from typing import Union


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
    async def send(self, command: str) -> None:
        """
        Abstract method to send a command.

        Args:
            command (str): Command to be sent.
        """
        pass

    @abstractmethod
    async def response(self) -> Union[str, bytes]:
        """
        Abstract method that fetches the next response.

        Returns:
            str: String containing the response
        """
        pass

    @abstractmethod
    async def send_and_receive(self, command: str) -> Union[str, bytes]:
        """
        Abstract method that sends a command to the WebSocket server and waits for the response.

        Args:
            command (str): The command to send to the server.

        Returns:
            Union[str, bytes]: The response from the server as a string or bytes.

        """

    @abstractmethod
    async def close(self) -> None:
        """
        Abstract method to close the connection.
        """
        pass
