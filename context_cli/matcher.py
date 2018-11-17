"""
Module containing matchers
"""

from abc import ABC, abstractmethod

from .util import build_regexp_if_needed


import logging
logger = logging.getLogger(__name__)


class Matcher(ABC):

    @abstractmethod
    def matches(self, line): # pragma: no cover
        pass


class RegexMatcher(Matcher):
    """
    Matcher to match a line against a Regex.
    """

    def __init__(self, regexp):
        self.regexp = build_regexp_if_needed(regexp)

    def matches(self, line):
        """
        Returns True if the line argument matches the regex.
        """
        return self.regexp.search(line) is not None


class ContainsTextMatcher(Matcher):
    """
    Matches a line against a text.
    """

    def __init__(self, text):
        self.text = text

    def matches(self, line):
        """
        Returns true if the line argument contains the text.
        """
        return self.text in line


