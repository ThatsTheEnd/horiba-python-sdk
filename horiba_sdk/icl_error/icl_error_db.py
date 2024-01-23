import json
from pathlib import Path
from typing import final

from loguru import logger
from overrides import override

from horiba_sdk.icl_error.abstract_error import AbstractError, Severity, StringAsSeverity
from horiba_sdk.icl_error.abstract_error_db import AbstractErrorDB
from horiba_sdk.icl_error.icl_error import ICLError


@final
class ICLErrorDB(AbstractErrorDB):
    """ICL Error Database

    This class loads a error database in json format. Based on an error string from the ICL, it returns a
    `horiba_sdk.icl_error.ICLError`
    object.

    The json databse has to look like the following example:

    .. code-block:: json

       {
         "errors": [
           {
             "number": -1,
             "text": "ICL error: no parser found",
             "level": "fatal"
           },
           {
             "number": -2,
             "text": "ICL error: unknown command",
             "level": "fatal"
           }
       }

    A database exists in this module under :code:`horiba_sdk/icl_error/error_list.json`

    """

    def __init__(self, json_db_path: Path) -> None:
        if not json_db_path.is_file():
            raise FileNotFoundError(f'ICL Json DB does not exist at {json_db_path}')

        with open(json_db_path) as file:
            self._icl_error_db = json.load(file)

    @override
    def error_from(self, string: str) -> AbstractError:
        """Searches an error in the database and when successfull returns a corresponding
        `horiba_sdk.icl_error.ICLError`.

        Args:
            string (str): ICL error string in the format :code:`'[E];<error code>;<error string>'`

        Returns:
            ICLError: the corresponding error

        Raises:
            Exception: when the error string is not formatted as explained above or when no error is found with the
            given error code.
        """
        parsed_error = string.split(';')

        if len(parsed_error) != 3:
            raise Exception(f'Invalid length of ICL error string, was {len(parsed_error)} should be 3')

        error_code: int = int(parsed_error[1])
        found_error = next(
            (error for error in self._icl_error_db.get('errors', []) if error.get('number') == error_code), None
        )

        if found_error is None:
            logger.error(f'Error with number #{error_code} not found in error db')
            text: str = parsed_error[2]
            return ICLError(error_code, f'Unknown error: {text}', Severity.CRITICAL)

        level: str = found_error.get('level')
        severity: Severity = StringAsSeverity(level).to_severity()
        message: str = found_error.get('text')
        return ICLError(error_code, message, severity)
