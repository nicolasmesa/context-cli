from abc import ABC, abstractmethod
import argparse
from collections import deque
import logging
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def build_regexp_if_needed(maybe_regexp):
    if isinstance(maybe_regexp, str):
        return re.compile(maybe_regexp)
    return maybe_regexp


class Context:

    def __init__(self, lines):
        self.lines = lines

    def contains_text(self, text):
        return any(text in line for line in self.lines)

    def contains_regexp(self, regexp):
        regexp = build_regexp_if_needed(regexp)
        return any(regexp.match(line) for line in self.lines)

    def matches_text(self, text):
        return any(text == line for line in self.lines)

    def matches_regexp(self, regexp):
        # We could add ^ and $ at the end if it doesn't have it already, but I'm not sure how useful.
        return self.contains_regexp(regexp)

    def __str__(self):
        return '\n'.join(self.lines)


class ContextFilter(ABC):

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

    def __init__(self, context_generator, text):
        super().__init__(context_generator)
        self.text = text

    def is_context_valid(self, context):
        return context.contains_text(self.text)


class ContainsRegexContextFilter(ContextFilter):

    def __init__(self, context_generator, regexp):
        super().__init__(context_generator)
        self.regexp = build_regexp_if_needed(regexp)

    def is_context_valid(self, context):
        return context.contains_regexp(self.regexp)


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


class ContextFactory:

    def __init__(self, file, start_delimiter_matcher, end_delimiter_matcher, exclude_start_delimiter=False, exclude_end_delimiter=False):

        self.file = file

        self.start_delimiter_matcher = start_delimiter_matcher
        self.end_delimiter_matcher = end_delimiter_matcher
        self.exclude_start_delimiter = exclude_start_delimiter
        self.exclude_end_delimiter = exclude_end_delimiter

        self.delimiter_start_fn = None
        self.delimiter_end_fn = None

        self.stack = deque()

    def is_start(self, line):
        return self.start_delimiter_matcher.matches(line)

    def is_end(self, line):
        return self.end_delimiter_matcher.matches(line)

    def contexts(self):
        while True:
            start_line = self._get_next_start_line()

            if start_line is None:
                break

            context_lines = []

            if not self.exclude_start_delimiter:
                context_lines.append(start_line)

            # TODO Ugly code here. Simplify this
            for line in self._lines():
                if line is None:
                    break
                if self.is_end(line):
                    if self.exclude_end_delimiter:
                        self._push(line)
                    else:
                        context_lines.append(line)
                    break
                context_lines.append(line)

            yield Context(context_lines)

    def _get_next_start_line(self):
        for line in self._lines():
            if self.is_start(line):
                return line
        return None

    def _push(self, line):
        self.stack.append(line)

    def _pop(self):
        return self.stack.pop()

    def _lines(self):
        line = 'dummy'
        while line:
            try:
                line = self._pop()
                yield line
                continue
            except IndexError:
                pass

            line = self.file.readline()
            yield line.rstrip('\n')


