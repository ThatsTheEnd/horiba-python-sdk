# pylint: skip-file


from horiba_sdk.icl_error import Severity, StringAsSeverity


def test_string_as_severity_parses():
    # arrange
    severity = 'fatal'
    string_as_severity = StringAsSeverity(severity)

    # act
    actual_severity = string_as_severity.to_severity()

    # assert
    assert actual_severity == Severity.CRITICAL


def test_string_as_severity_unknown_severity_is_info_level():
    # arrange
    severity = 'asdf'
    string_as_severity = StringAsSeverity(severity)

    # act
    actual_severity = string_as_severity.to_severity()

    # assert
    assert actual_severity == Severity.INFO
