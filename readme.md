# url-expand

The aim of url-expand is to automatically replace URLs which have been shortened by URL shortening services with their expanded counterparts. In many web-mining applications, knowing the original URL can be valuable.

There is a command-line interface, which supports piping:

```
usage: urlexpand.py [-h] [--errors [ERRORS]] transformer [infile] [outfile]

Transform URLs in-place.

positional arguments:
  transformer           The transform to apply, one of: expand shorten
  infile                The input file containing text with shortened URLs.
                        Default is STDIN.
  outfile               Writeable output file. Default is STDOUT.

optional arguments:
  -h, --help            show this help message and exit
  --errors [ERRORS], -e [ERRORS]
                        Logfile for warnings. Default is STDERR.

```

There is a programmatic interface:

```{python}
import transforms.expander
e = transforms.expander.URLExpander() 
e.transform('http://bit.ly/1RmnUT')
# 'http://google.com'
e.transform_in_place("I just went to http://bit.ly/1RmnUT.")
#'I just went to http://google.com.'
```

Currently there are two transforms:

+ `expander` uses [LongURL](http://longurl.org/) to expand a shortened URL to its original.
+ `shortner` uses [bit.ly](http://dev.bitly.com/) to shorten a URL. (This is not set up for the CLI's use just yet.)
