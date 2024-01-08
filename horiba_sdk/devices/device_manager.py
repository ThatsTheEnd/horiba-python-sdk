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

import platform
import subprocess
from typing import TYPE_CHECKING

import psutil
from loguru import logger

from horiba_sdk.communication import AbstractCommunicator, WebsocketCommunicator

if TYPE_CHECKING:
    from horiba_sdk.devices.single_devices import AbstractDevice


class SingletonMeta(type):
    """
    Metaclass to implement the Singleton pattern.
    """

    _instances: dict[type, 'SingletonMeta'] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DeviceManager(metaclass=SingletonMeta):
    """
    DeviceManager class manages the lifecycle and interactions with devices.

    Attributes:
        _communicator (horiba_sdk.communication.AbstractCommunicator): The communicator class used to talk to devices.
        devices (List[Device]): List of managed devices.
    """

    def __init__(self, start_icl: bool = True, websocket_ip: str = '127.0.0.1', websocket_port: str = '25010'):
        """
        Initializes the DeviceManager with the specified communicator class.

        Args:
            websocket_ip: str = '127.0.0.1': websocket IP
            websocket_port: str = '25010': websocket port
        """
        self.devices: list['AbstractDevice'] = []
        self._communicator: WebsocketCommunicator = WebsocketCommunicator(
            'ws://' + websocket_ip + ':' + str(websocket_port)
        )
        if start_icl:
            self.start_icl()

    @staticmethod
    def start_icl() -> None:
        """
        Starts the ICL software and establishes communication.
        """
        try:
            if platform.system() == 'Windows':
                icl_running = 'icl.exe' in (p.name() for p in psutil.process_iter())
                if not icl_running:
                    logger.debug('icl not running, starting it...')
                    subprocess.Popen([r'C:\Program Files\HORIBA Scientific\SDK\icl.exe'])
        except subprocess.CalledProcessError:
            logger.error('Failed to start ICL software.')
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error('Unexpected error: %s', e)

    def stop_icl(self) -> None:
        """
        Stops the communication and cleans up resources.
        """
        pass

    def discover_devices(self) -> None:
        """
        Discovers and registers devices.
        (This is a placeholder and will need a proper implementation.)
        """
        # Placeholder implementation for discovering devices
        pass

    @staticmethod
    def handle_error(error: Exception) -> None:
        """
        Handles errors, logs them, and may take corrective actions.

        Args:
            error (Exception): The exception or error to handle.
        """
        logger.error('Unexpected error: %s', error)

    @property
    def communicator(self) -> AbstractCommunicator:
        """
        Getter method for the communicator attribute.

        Returns:
            horiba_sdk.communication.AbstractCommunicator: Returns the internal communicator instance.
        """
        return self._communicator
