import re
import sys
import logging
import argparse
import shorters.shorters as shorters

class Expander:

  def __init__(self,shorteners=shorters.defaults):
    self.url_map = {}
    self.shorteners = shorteners

  def expand_in_place(self,text):
    """ Given an input text, return a version of the text with
    the URLs replaced with their expanded versions.
    
    :param str text: A piece of text containing URLs to be expanded.
    :param list shorteners: A list of usable ShortenerService objects.
    :return: The modified string. """
    urls = extract_urls(text)
    for url in urls:
      sub = self.expand(url)
      if sub:
        text = text.replace(url,sub)
    return text
  

  def expand(self,url):
    """ Look up a URL and return its expanded
    version, or None if no expansion exists in this
    expander's set of shorteners. 

    :param str url: A URL string.
    :return: A dictionary mapping the url inputs to their long versions. """
    if url not in self.url_map:
      for shortener in self.shorteners:
        if shortener.ownsURL(url):
          self.url_map[url] = shortener.resolve(url)
          break
      if url not in self.url_map:
        self.url_map[url] = None
    return self.url_map[url]


url_regex = re.compile("https?://[^ \n\r\t]+")
default_expander = Expander()

def extract_urls(text):
  return url_regex.findall(text)

def expand_in_place(text):
  return default_expander.expand_in_place(text)
  
def expand(url):
  return default_expander.expand(url)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Expand shortened URLs in-place.')
  parser.add_argument('infile',nargs='?',help='The input file containing text with shortened URLs. Default is STDIN.',default=sys.stdin,type=argparse.FileType('r'))
  parser.add_argument('--outfile','-o',nargs='?',help='Writeable output file. Default is STDOUT. ',default=sys.stdout,type=argparse.FileType('w'))
  parser.add_argument('--errors', '-e',nargs='?',help='Logfile for warnings. Default is STDERR.',default=sys.stderr,type=argparse.FileType('w'))
  parser.add_argument('--config', '-c',help='A configuration file for initialising non-default shorters.',type=argparse.FileType('r'))
  args = parser.parse_args()

  if not args.config:
    logging.info("Using default shorter set.")
    for line in args.infile:
      args.outfile.write(expand_in_place(line))
  else:
    shorteners = shorters.from_config(args.config)
    e = Expander(shorteners)
    for line in args.infile:
      args.outfile.write(e.expand_in_place(line))
