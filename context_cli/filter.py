"""
Module containing the filters available
"""

from abc import ABC, abstractmethod

from .context import Context
from .util import build_regexp_if_needed


class BaseFilter(ABC):
    """
    Abstract base filter class.
    """
    @abstractmethod
    def __iter__(self):
        pass


class ContextFilter(BaseFilter):
    """
    Abstract class that other filters inherit from
    """

    def __init__(self, context_generator):
        super().__init__()
        self.context_generator = context_generator

    @abstractmethod
    def is_context_valid(self, context):
        pass

    def __iter__(self):
        for context in self.context_generator:
            if self.is_context_valid(context):
                yield context


class NegateContextFilterMixin:
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
        self.regexp = build_regexp_if_needed(regexp, match_start_and_end=True)

    def is_context_valid(self, context):
        return any(self.regexp.match(line) for line in context.lines)


class NotContainsTextContextFilter(NegateContextFilterMixin, ContainsTextContextFilter):
    """
    Checks whether the context doesn't have the specified text.
    """
    pass


class NotContainsRegexContextFilter(NegateContextFilterMixin, ContainsRegexContextFilter):
    """
    Checks whether the context doesn't match a specific regex.
    """
    pass


class NotMatchesTextContextFilter(NegateContextFilterMixin, MatchesTextContextFilter):
    """
    Checks whether the context doesn't match at least one line with the text.
    """
    pass


class NotMatchesRegexContextFilter(NegateContextFilterMixin, MatchesRegexContextFilter):
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


class LineFilter(BaseFilter):

    def __init__(self, context_generator):
        super().__init__()
        self.context_generator = context_generator

    @abstractmethod
    def filter_line(self, line):
        pass

    def __iter__(self):
        for context in self.context_generator:
            yield self.get_filtered_context(context)

    def get_filter(self, context):
        return filter(self.filter_line, context.lines)

    def get_filtered_context(self, context):
        context_filter = self.get_filter(context)
        return Context(lines=list(context_filter))


class NegateLineFilterMixin:
    """
    Mixin used to negate the result of filter_line. Must be used with a class that implements LineFilter.
    """

    def filter_line(self, line):
        return not super().filter_line(line)


class ContainsTextLineFilter(LineFilter):
    """
    Filters out lines that don't contain the `text`.
    """

    def __init__(self, context_generator, text):
        super().__init__(context_generator)
        self.text = text

    def filter_line(self, line):
        return self.text in line


class ContainsRegexLineFilter(LineFilter):
    """
    Filters out the lines that don't match the regex.
    """

    def __init__(self, context_generator, regexp):
        super().__init__(context_generator)
        self.regexp = build_regexp_if_needed(regexp)

    def filter_line(self, line):
        return self.regexp.search(line)


class NotContainsTextLineFilter(NegateLineFilterMixin, ContainsTextLineFilter):
    """
    Filters out the lines that contain the `text`
    """
    pass


class NotContainsRegexLineFilter(NegateLineFilterMixin, ContainsRegexLineFilter):
    """
    Filters out the lines that contain the `regex`.
    """
    pass
