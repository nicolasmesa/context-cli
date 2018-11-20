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
            lines.append(line)
        lines.append(delimiter)
    lines.pop()
    return get_file_mock(lines)


def get_start_and_end_delimiter(*contexts_lines, start_delimiter='===', end_delimiter='...', add_stuff_inbetween=False):
    lines = []
    if add_stuff_inbetween:
        for _ in range(5):
            lines.append('This should not show up')

    for context_lines in contexts_lines:
        lines.append(start_delimiter)
        for line in context_lines:
            lines.append(line)
        lines.append(end_delimiter)

        if add_stuff_inbetween:
            for _ in range(5):
                lines.append('This should not show up')
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
    assert repr(context) != str(context)


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
    file = get_single_delimiter_file_mock([delimiter] + CONTEXT1_LINES, CONTEXT2_LINES + [delimiter], delimiter=delimiter)
    factory = SingleDelimiterContextFactory(file, delimiter_matcher=ContainsTextMatcher(text=delimiter), exclude_delimiter=False)

    contexts = list(factory)
    assert len(contexts) == 2

    context_lines = contexts[0].lines + contexts[1].lines

    for line in lines:
        assert line in context_lines


def test_single_delimiter_context_factory_empty_context_exclude_delimiter():
    delimiter = '==='
    lines = CONTEXT1_LINES + CONTEXT2_LINES
    file = get_single_delimiter_file_mock([delimiter] + CONTEXT1_LINES, CONTEXT2_LINES + [delimiter], delimiter=delimiter)
    factory = SingleDelimiterContextFactory(file, delimiter_matcher=ContainsTextMatcher(text=delimiter), exclude_delimiter=True)

    contexts = list(factory)
    assert len(contexts) == 2

    context_lines = contexts[0].lines + contexts[1].lines

    for line in lines:
        assert line in context_lines


def test_start_and_end_delimiter_context_factory_defaults_different_delimiters():
    start_delimiter = '===='
    end_delimiter = '...'
    file = get_start_and_end_delimiter(CONTEXT1_LINES, CONTEXT2_LINES, start_delimiter=start_delimiter, end_delimiter=end_delimiter)
    factory = StartAndEndDelimiterContextFactory(
        file,
        start_delimiter_matcher=ContainsTextMatcher(text=start_delimiter),
        end_delimiter_matcher=ContainsTextMatcher(text=end_delimiter),
    )

    contexts = list(factory)
    assert len(contexts) == 2

    expected_contexts_lines = [
        [start_delimiter] + CONTEXT1_LINES + [end_delimiter],
        [start_delimiter] + CONTEXT2_LINES + [end_delimiter],
    ]

    for expected_lines, context in zip(expected_contexts_lines, contexts):
        assert context.lines == expected_lines


def test_start_and_end_delimiter_context_factory_different_delimiters_separated():
    start_delimiter = '===='
    end_delimiter = '...'
    file = get_start_and_end_delimiter(
        CONTEXT1_LINES, CONTEXT2_LINES,start_delimiter=start_delimiter, end_delimiter=end_delimiter, add_stuff_inbetween=True
    )
    factory = StartAndEndDelimiterContextFactory(
        file,
        start_delimiter_matcher=ContainsTextMatcher(text=start_delimiter),
        end_delimiter_matcher=ContainsTextMatcher(text=end_delimiter),
    )

    contexts = list(factory)
    assert len(contexts) == 2

    expected_contexts_lines = [
        [start_delimiter] + CONTEXT1_LINES + [end_delimiter],
        [start_delimiter] + CONTEXT2_LINES + [end_delimiter],
    ]

    for expected_lines, context in zip(expected_contexts_lines, contexts):
        assert context.lines == expected_lines


def test_start_and_end_delimiter_context_factory_defaults_different_delimiters_exclude_start():
    start_delimiter = '===='
    end_delimiter = '...'
    file = get_start_and_end_delimiter(CONTEXT1_LINES, CONTEXT2_LINES, start_delimiter=start_delimiter,
                                       end_delimiter=end_delimiter)
    factory = StartAndEndDelimiterContextFactory(
        file,
        start_delimiter_matcher=ContainsTextMatcher(text=start_delimiter),
        end_delimiter_matcher=ContainsTextMatcher(text=end_delimiter),
        exclude_start_delimiter=True,
    )

    contexts = list(factory)
    assert len(contexts) == 2

    expected_contexts_lines = [
        CONTEXT1_LINES + [end_delimiter],
        CONTEXT2_LINES + [end_delimiter],
    ]

    for expected_lines, context in zip(expected_contexts_lines, contexts):
        assert context.lines == expected_lines


def test_start_and_end_delimiter_context_factory_defaults_different_delimiters_exclude_end():
    start_delimiter = '===='
    end_delimiter = '...'
    file = get_start_and_end_delimiter(CONTEXT1_LINES, CONTEXT2_LINES, start_delimiter=start_delimiter,
                                       end_delimiter=end_delimiter)
    factory = StartAndEndDelimiterContextFactory(
        file,
        start_delimiter_matcher=ContainsTextMatcher(text=start_delimiter),
        end_delimiter_matcher=ContainsTextMatcher(text=end_delimiter),
        exclude_end_delimiter=True
    )

    contexts = list(factory)
    assert len(contexts) == 2

    expected_contexts_lines = [
        [start_delimiter] + CONTEXT1_LINES,
        [start_delimiter] + CONTEXT2_LINES,
    ]

    for expected_lines, context in zip(expected_contexts_lines, contexts):
        assert context.lines == expected_lines


