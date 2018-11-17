import pytest

from context_cli.matcher import ContainsTextMatcher, RegexMatcher

# Any line containing an email
PARTIAL_REGEX = '[a-zA-Z0-9_.-]+@[a-zA-Z0-9]+(\\.[a-zA-Z]+)+'
FULL_REGEX = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9]+(\\.[a-zA-Z]+)+$'
TEXT_TO_MATCH = 'hello world'


@pytest.fixture
def partial_regex_matcher():
    return RegexMatcher(regexp=PARTIAL_REGEX)


@pytest.fixture
def full_regex_matcher():
    return RegexMatcher(regexp=FULL_REGEX)


@pytest.fixture
def text_matcher():
    return ContainsTextMatcher(text=TEXT_TO_MATCH)


def test_regex_matcher_matches_partial_line(partial_regex_matcher):
    line = 'hello my email is hello@world.com and this should match!'
    assert partial_regex_matcher.matches(line) is True


def test_regex_matcher_not_matches_line(partial_regex_matcher):
    line = 'this should not match'
    assert partial_regex_matcher.matches(line) is False


def test_regex_matcher_matches_exact_line(partial_regex_matcher):
    line = 'hello@world.com'
    assert partial_regex_matcher.matches(line) is True


def test_full_regex_matcher_matches_exact_line(full_regex_matcher):
    line = 'hello@world.com'
    assert full_regex_matcher.matches(line) is True


def test_full_regex_matcher_not_matches_partial_line(full_regex_matcher):
    line = 'this line should not match even though hello@world.com is part of it'
    assert full_regex_matcher.matches(line) is False


def test_full_regex_matcher_not_matches_line(full_regex_matcher):
    line = 'should not match'
    assert full_regex_matcher.matches(line) is False


def test_text_matcher_matches_partial_line(text_matcher):
    line = 'My first program said "hello world!"'
    assert text_matcher.matches(line) is True


def test_text_matcher_matches_full_line(text_matcher):
    assert text_matcher.matches(TEXT_TO_MATCH) is True


def test_text_matcher_not_matches_line(text_matcher):
    line = 'should not match'
    assert text_matcher.matches(line) is False
