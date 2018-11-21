from mock import patch, mock

from context_cli.core import (
    start_and_end_delimiter_context_factory_creator, single_delimiter_context_factory_creator,
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
