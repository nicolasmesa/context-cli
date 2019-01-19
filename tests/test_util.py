import re
import pytest
from mock import patch, mock

from context_cli.util import CtxRc, build_regexp_if_needed, TypeArgDoesNotExistException

REGEX = re.compile('aaa')
JSON_STR = """
    {
        "version": 1,
        "types": {
            "type1": {
                "argv": ["something"]
            }
        }
    }
"""


def test_build_regexp_if_needed_when_needed():
    regex_str = '[0-9]+'
    r = build_regexp_if_needed(regex_str)
    assert type(r) is type(REGEX)


def test_build_regexp_if_needed_when_not_needed():
    r = build_regexp_if_needed(REGEX)
    assert r is REGEX


@patch('context_cli.util.open')
def test_ctxrc_from_path(open_mock):
    file = mock.MagicMock()
    open_mock.return_value = file
    file.__enter__ = mock.MagicMock()
    read_fn = mock.MagicMock()
    file.__enter__.return_value = read_fn
    read_fn.read.return_value = JSON_STR

    ctxrc = CtxRc.from_path('/some/path')
    open_mock.assert_called_once_with('/some/path', 'r')
    assert ctxrc.get_type_argv('type1') == ['something']
    assert ctxrc.ctxrc_dict['version'] == 1
    assert ctxrc.available_types == {'type1'}


@patch('context_cli.util.open')
def test_ctxrc_from_path_no_file(open_mock):
    open_mock.side_effect = FileNotFoundError()

    ctxrc = CtxRc.from_path('/some/path')
    assert ctxrc.ctxrc_dict['version'] == 1
    assert ctxrc.ctxrc_dict['types'] == {}
    assert ctxrc.available_types == set()


def test_ctxrc_type_doesnt_exist():
    ctxrc = CtxRc({})
    with pytest.raises(TypeArgDoesNotExistException):
        ctxrc.get_type_argv('not_existent')


def test_ctxrc_add_type():
    ctxrc = CtxRc({})
    ctxrc.add_type('type', ['args'])
    assert ctxrc.get_type_argv('type') == ['args']
    assert ctxrc.available_types == {'type'}


def test_ctxrc_available_types_no_dict():
    ctxrc = CtxRc(None)
    assert ctxrc.available_types == set()


def test_ctxrc_available_types_no_types():
    ctxrc = CtxRc({})
    assert ctxrc.available_types == set()


@patch('context_cli.util.open')
def test_ctxrc_save(open_mock):
    file = mock.MagicMock()
    open_mock.return_value = file
    file.__enter__ = mock.MagicMock()
    write_fn = mock.MagicMock()
    file.__enter__.return_value = write_fn

    ctxrc = CtxRc({})
    ctxrc.save('/some/path')

    open_mock.assert_called_once_with('/some/path', 'w')
    write_fn.write.assert_called_once_with('{}')

