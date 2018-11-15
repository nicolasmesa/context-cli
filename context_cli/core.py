import argparse
import logging

from .context import ContextFactory
from .filter import (
    # ContextFilters
    ContainsRegexContextFilter, ContainsTextContextFilter, MatchesTextContextFilter, MatchesRegexContextFilter,
    NotContainsTextContextFilter, NotContainsRegexContextFilter, NotMatchesTextContextFilter, NotMatchesRegexContextFilter,
    NotEmptyContextFilter,

    # LineFilters
    ContainsTextLineFilter, ContainsRegexLineFilter, NotContainsTextLineFilter, NotContainsRegexLineFilter,
)
from .matcher import ContainsTextMatcher, RegexMatcher, MatchFirstLine



logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)



def main():
    import sys
    from . import __doc__

    ap = argparse.ArgumentParser(
        description=__doc__
    )
    ap.add_argument('-d', '--delimiter-text', help="delimiter text")
    ap.add_argument('-D', '--delimiter-regex', help="delimiter regex")
    ap.add_argument('-s', '--delimiter-start-text', help="delimiter start text")
    ap.add_argument('-S', '--delimiter-start-regex', help='delimiter start regex')
    ap.add_argument('-e', '--delimiter-end-text', help='delimiter end text')
    ap.add_argument('-E', '--delimiter-end-regex', help='delimiter end regex')

    ap.add_argument('-x', '--exclude-start-delimiter',
                    help='exclude start delimiter from the context', action='store_const', const=True, default=False)
    ap.add_argument('-X', '--exclude-end-delimiter',
                    help='exclude end delimiter from the context', action='store_const', const=True, default=False)
    ap.add_argument('-i', '--ignore-end-delimiter',
                    help='prevent end delimiter from being considered as a start delimiter (only applies if -X is used)',
                    action='store_const', const=True, default=False)

    # Context filters
    ap.add_argument('-c', '--contains-text',
                    help='display only contexts that have line(s) that contain this text', action='append', default=[])
    ap.add_argument('-C', '--contains-regex',
                    help='display only contexts that have line(s) that contain this regex', action='append', default=[])
    ap.add_argument('-m', '--matches-text',
                    help='display only contexts that have line(s) that exactly match this text', action='append', default=[])
    ap.add_argument('-M', '--matches-regex',
                    help='display only contexts that have line(s) that exactly match this regex', action='append', default=[])

    ap.add_argument('-c!', '--not-contains-text',
                    help="display only contexts that have line(s) that don't contain this text", action='append', default=[])
    ap.add_argument('-C!', '--not-contains-regex',
                    help="display only contexts that have line(s) that don't contain this regex", action='append', default=[])
    ap.add_argument('-m!', '--not-matches-text',
                    help="display only contexts that have line(s) that don't exactly match this text", action='append', default=[])
    ap.add_argument('-M!', '--not-matches-regex',
                    help="display only contexts that have line(s) that don't exactly match this regex", action='append', default=[])

    # Line filters
    ap.add_argument('-l', '--line-contains-text',
                    help='display only lines in the context that contain this text', action='append', default=[])
    ap.add_argument('-L', '--line-contains-regex',
                    help='display only lines in the context that contain this regex', action='append', default=[])
    ap.add_argument('-l!', '--not-line-contains-text',
                    help="display only lines in the context that don't contain this text", action='append', default=[])
    ap.add_argument('-L!', '--not-line-contains-regex',
                    help="display only lines in the context that don't contain this regex", action='append', default=[])

    # Output
    ap.add_argument('-o', '--output-delimiter', help='Output delimiter', default='')
    ap.add_argument('infiles', nargs='*', type=argparse.FileType('r'), default=sys.stdin)


    # TODO Validate combinations of these

    args = ap.parse_args()

    # TODO: These should actually be reusable classes. I should only need to pass in a start and end class and the
    # class should figure out what to return.
    delimiter_start_text = args.delimiter_start_text
    delimiter_start_regex = args.delimiter_start_regex
    delimiter_end_text = args.delimiter_end_text
    delimiter_end_regex = args.delimiter_end_regex
    delimiter_text = args.delimiter_text
    delimiter_regex = args.delimiter_regex

    start_delimiter_matcher = None
    end_delimiter_matcher = None
    exclude_start = args.exclude_start_delimiter
    exclude_end = args.exclude_end_delimiter
    ignore_end_delimiter = args.ignore_end_delimiter
    first_line = None

    if delimiter_start_text:
        start_delimiter_matcher = ContainsTextMatcher(text=delimiter_start_text)
    elif delimiter_start_regex:
        start_delimiter_matcher = RegexMatcher(regexp=delimiter_start_regex)

    if delimiter_end_text:
        end_delimiter_matcher = ContainsTextMatcher(text=delimiter_end_text)
    elif delimiter_end_regex:
        end_delimiter_matcher = RegexMatcher(regexp=delimiter_end_regex)

    if not start_delimiter_matcher and not end_delimiter_matcher:
        exclude_start = True
        exclude_end = True
        first_line = ''

        # End delimiter needs to be start delimiter
        ignore_end_delimiter = False
        if delimiter_text:
            start_delimiter_matcher = MatchFirstLine(ContainsTextMatcher(text=delimiter_text))
            end_delimiter_matcher = ContainsTextMatcher(text=delimiter_text)
        elif delimiter_regex:
            start_delimiter_matcher = MatchFirstLine(RegexMatcher(regexp=delimiter_regex))
            end_delimiter_matcher = RegexMatcher(regexp=delimiter_regex)

    if not start_delimiter_matcher or not end_delimiter_matcher:
        ap.error('Expected delimiters to be set. Use -d/-D or -s/-S and -e/-E.')

    logger.debug("args: start_delimiter_matcher:%s, end_delimiter_matcher:%s, exclude_start_delimiter:%s, exclude_end_delimiter: %s, end_delimiter_can_be_start_delimiter: %s",
                start_delimiter_matcher, end_delimiter_matcher, exclude_start, exclude_end, ignore_end_delimiter)

    first = True
    for file in args.infiles:
        cf = ContextFactory(
            file,
            start_delimiter_matcher=start_delimiter_matcher,
            end_delimiter_matcher=end_delimiter_matcher,
            exclude_start_delimiter=exclude_start,
            exclude_end_delimiter=exclude_end,
            ignore_end_delimiter=ignore_end_delimiter,
            first_line=first_line,
        )

        curr = cf

        # We do text matching first because it's a bit faster. This helps filter out some contexts before they reach the
        # regex matchers which are slower.
        for text in args.matches_text:
            curr = MatchesTextContextFilter(context_generator=curr, text=text)

        for text in args.not_matches_text:
            curr = NotMatchesTextContextFilter(context_generator=curr, text=text)

        for text in args.contains_text:
            curr = ContainsTextContextFilter(context_generator=curr, text=text)

        for text in args.not_contains_text:
            curr = NotContainsTextContextFilter(context_generator=curr, text=text)

        for regexp in args.matches_regex:
            curr = MatchesRegexContextFilter(context_generator=curr, regexp=regexp)

        for regexp in args.not_matches_regex:
            curr = NotMatchesRegexContextFilter(context_generator=curr, regexp=regexp)

        for regexp in args.contains_regex:
            curr = ContainsRegexContextFilter(context_generator=curr, regexp=regexp)

        for regexp in args.not_contains_regex:
            curr = NotContainsRegexContextFilter(context_generator=curr, regexp=regexp)

        for text in args.line_contains_text:
            curr = ContainsTextLineFilter(context_generator=curr, text=text)

        for text in args.not_line_contains_text:
            curr = NotContainsTextLineFilter(context_generator=curr, text=text)

        for regexp in args.line_contains_regex:
            curr = ContainsRegexLineFilter(context_generator=curr, regexp=regexp)

        for regexp in args.not_line_contains_regex:
            curr = NotContainsRegexLineFilter(context_generator=curr, regexp=regexp)

        # Ensure no empty contexts
        curr = NotEmptyContextFilter(context_generator=curr)

        for ctx in curr.contexts():
            if not first and args.output_delimiter:
                sys.stdout.write(args.output_delimiter)
                sys.stdout.write('\n')
            first = False

            text = str(ctx)
            sys.stdout.write(text)
            if not text.endswith('\n'):
                sys.stdout.write('\n')
            sys.stdout.flush()

