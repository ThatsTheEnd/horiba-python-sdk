import json
from typing import Any

from .abstracts import AbstractCommandBuilder


class WebSocketCommandBuilder(AbstractCommandBuilder):
    """
    Builds commands for WebSocket communication.
    """

    @staticmethod
    def build(device_id: int, command: str, **kwargs: Any) -> str:
        """
        Build a WebSocket command in JSON format.

        Args:
            device_id (int): ID of the device.
            command (str): Command to be sent.
            **kwargs: Additional keyword arguments.

        Returns:
            str: Formatted WebSocket command as a JSON string.
        """
        cmd_dict = {
            "id": device_id,
            "command": command,
            "parameters": kwargs
        }
        return json.dumps(cmd_dict)
