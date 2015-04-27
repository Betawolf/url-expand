import re
import os
import time
import inspect

url_regex = re.compile("https?://[^ \n\r\t]+")

def extract_urls(text):
  return url_regex.findall(text)


def all_transforms():
  all_s = {}
  import transforms
  for pyfile in os.listdir(os.path.dirname(transforms.__file__)):
    if pyfile.find('.') < 1:
      continue
    bname,ext = pyfile.split('.')
    if ext == 'py' and bname != '__init__':
      mod = __import__(transforms.__name__+'.'+bname)
      mod = getattr(mod,bname)
      classes = inspect.getmembers(mod,lambda thing : inspect.isclass(thing) and thing != URLTransform and issubclass(thing,URLTransform))
      if classes:
        for name, cls in classes:
          all_s[cls.keyword] = cls
  return all_s


class URLTransform:
  
  keyword = 'undefined'

  def __init__(self):
    self.url_map = {}


  def transform_in_place(self,text,rush=False):
    """ Given an input text, return a version of the text with
    the URLs replaced with their transformed versions.
    
    :param str text: A piece of text containing URLs to be expanded.
    :param list shorteners: A list of usable ShortenerService objects.
    :param Boolean rush: Set to true to disregard inbuilt rate limits.
    :return: The modified string. """
    urls = extract_urls(text)
    subs = transform_all(urls,rush)
    for url, sub in zip(urls,subs):
      if sub:
        text = text.replace(url,sub)
    return text


  def transform(self,url):
    """ Applies a transform to the URL specified.
    Acts as a caching wrapper to inner_transform,
    which is the method which should normally be
    overridden, not this one. Checks with supports()
    before calling. 
  
    :param str url: The url to transform. 
    :return: The result of calling self.inner_transform(url), or the cached version."""
    if url not in self.url_map:
      if self.supports(url):
          self.url_map[url] = self.inner_transform(url)
      if url not in self.url_map:
        self.url_map[url] = None
    return self.url_map[url]


  def transform_all(self, urls, rush=False):
    """ Applies a transform to all of the listed
    URLs which are supported, returning a list of the results.
    Uses inbuilt rate limiting by default.

    :param list urls: A list of URL strings to be potentially
    :param Boolean rush: Set to true to disregard inbuilt rate limits.
    :return: A list corresponding to the input, of either URL strings or Nones.
    """
    returnlist = []
    for url in urls:
      returnlist.append(self.transform(url))
      time.sleep(self.delay)
    return returnlist


  def supports(self, url):
    raise NotImplementedError("{}.supports(url) has not yet been implemented.".format(self.__class__.__name__))    
    

  def inner_transform(self,url):
    raise NotImplementedError("{}.inner_transform(url) has not yet been implemented.".format(self.__class__.__name__))    
