# url-morph

`url-morph` is a library of transformations which can be applied to URLs, and a tool for applying them. Each transform object implements an interface which builds up a local cache of URL mappings and handles rate limiting, allowing for simple and efficient querying.

There is a command-line interface, which supports piping:

```
usage: urlmorph-cli.py [-h] [--errors [ERRORS]] [--args [ARGS [ARGS ...]]]
                       transformer [infile] [outfile]

Transform URLs in-place.

positional arguments:
  transformer           The transform to apply, one of {shorten,expand,title}
  infile                The input file containing text with shortened URLs.
                        Default is STDIN.
  outfile               Writeable output file. Default is STDOUT.

optional arguments:
  -h, --help            show this help message and exit
  --errors [ERRORS], -e [ERRORS]
                        Logfile for warnings. Default is STDERR.
  --args [ARGS [ARGS ...]], -a [ARGS [ARGS ...]]
                        Optional arguments to pass to the selected transform.
```

There is a programmatic interface:

```{python}
import urlmorph.expander
e = urlmorph.expander.URLExpander() 
e.transform('http://bit.ly/1RmnUT')
# 'http://google.com'
e.transform_all(['http://bit.ly/1RmnUT','http://tinyurl.com/6cfcq3'])
# ['http://www.google.com/', 'https://news.ycombinator.com/'] 
e.transform_in_place("I just went to http://bit.ly/1RmnUT.")
#'I just went to http://google.com.'
```

Currently there are three transforms:

+ `expander` uses [LongURL](http://longurl.org/) to expand a shortened URL to its original. 
+ `shorten` uses [bit.ly](http://dev.bitly.com/) to shorten a URL. (Requires passing API auth information)
+ `title` replaces a URL with the title of the corresponding webpage (if available). (Currently in an uncertain state, will at best work for shortened URLs).

You can install the library by cloning this repository and using `setup.py`.

```
$ git clone https://github.com/Betawolf/url-morph
$ cd url-morph/
$ sudo python setup.py install
```

