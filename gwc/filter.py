"""
Module containing the filters available
"""

from abc import ABC, abstractmethod

from .util import build_regexp_if_needed


class ContextFilter(ABC):
    """
    Abstract class that other filters inherit from
    """

    def __init__(self, context_generator):
        self.context_generator = context_generator

    @abstractmethod
    def is_context_valid(self, context):
        pass

    def contexts(self):
        for context in self.context_generator.contexts():
            if self.is_context_valid(context):
                yield context


class ContainsTextContextFilter(ContextFilter):
    """
    Checks whether the context contains the text.
    """

    def __init__(self, context_generator, text):
        super().__init__(context_generator)
        self.text = text

    def is_context_valid(self, context):
        return context.contains_text(self.text)


class ContainsRegexContextFilter(ContextFilter):
    """
    Checks whether the context matches a specific regex.
    """

    def __init__(self, context_generator, regexp):
        super().__init__(context_generator)
        self.regexp = build_regexp_if_needed(regexp)

    def is_context_valid(self, context):
        return context.contains_regexp(self.regexp)

