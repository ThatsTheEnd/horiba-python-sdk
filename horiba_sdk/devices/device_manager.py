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

import importlib.resources
import platform
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, Type, final

import psutil
from loguru import logger
from mypy_extensions import KwArg, VarArg

from horiba_sdk.communication import AbstractCommunicator, Command, Response, WebsocketCommunicator
from horiba_sdk.devices.abstract_device_manager import AbstractDeviceManager
from horiba_sdk.icl_error.abstract_error import AbstractError
from horiba_sdk.icl_error.abstract_error_db import AbstractErrorDB
from horiba_sdk.icl_error.icl_error_db import ICLErrorDB

if TYPE_CHECKING:
    from horiba_sdk.devices.single_devices import AbstractDevice


def singleton(cls: Type[Any]) -> Callable[[VarArg(Any), KwArg(Any)], Any]:
    """
    Decorator to implement the Singleton pattern.
    """

    _instances: Dict[Type[Any], Any] = {}

    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return get_instance


@final
@singleton
class DeviceManager(AbstractDeviceManager):
    """
    DeviceManager class manages the lifecycle and interactions with devices.

    Attributes:
        _communicator (horiba_sdk.communication.AbstractCommunicator): The communicator class used to talk to the ICL.
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
        self._icl_communicator: WebsocketCommunicator = WebsocketCommunicator(
            'ws://' + websocket_ip + ':' + str(websocket_port)
        )
        self._icl_websocket_ip: str = websocket_ip
        self._icl_websocket_port: str = websocket_port

        error_list_path: Path = Path(str(importlib.resources.files('horiba_sdk.icl_error') / 'error_list.json'))
        self._icl_error_db: AbstractErrorDB = ICLErrorDB(error_list_path)

        logger.debug(f'Start ICL: {start_icl}')
        if start_icl:
            self.start_icl()

    def start_icl(self) -> None:
        """
        Starts the ICL software and establishes communication.
        """
        logger.debug('Starting ICL software...')
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

    async def stop_icl(self) -> None:
        """
        Stops the communication and cleans up resources.
        """
        logger.info('Requesting shutdown of ICL...')

        if not self._icl_communicator.opened():
            await self._icl_communicator.open()

        command: Command = Command('icl_shutdown', {})
        await self._icl_communicator.send(command)
        response: Response = await self._icl_communicator.response()

        if response.errors:
            self.handle_errors(response.errors)

        if self._icl_communicator.opened():
            await self._icl_communicator.close()

        logger.info('icl_shutdown command sent')

    def discover_devices(self) -> None:
        """
        Discovers and registers devices.
        (This is a placeholder and will need a proper implementation.)
        """
        # Placeholder implementation for discovering devices
        pass

    def handle_errors(self, errors: list[str]) -> None:
        """
        Handles errors, logs them, and may take corrective actions.

        Args:
            error (Exception): The exception or error to handle.
        """
        for error in errors:
            icl_error: AbstractError = self._icl_error_db.error_from(error)
            icl_error.log()

    @property
    def communicator(self) -> AbstractCommunicator:
        """
        Getter method for the communicator attribute.

        Returns:
            horiba_sdk.communication.AbstractCommunicator: Returns a new communicator instance.
        """
        return WebsocketCommunicator('ws://' + self._icl_websocket_ip + ':' + str(self._icl_websocket_port))
