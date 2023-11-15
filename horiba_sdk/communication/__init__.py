"""
communication

A package that provides tools and abstractions for communication. The package includes
implementations for WebSocket communication, message formatting and parsing, and an abstract
base for defining communication contracts.

Modules:
- base_communication: Contains the abstract base class defining the communication contract.
- message_parser: Provides utility functions for message formatting and parsing.
- websocket_client: Concrete implementation of the communication contract using WebSockets.

Directly Available Imports:
- WebSocketClient: WebSocket-based communication client.
- MessageParsingError: Exception raised for message format errors.
- format_message: Utility to format messages for sending.
- parse_received_message: Utility to parse received messages into a structured format.

Typical usage example:

from communication import WebSocketClient, format_message, parse_received_message

ws = WebSocketClient("ws://example.com")
await ws.connect()
await ws.send("command", {"param": "value"})
response = await ws.receive()
await ws.disconnect()
"""

# Necessary to make Python treat the directory as a package
from .abstract_communicator import AbstractCommunicator
from .communication_exception import CommunicationException
from .websocket_communicator import WebsocketCommunicator

__all__ = ['AbstractCommunicator', 'WebsocketCommunicator', 'CommunicationException']
