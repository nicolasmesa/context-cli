from mock import patch, mock, ANY

from context_cli.core import (
    start_and_end_delimiter_context_factory_creator, single_delimiter_context_factory_creator,

    get_context_factory_from_args, build_pipeline, construct_arg_parser
)


@patch('context_cli.context.StartAndEndDelimiterContextFactory.__init__', return_value=None)
def test_start_and_end_delimiter_context_factory_creator(mock_init_method):
    start_delimiter_matcher = mock.MagicMock()
    end_delimiter_matcher = mock.MagicMock()
    exclude_start = False
    exclude_end = True
    ignore_end_delimiter = True
    file = mock.MagicMock()

    factory = start_and_end_delimiter_context_factory_creator(
        start_delimiter_matcher=start_delimiter_matcher,
        end_delimiter_matcher=end_delimiter_matcher,
        exclude_start=exclude_start,
        exclude_end=exclude_end,
        ignore_end_delimiter=ignore_end_delimiter,
    )

    assert callable(factory) is True

    context_factory = factory(file)

    assert context_factory is not None
    mock_init_method.assert_called_once_with(
        file,
        start_delimiter_matcher=start_delimiter_matcher,
        end_delimiter_matcher=end_delimiter_matcher,
        exclude_start_delimiter=exclude_start,
        exclude_end_delimiter=exclude_end,
        ignore_end_delimiter=ignore_end_delimiter,
    )


@patch('context_cli.context.SingleDelimiterContextFactory.__init__', return_value=None)
def test_single_delimiter_context_factory_creator(mock_init_method):
    delimiter_matcher = mock.MagicMock()
    exclude_delimiter = False
    file = mock.MagicMock()

    factory = single_delimiter_context_factory_creator(
        delimiter_matcher=delimiter_matcher,
        exclude_delimiter=exclude_delimiter,
    )

    assert callable(factory) is True

    context_factory = factory(file)

    assert context_factory is not None
    mock_init_method.assert_called_once_with(
        file,
        delimiter_matcher=delimiter_matcher,
        exclude_delimiter=exclude_delimiter,
    )


def test_get_context_factory_from_args_all_matchers_defined():
    args = mock.MagicMock()
    args.start_delimiter_matcher = mock.MagicMock()
    args.end_delimiter_matcher = mock.MagicMock()
    args.delimiter_matcher = mock.MagicMock()
    ap = mock.MagicMock()
    ap.error = mock.MagicMock()

    get_context_factory_from_args(ap, args)

    ap.error.assert_called()


def test_get_context_factory_from_args_no_matchers_defined():
    args = mock.MagicMock()
    args.start_delimiter_matcher = None
    args.end_delimiter_matcher = None
    args.delimiter_matcher = None
    ap = mock.MagicMock()
    ap.error = mock.MagicMock()

    get_context_factory_from_args(ap, args)

    ap.error.assert_called()


@patch('context_cli.core.start_and_end_delimiter_context_factory_creator', return_value=mock.MagicMock())
def test_get_context_factory_from_args_start_and_end_delimiter_matchers(factory_creator_mock):
    args = mock.MagicMock()
    args.start_delimiter_matcher = mock.MagicMock()
    args.end_delimiter_matcher = mock.MagicMock()
    args.exclude_start_delimiter = mock.MagicMock()
    args.exclude_end_delimiter = mock.MagicMock()
    args.ignore_end_delimiter = mock.MagicMock()
    ap = mock.MagicMock()

    context_factory_factory = get_context_factory_from_args(ap, args)

    assert context_factory_factory is not None
    factory_creator_mock.assert_called_once_with(
        start_delimiter_matcher=args.start_delimiter_matcher,
        end_delimiter_matcher=args.end_delimiter_matcher,
        exclude_start=args.exclude_start_delimiter,
        exclude_end=args.exclude_end_delimiter,
        ignore_end_delimiter=args.ignore_end_delimiter,
    )


@patch('context_cli.core.single_delimiter_context_factory_creator', return_value=mock.MagicMock())
def test_get_context_factory_from_args_delimiter_matchers(factory_creator_mock):
    args = mock.MagicMock()
    args.delimiter_matcher = mock.MagicMock()
    args.start_delimiter_matcher = None
    args.end_delimiter_matcher = None
    ap = mock.MagicMock()

    context_factory_factory = get_context_factory_from_args(ap, args)

    assert context_factory_factory is not None
    factory_creator_mock.assert_called_once_with(
        delimiter_matcher=args.delimiter_matcher,
        exclude_delimiter=True,
    )


