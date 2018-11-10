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


class NegateMixin:
    """
    Mixin used to negate the result of is_context_valid. Must be used with a class that implements ContextFilter.
    """

    def is_context_valid(self, context):
        return not super().is_context_valid(context)


class ContainsTextContextFilter(ContextFilter):
    """
    Checks whether the context contains the text.
    Example
        text: 'hello world'
        matches: 'hello world', 'a hello world', 'anything that has hello world in it'
    """

    def __init__(self, context_generator, text):
        super().__init__(context_generator)
        self.text = text

    def is_context_valid(self, context):
        return any(self.text in line for line in context.lines)


class ContainsRegexContextFilter(ContextFilter):
    """
    Checks whether the context matches a specific regex. The regex doesn't need to match the whole line.
    Example:
        regex: '[a-zA-Z]'
        matches: 'abc', '1abc1', 'Abc1'

        regex: '^[a-zA-Z]$'
        matches: 'abc', 'ABc'
    """

    def __init__(self, context_generator, regexp):
        super().__init__(context_generator)
        self.regexp = build_regexp_if_needed(regexp)

    def is_context_valid(self, context):
        return any(self.regexp.search(line) for line in context.lines)


class MatchesTextContextFilter(ContextFilter):
    """
    Checks whether the context matches at least one line with the text.
    Example
        text: 'hello world'
        matches: 'hello world'
        doesn't match: 'a hello world'
    """

    def __init__(self, context_generator, text):
        super().__init__(context_generator)
        self.text = text

    def is_context_valid(self, context):
        return any(self.text == line for line in context.lines)


class MatchesRegexContextFilter(ContextFilter):
    """
    Checks whether the context matches at least one line with the regex (at least one **whole** line needs to match).
    Examples:
        regex: '[a-zA-Z]'
        matches: 'abc', 'ABC'
        doesn't match: 'abc1', '1abc'
    """
    def __init__(self, context_generator, regexp):
        super().__init__(context_generator)
        if isinstance(regexp, str):
            if not regexp.startswith('^'):
                regexp = '^' + regexp
            if not regexp.endswith('$'):
                regexp = regexp + '$'
        self.regexp = build_regexp_if_needed(regexp)

    def is_context_valid(self, context):
        return any(self.regexp.match(line) for line in context.lines)


class NotContainsTextContextFilter(NegateMixin, ContainsTextContextFilter):
    """
    Checks whether the context doesn't have the specified text.
    """
    pass


class NotContainsRegexContextFilter(NegateMixin, ContainsRegexContextFilter):
    """
    Checks whether the context doesn't match a specific regex.
    """
    pass


class NotMatchesTextContextFilter(NegateMixin, MatchesTextContextFilter):
    """
    Checks whether the context doesn't match at least one line with the text.
    """
    pass


class NotMatchesRegexContextFilter(NegateMixin, MatchesRegexContextFilter):
    """
    Checks whether the context doesn't match at least one line with the regex.
    """
    pass


class NotEmptyContextFilter(ContextFilter):
    """
    Checks whether the context is not empty.
    """

    def is_context_valid(self, context):
        return len(context.lines) > 0
