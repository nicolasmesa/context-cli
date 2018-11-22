import re
import logging

logger = logging.getLogger(__name__)


def build_regexp_if_needed(maybe_regexp):
    """
    Creates a regexp if the `maybe_regexp` is a str.
    """
    if not isinstance(maybe_regexp, str):
        return maybe_regexp
    return re.compile(maybe_regexp)

