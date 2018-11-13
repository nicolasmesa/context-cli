import re
import logging
from functools import wraps


logger = logging.getLogger(__name__)

def tracer(func):
    logger = logging.getLogger(func.__module__)

    @wraps(func)
    def wrap(*args, **kwargs):
        logger.debug("call: %s(%s, %s)", func.__name__, args[1:], kwargs)
        result = func(*args, **kwargs)
        logger.debug("result: %s=%s", func.__name__, result)
        return result

    return wrap


def build_regexp_if_needed(maybe_regexp, match_start_and_end=False):
    """
    Creates a regexp if the `maybe_regexp` is a str. If `match_start_and_end` is True, it prepends '^' and appends '$'
    if they are not there already.
    """
    if not isinstance(maybe_regexp, str):
        return maybe_regexp
    elif match_start_and_end:
        # TODO: Maybe using fullmatch(line) would help avoid this
        if not maybe_regexp.startswith('^'):
            maybe_regexp = '^' + maybe_regexp
        if not maybe_regexp.endswith('$'):
            maybe_regexp = maybe_regexp + '$'
    return re.compile(maybe_regexp)