def test_start_and_end_delimiter_context_factory_defaults_different_delimiters_exclude_and_not_ignore_end():
    start_delimiter = '===='
    end_delimiter = '...'
    file = get_start_and_end_delimiter(CONTEXT1_LINES, CONTEXT2_LINES, start_delimiter=start_delimiter,
                                       end_delimiter=end_delimiter)
    factory = StartAndEndDelimiterContextFactory(
        file,
        start_delimiter_matcher=ContainsTextMatcher(text=start_delimiter),
        end_delimiter_matcher=ContainsTextMatcher(text=end_delimiter),
        exclude_end_delimiter=True,
        ignore_end_delimiter=False,
    )

    contexts = list(factory)
    assert len(contexts) == 2

    expected_contexts_lines = [
        [start_delimiter] + CONTEXT1_LINES,
        [start_delimiter] + CONTEXT2_LINES,
    ]

    for expected_lines, context in zip(expected_contexts_lines, contexts):
        assert context.lines == expected_lines


def test_start_and_end_delimiter_context_factory_defaults_different_delimiters_exclude_start_and_end():
    start_delimiter = '===='
    end_delimiter = '...'
    file = get_start_and_end_delimiter(CONTEXT1_LINES, CONTEXT2_LINES, start_delimiter=start_delimiter,
                                       end_delimiter=end_delimiter)
    factory = StartAndEndDelimiterContextFactory(
        file,
        start_delimiter_matcher=ContainsTextMatcher(text=start_delimiter),
        end_delimiter_matcher=ContainsTextMatcher(text=end_delimiter),
        exclude_start_delimiter=True,
        exclude_end_delimiter=True,
    )

    contexts = list(factory)
    assert len(contexts) == 2

    expected_contexts_lines = [
        CONTEXT1_LINES,
        CONTEXT2_LINES,
    ]

    for expected_lines, context in zip(expected_contexts_lines, contexts):
        assert context.lines == expected_lines


def test_start_and_end_delimiter_context_factory_end_delimiter_contains_start_delimiter_ignore_end_delimiter():
    start_delimiter = 'start_delimiter'
    end_delimiter = 'end_delimiter start_delimiter'

    file = get_start_and_end_delimiter(CONTEXT1_LINES, CONTEXT2_LINES, start_delimiter=start_delimiter,
                                       end_delimiter=end_delimiter)
    factory = StartAndEndDelimiterContextFactory(
        file,
        start_delimiter_matcher=ContainsTextMatcher(text=start_delimiter),
        end_delimiter_matcher=ContainsTextMatcher(text=end_delimiter),
        exclude_start_delimiter=True,
        exclude_end_delimiter=True,
        ignore_end_delimiter=True,
    )

    contexts = list(factory)
    assert len(contexts) == 2

    expected_contexts_lines = [
        CONTEXT1_LINES,
        CONTEXT2_LINES,
    ]

    for expected_lines, context in zip(expected_contexts_lines, contexts):
        assert context.lines == expected_lines



def test_start_and_end_delimiter_context_factory_end_delimiter_contains_start_delimiter_not_ignore_end_delimiter():
    start_delimiter = 'start_delimiter'
    end_delimiter = 'end_delimiter start_delimiter'

    context1 = [
        'This should be there',
        'And so should this',
    ]
    context2 = [
        'This is the second context',
        'And so is this',
    ]
    lines = ['This should not be there', start_delimiter] + context1 + [end_delimiter] + context2 + [end_delimiter]
    file = get_file_mock(lines)

    factory = StartAndEndDelimiterContextFactory(
        file,
        start_delimiter_matcher=ContainsTextMatcher(text=start_delimiter),
        end_delimiter_matcher=ContainsTextMatcher(text=end_delimiter),
        exclude_start_delimiter=True,
        exclude_end_delimiter=True,
        ignore_end_delimiter=False,
    )

    contexts = list(factory)
    # An empty context is created since the last end_delimiter is treated as a start_delimiter
    assert len(contexts) == 3

    expected_contexts_lines = [
        context1,
        context2,
        [], # Empty lines
    ]

    for expected_lines, context in zip(expected_contexts_lines, contexts):
        assert context.lines == expected_lines


def test_start_and_end_delimiter_context_factory_incomplete():
    start_delimiter = 'start_delimiter'
    end_delimiter = 'end_delimiter'

    file = get_start_and_end_delimiter(CONTEXT1_LINES, CONTEXT2_LINES, start_delimiter=start_delimiter,
                                       end_delimiter=end_delimiter)
    # Remove last delimiter
    file.lines.pop()

    factory = StartAndEndDelimiterContextFactory(
        file,
        start_delimiter_matcher=ContainsTextMatcher(text=start_delimiter),
        end_delimiter_matcher=ContainsTextMatcher(text=end_delimiter),
        exclude_start_delimiter=True,
        exclude_end_delimiter=True,
    )

    contexts = list(factory)
    assert len(contexts) == 2

    expected_contexts_lines = [
        CONTEXT1_LINES,
        CONTEXT2_LINES,
    ]

    for expected_lines, context in zip(expected_contexts_lines, contexts):
        assert context.lines == expected_lines
