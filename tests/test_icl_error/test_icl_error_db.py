# pylint: skip-file

import importlib
import re

import pytest

from horiba_sdk.icl_error.icl_error_db import ICLErrorDB


def test_icl_error_db_non_existing_file_throws():
    # arrange
    non_existing_error_list_path = importlib.resources.files('horiba_sdk.icl_error') / 'inexisting_dummy_file.json'
    # act
    # assert
    with pytest.raises(FileNotFoundError):
        icl_error_db = ICLErrorDB(non_existing_error_list_path)
        icl_error_db.error_from('ignored')


def test_icl_error_db_error_from_with_incorrect_string_throws():
    # arrange
    error_list_path = importlib.resources.files('horiba_sdk.icl_error') / 'error_list.json'
    icl_error_db = ICLErrorDB(error_list_path)

    # act
    # assert
    with pytest.raises(Exception, match=re.compile('^Invalid length of ICL error string')):
        icl_error_db.error_from('incorrect formatted string')


def test_icl_error_db_error_from_not_existing_error_throws():
    # arrange
    error_list_path = importlib.resources.files('horiba_sdk.icl_error') / 'error_list.json'
    icl_error_db = ICLErrorDB(error_list_path)

    # act
    # assert
    with pytest.raises(Exception, match=re.compile('^Error with number')):
        icl_error_db.error_from('[E];12345;some error string')


def test_icl_error_db_error_from():
    # arrange
    error_list_path = importlib.resources.files('horiba_sdk.icl_error') / 'error_list.json'
    icl_error_db = ICLErrorDB(error_list_path)

    # act
    icl_error = icl_error_db.error_from('[E];-1;ICL error: no parser found')

    # assert
    assert icl_error.message() == 'ICL error: no parser found'
