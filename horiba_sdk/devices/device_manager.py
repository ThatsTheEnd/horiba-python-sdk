"""
Device Manager Module

This module provides the DeviceManager class, responsible for managing the lifecycle and interactions with devices.

Import Structure Explanation:
-----------------------------
Due to the interdependence between the AbstractDevice class and the DeviceManager class, we face a potential circular
import issue. Specifically, the AbstractDevice class needs knowledge about the DeviceManager, and vice versa.

To handle this challenge while still allowing type checking tools like mypy to function correctly, we've made use of
Python's TYPE_CHECKING constant available in the `typing` module. This constant is `True` only when type checking is
performed, and not during runtime. This ensures that:

1. At runtime, there's no circular import, as the import statement within the TYPE_CHECKING block is effectively
   ignored.

2. During type checking (like when running mypy), the import statement is executed, allowing mypy to recognize and
   validate types.

Therefore, the `if TYPE_CHECKING:` block is a solution to maintain clean architecture while still benefiting from type
checking capabilities.

Notes:
------
The forward declaration method ("ClassName") is used for type hints within the module to further prevent any runtime
circular dependencies.

For more details on the TYPE_CHECKING constant and its usage, refer to:
https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING
"""

import logging
import subprocess
from typing import Dict, List, Type
from horiba_sdk.communication import AbstractCommunicator, TelnetCommunicator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from horiba_sdk.devices.single_devices import AbstractDevice

logging.basicConfig(level=logging.INFO)


class SingletonMeta(type):
    """
    Metaclass to implement the Singleton pattern.
    """

    _instances: Dict[Type, "SingletonMeta"] = {}

    def __call__(cls, *args, **kwargs):  # type: ignore
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DeviceManager(metaclass=SingletonMeta):
    """
    DeviceManager class manages the lifecycle and interactions with devices.

    Attributes:
        _communicator (AbstractCommunicator): The communicator class used to talk to devices.
        devices (List[Device]): List of managed devices.
    """

    def __init__(
        self, communicator_cls: Type[AbstractCommunicator] = TelnetCommunicator, start_acl: bool = True
    ):
        """
        Initializes the DeviceManager with the specified communicator class.

        Args:
            communicator_cls (Type[AbstractCommunicator], optional): Communicator class to be used.
            Defaults to TelNetCommunicator.
        """
        self.devices: List["AbstractDevice"] = []
        self._communicator = communicator_cls()
        if start_acl:
            self.start_acl()

    @staticmethod
    def start_acl() -> None:
        """
        Starts the ACL software and establishes communication.
        """
        try:
            subprocess.run(["C:\\Program Files\\Horiba Scientific\\SDK\\icl.exe"], check=True)
        except subprocess.CalledProcessError:
            logging.error("Failed to start ACL software.")
        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error("Unexpected error: %s", e)

    def stop_acl(self) -> None:
        """
        Stops the communication and cleans up resources.
        """
        self._communicator.close()

    def discover_devices(self) -> None:
        """
        Discovers and registers devices.
        (This is a placeholder and will need a proper implementation.)
        """
        # Placeholder implementation for discovering devices
        # In reality, you'd likely use your communicator to search for devices and populate self.devices
        pass

    @staticmethod
    def handle_error(error: Exception) -> None:
        """
        Handles errors, logs them, and may take corrective actions.

        Args:
            error (Exception): The exception or error to handle.
        """
        logging.error("Unexpected error: %s", error)

    @property
    def communicator(self) -> AbstractCommunicator:
        """
        Getter method for the communicator attribute.

        Returns:
            AbstractCommunicator: Returns the internal communicator instance.
        """
        return self._communicator
