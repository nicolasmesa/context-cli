"""
Module containing matchers
"""

from abc import ABC, abstractmethod

from .util import build_regexp_if_needed


import logging
logger = logging.getLogger(__name__)


class Matcher(ABC):

    @abstractmethod
    def matches(self, line):
        pass


# TODO Remove this class. This responsibility should not go in the matcher.
class MatchFirstLine(Matcher):

    def __init__(self, matcher):
        self.matcher = matcher
        self._first = True

    def matches(self, line):
        if self._first:
            self._first = False
            return True
        return self.matcher.matches(line)


class RegexMatcher(Matcher):

    def __init__(self, regexp):
        self.regexp = build_regexp_if_needed(regexp)

    def matches(self, line):
        return self.regexp.match(line) is not None


class ContainsTextMatcher(Matcher):

    def __init__(self, text):
        self.text = text

    def matches(self, line):
        return self.text in line


class ExactTextMatcher(Matcher):

    def __init__(self, text):
        self.text = text

    def matches(self, line):
        return line == self.text

