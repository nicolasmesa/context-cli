import argparse
import logging
import sys

from .context import StartAndEndDelimiterContextFactory, SingleDelimiterContextFactory
from .filter import (
    # ContextFilters
    ContainsRegexContextFilter, ContainsTextContextFilter, MatchesTextContextFilter, MatchesRegexContextFilter,
    NotContainsTextContextFilter, NotContainsRegexContextFilter, NotMatchesTextContextFilter, NotMatchesRegexContextFilter,
    NotEmptyContextFilter,

    # LineFilters
    ContainsTextLineFilter, ContainsRegexLineFilter, NotContainsTextLineFilter, NotContainsRegexLineFilter,
)
from .matcher import ContainsTextMatcher, RegexMatcher

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def start_and_end_delimiter_context_factory_creator(start_delimiter_matcher, end_delimiter_matcher, exclude_start, exclude_end, ignore_end_delimiter):
    """Returns a factory function for StartAndEndDelimiterContextFactory where only the file is needed"""

    def factory(file):
        return StartAndEndDelimiterContextFactory(
            file,
            start_delimiter_matcher=start_delimiter_matcher,
            end_delimiter_matcher=end_delimiter_matcher,
            exclude_start_delimiter=exclude_start,
            exclude_end_delimiter=exclude_end,
            ignore_end_delimiter=ignore_end_delimiter,
        )

    return factory


def single_delimiter_context_factory_creator(delimiter_matcher, exclude_delimiter):
    """
    Returns a factory function for SingleDelimiterContextFactory where only the file is neded.
    """

    def factory(file):
        return SingleDelimiterContextFactory(
            file,
            delimiter_matcher=delimiter_matcher,
            exclude_delimiter=exclude_delimiter
        )
    return factory


def get_context_factory_from_args(ap, args):
    """
    Uses the arguments to create a factory of context factories.
    """

    start_delimiter_matcher = args.start_delimiter_matcher
    end_delimiter_matcher = args.end_delimiter_matcher
    delimiter_matcher = args.delimiter_matcher

    exclude_start = args.exclude_start_delimiter
    exclude_end = args.exclude_end_delimiter
    ignore_end_delimiter = args.ignore_end_delimiter

    if delimiter_matcher and (start_delimiter_matcher or end_delimiter_matcher):
        ap.error('-d/-D cannot be used with -s/-S or -e/-E')

    context_factory_factory = None
    if start_delimiter_matcher and end_delimiter_matcher:
        context_factory_factory = start_and_end_delimiter_context_factory_creator(
            start_delimiter_matcher=start_delimiter_matcher,
            end_delimiter_matcher=end_delimiter_matcher,
            exclude_start=exclude_start,
            exclude_end=exclude_end,
            ignore_end_delimiter=ignore_end_delimiter,
        )
    elif delimiter_matcher:
        context_factory_factory = single_delimiter_context_factory_creator(
            delimiter_matcher=delimiter_matcher,
            exclude_delimiter=True,
        )
    else:
        ap.error('Expected delimiters to be set. Use -d/-D or -s/-S and -e/-E.')

    return context_factory_factory


def build_pipeline(context_factory, args):
    """
    Builds the pipeline to execute for the context_factory and all of the arguments.
    """

    curr = context_factory

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

    return curr


def construct_arg_parser():
    from . import __doc__

    ap = argparse.ArgumentParser(
        description=__doc__
    )
    ap.add_argument('-d', '--delimiter-text', help="delimiter text", dest='delimiter_matcher', type=ContainsTextMatcher)
    ap.add_argument('-D', '--delimiter-regex', help="delimiter regex", dest='delimiter_matcher', type=RegexMatcher)

    ap.add_argument('-s', '--delimiter-start-text', help="delimiter start text", dest='start_delimiter_matcher',
                    type=ContainsTextMatcher)
    ap.add_argument('-S', '--delimiter-start-regex', help='delimiter start regex', dest='start_delimiter_matcher',
                    type=RegexMatcher)
    ap.add_argument('-e', '--delimiter-end-text', help='delimiter end text', dest='end_delimiter_matcher',
                    type=ContainsTextMatcher)
    ap.add_argument('-E', '--delimiter-end-regex', help='delimiter end regex', dest='end_delimiter_matcher',
                    type=RegexMatcher)

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
                    help='display only contexts that have line(s) that exactly match this text', action='append',
                    default=[])
    ap.add_argument('-M', '--matches-regex',
                    help='display only contexts that have line(s) that exactly match this regex', action='append',
                    default=[])

    ap.add_argument('-c!', '--not-contains-text',
                    help="display only contexts that have line(s) that don't contain this text", action='append',
                    default=[])
    ap.add_argument('-C!', '--not-contains-regex',
                    help="display only contexts that have line(s) that don't contain this regex", action='append',
                    default=[])
    ap.add_argument('-m!', '--not-matches-text',
                    help="display only contexts that have line(s) that don't exactly match this text", action='append',
                    default=[])
    ap.add_argument('-M!', '--not-matches-regex',
                    help="display only contexts that have line(s) that don't exactly match this regex", action='append',
                    default=[])

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
    ap.add_argument('files', nargs='*', type=argparse.FileType('r'), default=[sys.stdin])

    return ap


def main(argv):
    """
    Main method.
    """

    ap = construct_arg_parser()
    args = ap.parse_args(argv[1:])
    context_factory_factory = get_context_factory_from_args(ap, args)

    first = True
    for file in args.files:
        context_factory = context_factory_factory(file)
        pipeline = build_pipeline(context_factory, args)

        for context in pipeline:
            if not first and args.output_delimiter:
                sys.stdout.write(args.output_delimiter)
                sys.stdout.write('\n')
            first = False

            text = str(context)
            sys.stdout.write(text)
            if not text.endswith('\n'):
                sys.stdout.write('\n')
            sys.stdout.flush()

    return 0
