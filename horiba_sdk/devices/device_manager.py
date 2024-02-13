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
import re
import subprocess
from pathlib import Path
from typing import Any, Callable, final

import psutil
from loguru import logger
from mypy_extensions import KwArg, VarArg
from overrides import override

from horiba_sdk.communication import Command, Response, WebsocketCommunicator
from horiba_sdk.devices.abstract_device_manager import AbstractDeviceManager
from horiba_sdk.icl_error import AbstractError, AbstractErrorDB, ICLErrorDB


def singleton(cls: type[Any]) -> Callable[[VarArg(Any), KwArg(Any)], Any]:
    """
    Decorator to implement the Singleton pattern.
    """

    _instances: dict[type[Any], Any] = {}

    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    def clear_instances():
        _instances.clear()

    get_instance.clear_instances = clear_instances

    return get_instance


@final
@singleton
class DeviceManager(AbstractDeviceManager):
    """
    DeviceManager class manages the lifecycle and interactions with devices.

    Attributes:
        _icl_communicator: The communicator class used to talk to the ICL.
        ccds (Dict[int, str]): CCD devices discovered.
        monos (Dict[int, str]): Monochromator devices discovered.
    """

    def __init__(self, start_icl: bool = True, websocket_ip: str = '127.0.0.1', websocket_port: str = '25010'):
        """
        Initializes the DeviceManager with the specified communicator class.

        Args:
            websocket_ip: str = '127.0.0.1': websocket IP
            websocket_port: str = '25010': websocket port
        """
        super().__init__()
        self.ccds: dict[int, 'str'] = {}
        self.monos: dict[int, 'str'] = {}
        self._icl_communicator: WebsocketCommunicator = WebsocketCommunicator(
            'ws://' + websocket_ip + ':' + str(websocket_port)
        )
        self._icl_communicator.register_binary_message_callback(self._binary_message_callback)
        self._icl_websocket_ip: str = websocket_ip
        self._icl_websocket_port: str = websocket_port

        error_list_path: Path = Path(str(importlib.resources.files('horiba_sdk.icl_error') / 'error_list.json'))
        self._icl_error_db: AbstractErrorDB = ICLErrorDB(error_list_path)

        logger.info(f'Start ICL: {start_icl}')
        if start_icl:
            self.start_icl()

    @override
    def start_icl(self) -> None:
        """
        Starts the ICL software and establishes communication.
        """
        logger.info('Starting ICL software...')
        try:
            if platform.system() != 'Windows':
                logger.log('Only Windows is supported for ICL software. Skip starting of ICL...')
                return

            icl_running = 'icl.exe' in (p.name() for p in psutil.process_iter())
            if not icl_running:
                logger.info('icl not running, starting it...')
                subprocess.Popen([r'C:\Program Files\HORIBA Scientific\SDK\icl.exe'])
        except subprocess.CalledProcessError:
            logger.error('Failed to start ICL software.')
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error('Unexpected error: %s', e)

    @override
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

    def _format_icl_binary_to_string(self, message: bytes) -> str:
        return ' '.join(format(byte, '02x') for byte in message[::-1])

    async def _binary_message_callback(self, message: bytes) -> None:
        hex_data = ' '.join(format(byte, '02x') for byte in message)
        if len(message) < 18:
            logger.warning(f'binary message not valid: {len(message)} < 16')
        logger.info(f'Received binary message: {hex_data}')
        logger.info(f'magic number: {self._format_icl_binary_to_string(message[:2])}')
        logger.info(f'message type: {self._format_icl_binary_to_string(message[2:4])}')
        logger.info(f'element type: {self._format_icl_binary_to_string(message[4:6])}')
        logger.info(f'element count: {self._format_icl_binary_to_string(message[6:10])}')
        logger.info(f'tag 1: {self._format_icl_binary_to_string(message[10:12])}')
        logger.info(f'tag 2: {self._format_icl_binary_to_string(message[12:14])}')
        logger.info(f'tag 3: {self._format_icl_binary_to_string(message[14:16])}')
        logger.info(f'tag 4: {self._format_icl_binary_to_string(message[16:18])}')
        logger.info(f'payload: {self._format_icl_binary_to_string(message[18:])}')
        logger.info(f'payload as string: {str(message[18:])}')

    @override
    async def discover_devices(self, error_on_no_device: bool = False) -> None:
        """
        Discovers the connected devices and saves them internally.
        Args:
            error_on_no_device (bool): If True, an exception is raised if no device is connected.
        """
        # Define the commands and device types in a list of tuples for iteration
        commands_and_types = [('ccd_discover', 'ccd_list', 'CCD'), ('mono_discover', 'mono_list', 'Monochromator')]

        for discover_command, list_command, device_type in commands_and_types:
            response: Response = await self._icl_communicator.execute_command(discover_command, {})
            if response.results.get('count', 0) == 0 and error_on_no_device:
                raise Exception(f'No {device_type} connected')
            response = await self._icl_communicator.execute_command(list_command, {})

            # as the responses of ccd_list and mono_list differ, we need to parse them separately
            if device_type == 'CCD':
                raw_device_list = response.results
                self.ccds = self._parse_ccds(raw_device_list)
                logger.info(f'Found {len(self.ccds)} CCD devices: {self.ccds}')
            elif device_type == 'Monochromator':
                raw_device_list = response.results['list']
                self.monos = self._parse_monos(raw_device_list)
                logger.info(f'Found {len(self.monos)} Monochromator devices: {self.monos}')

    def _parse_ccds(self, raw_device_list: dict[str, Any]) -> dict[int, str]:
        parsed_ccds = {}
        for key, value in raw_device_list.items():
            ccd_index: int = int(key.split(':')[0].replace('index', '').strip())
            ccd_type_match = re.search(r'deviceType: (.*?),', value)
            if not ccd_type_match:
                raise Exception(f'Failed to find ccd type "deviceType" in string "{value}"')
            ccd_type: str = str(ccd_type_match.group(1).strip())
            parsed_ccds[ccd_index] = ccd_type

        return parsed_ccds

    def _parse_monos(self, raw_device_list: dict[str, Any]) -> dict[int, str]:
        parsed_monos = {}
        for device_string in raw_device_list:
            mono_index: int = int(device_string.split(';')[0])
            mono_type: str = device_string.split(';')[1]
            parsed_monos[mono_index] = mono_type

        return parsed_monos

    @override
    def handle_errors(self, errors: list[str]) -> None:
        """
        Handles errors, logs them, and may take corrective actions.

        Args:
            errors (Exception): The exception or error to handle.
        """
        for error in errors:
            icl_error: AbstractError = self._icl_error_db.error_from(error)
            icl_error.log()

    @property
    def communicator(self) -> WebsocketCommunicator:
        """
        Getter method for the communicator attribute.

        Returns:
            horiba_sdk.communication.AbstractCommunicator: Returns a new communicator instance.
        """
        return self._icl_communicator
