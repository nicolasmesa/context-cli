# Context Cli

[![Build Status](https://travis-ci.org/nicolasmesa/context-cli.svg?branch=master)](https://travis-ci.org/nicolasmesa/context-cli)
[![Coverage](https://coveralls.io/repos/github/nicolasmesa/context-cli/badge.svg?branch=master)](https://coveralls.io/github/nicolasmesa/context-cli?branch=development)

Context Cli is a cli tool to search with contexts.


## Installation

```
$ pip install context-cli
```

## Usage

### Help

```
$ ctx -h
usage: ctx [-h] [-t TYPE] [-w] [-d DELIMITER_MATCHER]
                   [-D DELIMITER_MATCHER] [-s START_DELIMITER_MATCHER]
                   [-S START_DELIMITER_MATCHER] [-e END_DELIMITER_MATCHER]
                   [-E END_DELIMITER_MATCHER] [-x] [-X] [-i]
                   [-c CONTAINS_TEXT] [-C CONTAINS_REGEX] [-m MATCHES_TEXT]
                   [-M MATCHES_REGEX] [-c! NOT_CONTAINS_TEXT]
                   [-C! NOT_CONTAINS_REGEX] [-m! NOT_MATCHES_TEXT]
                   [-M! NOT_MATCHES_REGEX] [-l LINE_CONTAINS_TEXT]
                   [-L LINE_CONTAINS_REGEX] [-l! NOT_LINE_CONTAINS_TEXT]
                   [-L! NOT_LINE_CONTAINS_REGEX] [-o OUTPUT_DELIMITER]
                   [files [files ...]]

A cli tool to search with contexts.

positional arguments:
  files

optional arguments:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  type of search as specified in .ctxrc
  -w, --write           write the current context search to .ctxrc
  -d DELIMITER_MATCHER, --delimiter-text DELIMITER_MATCHER
                        delimiter text
  -D DELIMITER_MATCHER, --delimiter-regex DELIMITER_MATCHER
                        delimiter regex
  -s START_DELIMITER_MATCHER, --delimiter-start-text START_DELIMITER_MATCHER
                        delimiter start text
  -S START_DELIMITER_MATCHER, --delimiter-start-regex START_DELIMITER_MATCHER
                        delimiter start regex
  -e END_DELIMITER_MATCHER, --delimiter-end-text END_DELIMITER_MATCHER
                        delimiter end text
  -E END_DELIMITER_MATCHER, --delimiter-end-regex END_DELIMITER_MATCHER
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


### Save common arguments

If you use `ctx` with the same arguments over and over again, you can save those arguments under a name. In
the following example, we add `my_saved_search` by using the `--type` (or `-t`) and `--write` (or `-w`).

```
$ ctx --type my_saved_search -write -xXi -s '-----' -e 'end' -o '=========='
```

And then use it (note there is no `--write` anymore)

```
$ ctx -t my_saved_search my_file.txt
```

The configuration is saved to your home folder in a `.ctxrc` file.


TODO: Add more examples
