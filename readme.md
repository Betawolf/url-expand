# url-expand

The aim of url-expand is to automatically replace URLs which have been shortened by URL shortening services with their expanded counterparts. In many web-mining applications, knowing the original URL can be valuable.

There is a command-line interface, which supports piping:

```
usage: urlexpand.py [-h] [--outfile [OUTFILE]] [--errors [ERRORS]]
                    [--config CONFIG]
                    [infile]

Expand shortened URLs in-place.


positional arguments:
  infile                The input file containing text with shortened URLs.
                        Default is STDIN.

optional arguments:
  -h, --help            show this help message and exit
  --outfile [OUTFILE], -o [OUTFILE]
                        Writeable output file. Default is STDOUT.
  --errors [ERRORS], -e [ERRORS]
                        Logfile for warnings. Default is STDERR.
  --config CONFIG, -c CONFIG
                        A configuration file for initialising non-default
                        shorters, of the form <name> <args>
```

There is a programmatic interface:

```{python}
import urlexpand
shorteners = urlexpand.shorters.from_config(open('config','r'))
e = urlexpand.Expander(shorteners) 
e.expand('http://bit.ly/1RmnUT')
# 'http://google.com'
e.expand_in_place("I just went to http://google.com.")
#'I just went to http://google.com.'
```

There is also a convenient API which makes use of any services which don't require a user configuration.

```{python}
import urlexpand
urlexpand.expand_in_place("Go to http://bit.ly/1RmnUT if you dare.")
#"Go to http://bit.ly/1RmnUT if you dare."
```

Unfortunately, the only service currently implemented is `bit.ly`, which requires you to configure API access details.
