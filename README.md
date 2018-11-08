# Grep With Context

A command-line argument to make contextual greps


```
$ gwc --context-delimiter "my-delimiter" --contains-text "hello world" --not-contains-text "bye world" --contains-regex "20[0-9]{2}" my_file.txt
```


```
$ gwc --context-start-delimiter "my-start-delimiter" --context-end-delimiter "my-end-delimiter" --contains-text "blah" --contains-text "something else" my_file.txt
```

```
$ gwc --context-text "hello" --lines-before 5 --lines-after 2 --contains-text "world" my_file.txt
```

```
$ gwc --context-regex "20[0-9]{2}" --lines-before 5 --lines-after 2 --contains-text "world" my_file.txt
```

```
$ gwc --context-text "hello" --lines-before 5 --lines-after 2 --contains-text "world" my_file.txt
```

## Samples

```
 python cli.py -S "^class.*" -Ex "^[a-zA-Z].*" -c "def matches" -c "Matcher" -o="------------------" cli.py
```

## TODO

### Compare these

```
 python cli.py -sx "\`\`\`" -ex "\`\`\`" -o="--------------------" ../blog/blog/content/posts/saas-like-isolation-in-django-rest-framework.md

 python cli.py -S "^class.*" -Ex "^[a-zA-Z].*" -c "def matches" -c "Matcher" -o="------------------" cli.py
```

The `_.push` conflicts here.

## Open questions

* What should happen if the same text is found twice when doing `--context-regex`? Should it display the results "twice"? Consider the following text:

```
hello world!
My name is Nicolas
I like to say hello
And good bye
And something else
```

Running the following command:

```
$ gwc --context-regex "hello" --lines-after 3
```

Would match "hello" twice. It could output the thing twice like this:

```
hello world!
My name is Nicolas
I like to say hello

I like to say hello
And good bye
And something else
```

Or it could simply return the first one.

* `-i` to be able to do case-insensitive search

* Should be support highlighting?
* We should have a way of outputting a count instead (although it could be done as follows:
    * `expr $(gwc --delimiter "-----" -c "hello" -o "delimiter" | grep "delimiter" | wc -l) + 1`
* Handle sigpipe
* There should be a way to skip the delimiter or to not include the delimiter in the current Context and use it in the next