@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_no_filters(not_empty_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    not_empty_filter_mock.assert_called_once_with(context_generator=context_factory)


@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_no_filters(not_empty_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    not_empty_filter_mock.assert_called_once_with(context_generator=context_factory)


@patch('context_cli.core.MatchesTextContextFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_matches_text_filter(not_empty_filter_mock, matches_text_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.matches_text = ['matches this']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    matches_text_filter_mock.assert_called_once_with(context_generator=context_factory, text=args.matches_text[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=matches_text_filter_mock.return_value)


@patch('context_cli.core.NotMatchesTextContextFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_not_matches_text_filter(not_empty_filter_mock, not_matches_text_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.not_matches_text = ['not matches this']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    not_matches_text_filter_mock.assert_called_once_with(context_generator=context_factory, text=args.not_matches_text[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=not_matches_text_filter_mock.return_value)


@patch('context_cli.core.ContainsTextContextFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_contains_text_filter(not_empty_filter_mock, contains_text_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.contains_text = ['contains this']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    contains_text_filter_mock.assert_called_once_with(context_generator=context_factory, text=args.contains_text[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=contains_text_filter_mock.return_value)


@patch('context_cli.core.NotContainsTextContextFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_not_contains_text_filter(not_empty_filter_mock, not_contains_text_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.not_contains_text = ['not contains this']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    not_contains_text_filter_mock.assert_called_once_with(context_generator=context_factory, text=args.not_contains_text[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=not_contains_text_filter_mock.return_value)


@patch('context_cli.core.MatchesRegexContextFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_matches_regex_filter(not_empty_filter_mock, matches_regex_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.matches_regex = ['regex']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    matches_regex_filter_mock.assert_called_once_with(context_generator=context_factory, regexp=args.matches_regex[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=matches_regex_filter_mock.return_value)


@patch('context_cli.core.NotMatchesRegexContextFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_not_matches_regex_filter(not_empty_filter_mock, not_matches_regex_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.not_matches_regex = ['not regex']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    not_matches_regex_filter_mock.assert_called_once_with(context_generator=context_factory, regexp=args.not_matches_regex[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=not_matches_regex_filter_mock.return_value)


@patch('context_cli.core.ContainsRegexContextFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_contains_regex_filter(not_empty_filter_mock, contains_regex_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.contains_regex = ['regex']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    contains_regex_filter_mock.assert_called_once_with(context_generator=context_factory, regexp=args.contains_regex[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=contains_regex_filter_mock.return_value)


@patch('context_cli.core.NotContainsRegexContextFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_not_contains_regex_filter(not_empty_filter_mock, not_contains_regex_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.not_contains_regex = ['not regex']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    not_contains_regex_filter_mock.assert_called_once_with(context_generator=context_factory, regexp=args.not_contains_regex[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=not_contains_regex_filter_mock.return_value)


@patch('context_cli.core.ContainsTextLineFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_contains_text_line_filter(not_empty_filter_mock, contains_text_line_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.line_contains_text = ['contains this']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    contains_text_line_filter_mock.assert_called_once_with(context_generator=context_factory, text=args.line_contains_text[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=contains_text_line_filter_mock.return_value)


@patch('context_cli.core.NotContainsTextLineFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_not_contains_text_line_filter(not_empty_filter_mock, not_contains_text_line_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.not_line_contains_text = ['not contains this']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    not_contains_text_line_filter_mock.assert_called_once_with(context_generator=context_factory, text=args.not_line_contains_text[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=not_contains_text_line_filter_mock.return_value)


@patch('context_cli.core.ContainsRegexLineFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_contains_regex_line_filter(not_empty_filter_mock, contains_regex_line_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.line_contains_regex = ['regex']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    contains_regex_line_filter_mock.assert_called_once_with(context_generator=context_factory, regexp=args.line_contains_regex[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=contains_regex_line_filter_mock.return_value)


@patch('context_cli.core.NotContainsRegexLineFilter')
@patch('context_cli.core.NotEmptyContextFilter')
def test_build_pipeline_not_contains_regex_line_filter(not_empty_filter_mock, not_contains_regex_line_filter_mock):
    context_factory = mock.MagicMock()
    args = mock.MagicMock()
    args.not_line_contains_regex = ['not regex']

    pipeline = build_pipeline(context_factory, args)
    assert not_empty_filter_mock.return_value is pipeline
    not_contains_regex_line_filter_mock.assert_called_once_with(context_generator=context_factory, regexp=args.not_line_contains_regex[0])
    not_empty_filter_mock.assert_called_once_with(context_generator=not_contains_regex_line_filter_mock.return_value)


def test_construct_arg_parser():
    ap = construct_arg_parser()
    assert ap is not None