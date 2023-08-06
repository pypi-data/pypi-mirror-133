# nevArgs

It's a simple package that using shlex formats your cli-like argument strings and format them into a dict

```py
>>> import nevargs
>>> s = "this is -f True fun -c command"
>>> nevargs.dictify(s)
{'bin': ['-f'], '-f': ['True', 'command'], 'no': ['this', 'is', 'fun']}
```
