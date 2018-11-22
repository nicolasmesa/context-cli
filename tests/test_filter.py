import pytest
import re

from context_cli.context import Context

# Context filters
from context_cli.filter import (
    ContainsRegexContextFilter, ContainsTextContextFilter, MatchesTextContextFilter, MatchesRegexContextFilter,
    NotContainsRegexContextFilter, NotContainsTextContextFilter, NotMatchesRegexContextFilter,
    NotMatchesTextContextFilter, NotEmptyContextFilter,
)

# Line filters
from context_cli.filter import (
    ContainsRegexLineFilter, ContainsTextLineFilter, NotContainsRegexLineFilter, NotContainsTextLineFilter,
)


MATCH_LINES = [
    'Line 1: Hello world!',
    'Line 2: Bye world!',
    'Line 3: See ya',
    'No numbered line here',
]

NON_MATCH_LINES = [
    'None of these',
    'lines should',
    'match!',
]

context_matches = Context(lines=MATCH_LINES)
context_no_matches = Context(lines=NON_MATCH_LINES)


def get_generator_from_list(l):
    return (item for item in l)


@pytest.fixture
def context_matches_generator():
    return get_generator_from_list([context_matches])


@pytest.fixture
def context_non_matches_generator():
    return get_generator_from_list([context_no_matches])


def test_contains_text_context_filter_matches(context_matches_generator):
    context_filter = ContainsTextContextFilter(text='world', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_contains_text_context_filter_non_matches(context_non_matches_generator):
    context_filter = ContainsTextContextFilter(text='world', context_generator=context_non_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


def test_contains_regex_context_filter_matches(context_matches_generator):
    context_filter = ContainsRegexContextFilter(regexp='Line [0-9]', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_contains_regex_context_filter_non_matches(context_non_matches_generator):
    context_filter = ContainsRegexContextFilter(regexp='Line [0-9]', context_generator=context_non_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


def test_matches_text_context_filter_matches(context_matches_generator):
    context_filter = MatchesTextContextFilter(text=MATCH_LINES[-1], context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_matches_text_context_filter_non_matches(context_non_matches_generator):
    context_filter = MatchesTextContextFilter(text=MATCH_LINES[-1], context_generator=context_non_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


def test_matches_text_context_filter_non_matches_with_partial_matches(context_matches_generator):
    context_filter = MatchesTextContextFilter(text='world', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


def test_matches_regex_context_filter_matches(context_matches_generator):
    context_filter = MatchesRegexContextFilter(regexp='Line [0-9]: .+', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_matches_regex_context_filter_non_matches(context_non_matches_generator):
    context_filter = MatchesRegexContextFilter(regexp='Line [0-9]: .+', context_generator=context_non_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


def test_matches_regex_context_filter_non_matches_with_partial_matches(context_matches_generator):
    context_filter = MatchesRegexContextFilter(regexp='Line [0-9]', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


def test_not_contains_text_context_filter_matches(context_matches_generator):
    context_filter = NotContainsTextContextFilter(text='None', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_not_contains_text_context_filter_non_matches(context_non_matches_generator):
    context_filter = NotContainsTextContextFilter(text='None', context_generator=context_non_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


def test_not_contains_regex_context_filter_matches(context_matches_generator):
    context_filter = NotContainsRegexContextFilter(regexp='match.*', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_not_contains_regex_context_filter_non_matches(context_non_matches_generator):
    context_filter = NotContainsRegexContextFilter(regexp='match.*', context_generator=context_non_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


def test_not_match_text_context_filter_matches(context_matches_generator):
    context_filter = NotMatchesTextContextFilter(text='match!', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_not_match_text_context_filter_non_matches(context_non_matches_generator):
    context_filter = NotMatchesTextContextFilter(text='match!', context_generator=context_non_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


def test_not_match_text_context_filter_matches_with_partial(context_matches_generator):
    context_filter = NotMatchesTextContextFilter(text='world', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_not_match_regex_context_filter_matches(context_matches_generator):
    context_filter = NotMatchesRegexContextFilter(regexp='match.*', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_not_match_regex_context_filter_non_matches(context_non_matches_generator):
    context_filter = NotMatchesRegexContextFilter(regexp='match.*', context_generator=context_non_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


def test_not_match_regex_context_filter_matches_with_partial(context_matches_generator):
    context_filter = NotMatchesRegexContextFilter(regexp='Line [0-9]', context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_not_empty_context_filter_matches(context_matches_generator):
    context_filter = NotEmptyContextFilter(context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1
    assert contexts[0] is context_matches


def test_not_empty_context_filter_non_matches():
    empty_context = Context(lines=[])
    generator = get_generator_from_list([empty_context])
    context_filter = NotEmptyContextFilter(context_generator=generator)

    contexts = list(context_filter)
    assert len(contexts) == 0


# Line filters

def test_contains_text_line_filter(context_matches_generator):
    text_to_filter = 'Line'
    context_filter = ContainsTextLineFilter(text=text_to_filter, context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1

    assert contexts[0] is not context_matches # new copy is created
    assert len(context_matches.lines) != len(contexts[0].lines)

    context = contexts[0]
    for line in context.lines:
        assert text_to_filter in line


def test_contains_regex_line_filter(context_matches_generator):
    regex_to_filter = 'Line [0-9]:'
    regex = re.compile(regex_to_filter)

    context_filter = ContainsRegexLineFilter(regexp=regex_to_filter, context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1

    assert contexts[0] is not context_matches

    context = contexts[0]
    for line in context.lines:
        assert regex.search(line) is not None


def test_not_contains_text_line_filter(context_matches_generator):
    text_to_filter = 'world'
    context_filter = NotContainsTextLineFilter(text=text_to_filter, context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1

    assert contexts[0] is not context_matches
    assert len(context_matches.lines) != len(contexts[0].lines)

    context = contexts[0]
    for line in context.lines:
        assert text_to_filter not in line


def test_not_contains_regex_line_filter(context_matches_generator):
    regex_to_filter = 'Line [0-9]:'
    regex = re.compile(regex_to_filter)

    context_filter = NotContainsRegexLineFilter(regexp=regex_to_filter, context_generator=context_matches_generator)

    contexts = list(context_filter)
    assert len(contexts) == 1

    assert contexts[0] is not context_matches

    context = contexts[0]
    for line in context.lines:
        assert regex.search(line) is None