def main():
    import sys

    ap = argparse.ArgumentParser(
        description='Grep with context'
    )
    ap.add_argument('-d', '--delimiter-text', help="delimiter text")
    ap.add_argument('-D', '--delimiter-regex', help="delimiter regex")
    ap.add_argument('-s', '--delimiter-start-text', help="delimiter start text")
    ap.add_argument('-S', '--delimiter-start-regex', help='delimiter start regex')
    ap.add_argument('-e', '--delimiter-end-text', help='delimiter end text')
    ap.add_argument('-E', '--delimiter-end-regex', help='delimiter end regex')

    ap.add_argument('-dx', '--delimiter-text-exclude', help="delimiter text but exclude it from the contexts")
    ap.add_argument('-Dx', '--delimiter-regex-exclude', help="delimiter regex but exclude it from the contexts")
    ap.add_argument('-sx', '--delimiter-start-text-exclude', help="delimiter start text but exclude it from the contexts")
    ap.add_argument('-Sx', '--delimiter-start-regex-exclude', help='delimiter start regex but exclude it from the contexts')
    ap.add_argument('-ex', '--delimiter-end-text-exclude', help='delimiter end text but exclude it from the contexts')
    ap.add_argument('-Ex', '--delimiter-end-regex-exclude', help='delimiter end regex but exclude it from the contexts')

    ap.add_argument('-c', '--contains-text', help='context contains text', action='append', default=[])
    ap.add_argument('-C', '--contains-regex', help='context contains regex', action='append', default=[])
    ap.add_argument('-m', '--matches-text', help='context matches text', action='append', default=[])
    ap.add_argument('-M', '--matches-regex', help='context matches regex', action='append', default=[])
    ap.add_argument('-l', '--line-contains-text', help='line contains text', action='append', default=[])
    ap.add_argument('-L', '--line-contains-regex', help='line contains regex', action='append', default=[])

    ap.add_argument('-c!', '--not-contains-text', help='context does not contain text', action='append', default=[])
    ap.add_argument('-C!', '--not-contains-regex', help='context contains regex', action='append', default=[])
    ap.add_argument('-m!', '--not-matches-text', help='context does not match text', action='append', default=[])
    ap.add_argument('-M!', '--not-matches-regex', help='context does not match regex', action='append', default=[])
    ap.add_argument('-l!', '--not-line-contains-text', help='line doest not contain text', action='append', default=[])
    ap.add_argument('-L!', '--not-line-contains-regex', help='line does not contain regex', action='append', default=[])

    ap.add_argument('-o', '--output-delimiter', help='Output delimiter', default='')

    ap.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

    # TODO Validate combinations of these

    args = ap.parse_args()


    # TODO: These should actually be reusable classes. I should only need to pass in a start and end class and the
    # class should figure out what to return.
    delimiter_start_text = args.delimiter_start_text or args.delimiter_start_text_exclude
    delimiter_start_regex = args.delimiter_start_regex or args.delimiter_start_regex_exclude
    delimiter_end_text = args.delimiter_end_text or args.delimiter_end_text_exclude
    delimiter_end_regex = args.delimiter_end_regex or args.delimiter_end_regex_exclude
    delimiter_text = args.delimiter_text or args.delimiter_text_exclude
    delimiter_regex = args.delimiter_regex or args.delimiter_regex_exclude

    start_delimiter_matcher = None
    end_delimiter_matcher = None
    exclude_start = False
    exclude_end = False

    if delimiter_start_text:
        start_delimiter_matcher = ContainsTextMatcher(text=delimiter_start_text)
        if args.delimiter_start_text_exclude:
            exclude_start = True
    elif delimiter_start_regex:
        start_delimiter_matcher = RegexMatcher(regexp=delimiter_start_regex)
        if args.delimiter_start_regex_exclude:
            exclude_start = True

    if delimiter_end_text:
        end_delimiter_matcher = ContainsTextMatcher(text=delimiter_end_text)
        if args.delimiter_end_text_exclude:
            exclude_end = True
    elif delimiter_end_regex:
        end_delimiter_matcher = RegexMatcher(regexp=delimiter_end_regex)
        if args.delimiter_end_regex_exclude:
            exclude_end = True

    if not start_delimiter_matcher and not end_delimiter_matcher:
        if delimiter_text:
            start_delimiter_matcher = ContainsTextMatcher(text=delimiter_text)
            end_delimiter_matcher = ContainsTextMatcher(text=delimiter_text)
            if args.delimiter_text_exclude:
                exclude_start = True
                exclude_end = True
        elif delimiter_regex:
            start_delimiter_matcher = RegexMatcher(regexp=delimiter_regex)
            end_delimiter_matcher = RegexMatcher(regexp=delimiter_regex)
            if args.delimiter_regex_exclude:
                exclude_start = True
                exclude_end = True

    cf = ContextFactory(
        args.infile,
        start_delimiter_matcher=start_delimiter_matcher,
        end_delimiter_matcher=end_delimiter_matcher,
        exclude_start_delimiter=exclude_start,
        exclude_end_delimiter=exclude_end,
    )

    curr = cf

    for text in args.contains_text:
        curr = ContainsTextContextFilter(context_generator=curr, text=text)

    for regexp in args.contains_regex:
        curr = ContainsRegexContextFilter(context_generator=curr, regexp=regexp)

    first = True
    for ctx in curr.contexts():
        if not first:
            sys.stdout.write(args.output_delimiter)
            sys.stdout.write('\n')
        first = False

        text = str(ctx)
        sys.stdout.write(text)
        if not text.endswith('\n'):
            sys.stdout.write('\n')
        sys.stdout.flush()


if __name__ == '__main__':
    main()
