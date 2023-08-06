# dblpct

The % in the string given as the first argument is doubled and output to stdout.

## install

```
# pip install dblpct
```


## how to use

ex)
```
 # dblpct https%3A%2F%2Fwww.%E3%83%86%E3%82%B9%E3%83%88URL.com
https%%3A%%2F%%2Fwww.%%E3%%83%%86%%E3%%82%%B9%%E3%%83%%88URL.com
```

## Caution

Special characters in bash, etc. are not escaped. They will be interpreted as a command line string when entered.

ex)
```
 # dblpct FJWRF%)faw
-bash: syntax error near unexpected token `)'
```
