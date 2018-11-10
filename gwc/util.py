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


def build_regexp_if_needed(maybe_regexp):
    if isinstance(maybe_regexp, str):
        return re.compile(maybe_regexp)
    return maybe_regexp
