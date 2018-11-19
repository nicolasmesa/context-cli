import pytest

from context_cli.context import (
    Context, FileIterator, SingleDelimiterContextFactory, StartAndEndDelimiterContextFactory,
)
from context_cli.matcher import ContainsTextMatcher


class FileMock:
    def __init__(self, lines):
        self.lines = lines
        self.curr = 0

    def readline(self):
        curr = self.curr
        if curr < len(self.lines):
            self.curr += 1
            return self.lines[curr]
        return ''


def get_file_mock(context_lines):
    lines_with_new_line = [line + '\n' for line in context_lines]
    return FileMock(lines_with_new_line)


def get_single_delimiter_file_mock(*contexts_lines, delimiter='==='):
    lines = []
    for context_lines in contexts_lines:
        for line in context_lines:
            lines.append(line + '\n')
        lines.append(delimiter + '\n')
    lines.pop()
    return get_file_mock(lines)


CONTEXT1_LINES = [
    'Hello world!',
    'This is the first context',
    'Bye world!',
]

CONTEXT2_LINES = [
    'This is context2',
    'Hopefully, it will just work',
]


def test_context():
    context = Context(lines=CONTEXT1_LINES)
    assert context.lines == CONTEXT1_LINES
    assert str(context) == '\n'.join(CONTEXT1_LINES)


def test_file_iterator_no_unread():
    iterator = FileIterator(get_file_mock(CONTEXT1_LINES))
    assert list(iterator) == CONTEXT1_LINES


def test_file_iterator_with_unread():
    line_to_push = 'Just another line\n'
    iterator = FileIterator(get_file_mock(CONTEXT1_LINES))
    iterator.unread(line_to_push)
    assert list(iterator) == [line_to_push] + CONTEXT1_LINES


def test_single_delimiter_context_factory_exclude_delimiter():
    delimiter = '==='
    lines = CONTEXT1_LINES + CONTEXT2_LINES
    file = get_single_delimiter_file_mock(CONTEXT1_LINES, CONTEXT2_LINES)
    factory = SingleDelimiterContextFactory(file, delimiter_matcher=ContainsTextMatcher(text=delimiter), exclude_delimiter=True)

    contexts = list(factory)
    assert len(contexts) == 2

    for context in contexts:
        for line in context.lines:
            assert line in lines
            assert line != delimiter


def test_single_delimiter_context_factory_not_exclude_delimiter():
    delimiter = '==='
    lines = CONTEXT1_LINES + CONTEXT2_LINES
    file = get_single_delimiter_file_mock(CONTEXT1_LINES, CONTEXT2_LINES, delimiter=delimiter)
    factory = SingleDelimiterContextFactory(file, delimiter_matcher=ContainsTextMatcher(text=delimiter), exclude_delimiter=False)

    contexts = list(factory)
    assert len(contexts) == 2

    context_lines = contexts[0].lines + contexts[1].lines
    assert delimiter in context_lines

    for line in lines:
        assert line in context_lines


def test_single_delimiter_context_factory_empty_context_no_exclude_delimiter():
    delimiter = '==='
    lines = CONTEXT1_LINES + CONTEXT2_LINES
    file = get_single_delimiter_file_mock(CONTEXT1_LINES, CONTEXT2_LINES + [delimiter], delimiter=delimiter)
    factory = SingleDelimiterContextFactory(file, delimiter_matcher=ContainsTextMatcher(text=delimiter), exclude_delimiter=False)

    contexts = list(factory)
    assert len(contexts) == 2

    context_lines = contexts[0].lines + contexts[1].lines

    for line in lines:
        assert line in context_lines


def test_single_delimiter_context_factory_empty_context_exclude_delimiter():
    delimiter = '==='
    lines = CONTEXT1_LINES + CONTEXT2_LINES
    file = get_single_delimiter_file_mock(CONTEXT1_LINES, CONTEXT2_LINES + [delimiter], delimiter=delimiter)
    factory = SingleDelimiterContextFactory(file, delimiter_matcher=ContainsTextMatcher(text=delimiter), exclude_delimiter=True)

    contexts = list(factory)
    assert len(contexts) == 2

    context_lines = contexts[0].lines + contexts[1].lines

    for line in lines:
        assert line in context_lines
