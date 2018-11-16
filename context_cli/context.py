import logging
from abc import ABC, abstractmethod
from collections import deque

logger = logging.getLogger(__name__)


class Context:
    """
    Class that encapsulates a context. A context is a collection of lines that exist within a set of delimiters.
    """

    def __init__(self, lines):
        self._lines = lines

    @property
    def lines(self):
        return self._lines

    def __str__(self):
        return '\n'.join(self.lines)


class FileIterator:
    """
    Iterator to read a file that provides the ability to unread lines.
    """

    def __init__(self, file):
        self.file = file
        self.queue = deque()

    def __iter__(self):
        while True:
            if len(self.queue):
                yield self.queue.popleft()
                continue

            line = self.file.readline()
            if line == '':
                break

            yield line.rstrip('\n')

    def unread(self, line):
        self.queue.append(line)


class ContextFactoryBase(ABC):
    """
    Abstract ContextFactoryBase class.
    """

    def __init__(self, file):
        self.file_iterator = FileIterator(file)

    @abstractmethod
    def __iter__(self):
        pass


class SingleDelimiterContextFactory(ContextFactoryBase):
    """
    Class that creates Contexts from a file with a single delimiter.

    Example:
        file text:
            hello world
            something
            ...
            Another thing
            ....
            Last thing
        delimiter:
            "..."
        outputs:
            Context(lines=["hello world", "something"])
            Context(lines=["Another thing"])
            Context(lines=["Last thing"])
    """

    def __init__(self, file, delimiter_matcher, exclude_delimiter=True):
        super().__init__(file)
        self.delimiter_matcher = delimiter_matcher
        self.exclude_delimiter = exclude_delimiter

    def matches_delimiter(self, line):
        return self.delimiter_matcher.matches(line)

    def __iter__(self):
        context_lines = []

        # Only add delimiter if it's not the first line or if exclude_delimiter=False
        line = next(iter(self.file_iterator))
        if not (self.matches_delimiter(line) and self.exclude_delimiter):
            context_lines.append(line)

        for line in self.file_iterator:

            if self.matches_delimiter(line):
                if not self.exclude_delimiter:
                    context_lines.append(line)
                # Only yield if we actually have something to yield and it's not the first line
                if context_lines:
                    yield Context(context_lines)
                    context_lines = []
                    continue
            context_lines.append(line)

        if context_lines:
            yield Context(context_lines)


class StartAndEndDelimiterContextFactory(ContextFactoryBase):
    """
    Class that creates Contexts from a file with start and end delimiters. It's also useful to extract delimited
    text from a file.

    Example:
        file text:
            This should not be included
            ```
            this should be included
            and so should this
            ```
            This should not
        delimiter:
            "```"
        outputs:
            Context(lines=["this should be included", "and so should this"])
    """

    def __init__(self, file, start_delimiter_matcher, end_delimiter_matcher, exclude_start_delimiter=False, exclude_end_delimiter=False, ignore_end_delimiter=True,):

        super().__init__(file)
        self.start_delimiter_matcher = start_delimiter_matcher
        self.end_delimiter_matcher = end_delimiter_matcher
        self.exclude_start_delimiter = exclude_start_delimiter
        self.exclude_end_delimiter = exclude_end_delimiter
        self.ignore_end_delimiter = ignore_end_delimiter

        self.stack = deque()

    def is_start(self, line):
        return self.start_delimiter_matcher.matches(line)

    def is_end(self, line):
        return self.end_delimiter_matcher.matches(line)

    def __iter__(self):
        while True:
            start_line = self.get_next_start_line()

            if start_line is None:
                break

            context_lines = []
            if not self.exclude_start_delimiter:
                context_lines.append(start_line)

            for line in self.file_iterator:
                if line is None:
                    break
                if self.is_end(line):
                    if self.exclude_end_delimiter:
                        if not self.ignore_end_delimiter:
                            self.file_iterator.unread(line)
                    else:
                        context_lines.append(line)
                    break
                context_lines.append(line)

            yield Context(context_lines)

    def get_next_start_line(self):
        for line in self.file_iterator:
            if self.is_start(line):
                return line
        return None

