# Context Cli

[![Build Status](https://travis-ci.org/nicolasmesa/context-cli.svg?branch=master)](https://travis-ci.org/nicolasmesa/context-cli)

Context Cli is a cli tool to search with contexts.


## Installation

```
$ pip install context-cli
```

## Usage

### Help

```
$ ctx -h
usage: ctx [-h] [-d DELIMITER_TEXT] [-D DELIMITER_REGEX]
                   [-s DELIMITER_START_TEXT] [-S DELIMITER_START_REGEX]
                   [-e DELIMITER_END_TEXT] [-E DELIMITER_END_REGEX] [-x] [-X]
                   [-i] [-c CONTAINS_TEXT] [-C CONTAINS_REGEX]
                   [-m MATCHES_TEXT] [-M MATCHES_REGEX]
                   [-c! NOT_CONTAINS_TEXT] [-C! NOT_CONTAINS_REGEX]
                   [-m! NOT_MATCHES_TEXT] [-M! NOT_MATCHES_REGEX]
                   [-l LINE_CONTAINS_TEXT] [-L LINE_CONTAINS_REGEX]
                   [-l! NOT_LINE_CONTAINS_TEXT] [-L! NOT_LINE_CONTAINS_REGEX]
                   [-o OUTPUT_DELIMITER]
                   [files [files ...]]

A cli tool to search with contexts.

positional arguments:
  files

optional arguments:
  -h, --help            show this help message and exit
  -d DELIMITER_TEXT, --delimiter-text DELIMITER_TEXT
                        delimiter text
  -D DELIMITER_REGEX, --delimiter-regex DELIMITER_REGEX
                        delimiter regex
  -s DELIMITER_START_TEXT, --delimiter-start-text DELIMITER_START_TEXT
                        delimiter start text
  -S DELIMITER_START_REGEX, --delimiter-start-regex DELIMITER_START_REGEX
                        delimiter start regex
  -e DELIMITER_END_TEXT, --delimiter-end-text DELIMITER_END_TEXT
                        delimiter end text
  -E DELIMITER_END_REGEX, --delimiter-end-regex DELIMITER_END_REGEX
                        delimiter end regex
  -x, --exclude-start-delimiter
                        exclude start delimiter from the context
  -X, --exclude-end-delimiter
                        exclude end delimiter from the context
  -i, --ignore-end-delimiter
                        prevent end delimiter from being considered as a start
                        delimiter (only applies if -X is used)
  -c CONTAINS_TEXT, --contains-text CONTAINS_TEXT
                        display only contexts that have line(s) that contain
                        this text
  -C CONTAINS_REGEX, --contains-regex CONTAINS_REGEX
                        display only contexts that have line(s) that contain
                        this regex
  -m MATCHES_TEXT, --matches-text MATCHES_TEXT
                        display only contexts that have line(s) that exactly
                        match this text
  -M MATCHES_REGEX, --matches-regex MATCHES_REGEX
                        display only contexts that have line(s) that exactly
                        match this regex
  -c! NOT_CONTAINS_TEXT, --not-contains-text NOT_CONTAINS_TEXT
                        display only contexts that have line(s) that don't
                        contain this text
  -C! NOT_CONTAINS_REGEX, --not-contains-regex NOT_CONTAINS_REGEX
                        display only contexts that have line(s) that don't
                        contain this regex
  -m! NOT_MATCHES_TEXT, --not-matches-text NOT_MATCHES_TEXT
                        display only contexts that have line(s) that don't
                        exactly match this text
  -M! NOT_MATCHES_REGEX, --not-matches-regex NOT_MATCHES_REGEX
                        display only contexts that have line(s) that don't
                        exactly match this regex
  -l LINE_CONTAINS_TEXT, --line-contains-text LINE_CONTAINS_TEXT
                        display only lines in the context that contain this
                        text
  -L LINE_CONTAINS_REGEX, --line-contains-regex LINE_CONTAINS_REGEX
                        display only lines in the context that contain this
                        regex
  -l! NOT_LINE_CONTAINS_TEXT, --not-line-contains-text NOT_LINE_CONTAINS_TEXT
                        display only lines in the context that don't contain
                        this text
  -L! NOT_LINE_CONTAINS_REGEX, --not-line-contains-regex NOT_LINE_CONTAINS_REGEX
                        display only lines in the context that don't contain
                        this regex
  -o OUTPUT_DELIMITER, --output-delimiter OUTPUT_DELIMITER
                        Output delimiter
```

## Examples

### Extracting code blocks from Markdown

```
$ ctx -xXi -S '^```$' -E '^```$' -o "========" README.md
```

This command excludes the start and ending tick blocks from the output. We need the `-i` to avoid the ticks that cose the code-block from being interpreted as the opening ticks.
The `-o` adds the "========" between each context.

### Filter the output

### Only display contexts that have "install"

```
$ ctx -xXi -S '^```$' -E '^```$' -c install -o "========" README.md
```


TODO: Add more examples
