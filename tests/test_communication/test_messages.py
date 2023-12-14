# FILEPATH: /c:/Projects/Horiba/SDK/horiba_python_sdk/tests/test_messages.py

from horiba_sdk.communication.messages import Command, Response


def test_command_to_json():
    command1 = Command(command='example_command', parameters={'key1': 'value1', 'key2': 'value2'})
    assert (
        command1.to_json()
        == '{"id": 1, "command": "example_command", "parameters": {"key1": "value1", "key2": "value2"}}'
    )
    command2 = Command(command='example_command', parameters={'key1': 'value1', 'key2': 'value2'})
    assert command2.id == 2


def test_response_from_json():
    response_json = (
        '{"id": 1357, "command": "example_command", "results": {"key1": "value1", "key2": "value2"}, "errors":[]}'
    )
    response = Response.from_json(response_json)
    assert response.id == 1357
    assert response.command == 'example_command'
    assert response.results == {'key1': 'value1', 'key2': 'value2'}
    assert response.errors == []
