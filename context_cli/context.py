import logging
from collections import deque

logger = logging.getLogger(__name__)


class Context:

    def __init__(self, lines):
        self._lines = lines

    @property
    def lines(self):
        return self._lines

    def __str__(self):
        return '\n'.join(self.lines)


class ContextFactory:

    def __init__(self, file, start_delimiter_matcher, end_delimiter_matcher, exclude_start_delimiter=False, exclude_end_delimiter=False, ignore_end_delimiter=True, first_line=None):

        self.file = file

        self.start_delimiter_matcher = start_delimiter_matcher
        self.end_delimiter_matcher = end_delimiter_matcher
        self.exclude_start_delimiter = exclude_start_delimiter
        self.exclude_end_delimiter = exclude_end_delimiter
        self.ignore_end_delimiter = ignore_end_delimiter

        self.delimiter_start_fn = None
        self.delimiter_end_fn = None

        self.stack = deque()

        # TODO: Hack to make it work when -d is used since we want it to start "recording" from the first line.
        if first_line is not None:
            self.stack.append(first_line)

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
                        if not self.ignore_end_delimiter:
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

