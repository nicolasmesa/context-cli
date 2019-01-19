import logging
import json
import re

logger = logging.getLogger(__name__)


class CtxRc:
    """
    Contains the dict of .ctxrc

    {
        "version": 1,
        "types": {
            "md_code": {
                "argv": [
                    "-t",
                    "md_code",
                    "-w",
                    "-S",
                    "hello",
                    "-E",
                    "world"
                ]
            }
        }
    }
    """

    def __init__(self, ctxrc_dict):
        if ctxrc_dict == None:
            ctxrc_dict = self.get_default_dict()
        self.ctxrc_dict = ctxrc_dict

    @property
    def available_types(self):
        if not 'types' in self.ctxrc_dict:
            return set()
        return set(self.ctxrc_dict['types'].keys())

    def add_type(self, type, argv):
        if not 'types' in self.ctxrc_dict:
            self.ctxrc_dict['types']  = {}
        self.ctxrc_dict['types'][type] = {
            'argv': argv
        }

    def get_type_argv(self, type):
        try:
            return self.ctxrc_dict['types'][type]['argv']
        except KeyError:
            raise TypeArgDoesNotExistException(missing_type=type)

    def save(self, path):
        with open(path, 'w') as f:
            f.write(json.dumps(self.ctxrc_dict))

    @classmethod
    def from_path(cls, path):
        try:
            with open(path, 'r') as f:
                return cls(json.loads(f.read()))
        except FileNotFoundError:
            return cls(cls.get_default_dict())

    @staticmethod
    def get_default_dict():
        return {
            'version': 1,
            'types': {}
        }


class FriendlyException(Exception):
    """
    Contains a friendly error message
    """
    pass


class TypeArgDoesNotExistException(FriendlyException):
    """
    Exception raised when the type argument passed is not in the .ctxrc
    """

    def __init__(self, missing_type):
        super().__init__(f"type {missing_type} doesn't exist in the .ctxrc")


def build_regexp_if_needed(maybe_regexp):
    """
    Creates a regexp if the `maybe_regexp` is a str.
    """
    if not isinstance(maybe_regexp, str):
        return maybe_regexp
    return re.compile(maybe_regexp)

