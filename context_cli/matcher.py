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

