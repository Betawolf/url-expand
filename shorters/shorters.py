import os
import json
import time
import logging
import inspect
from urllib.request import urlopen
from urllib.parse import urlparse

defaults = []

def all_shorters():
  all_s = []
  import shorters
  for pyfile in os.listdir(os.path.dirname(shorters.__file__)):
    if pyfile.find('.') < 1:
      continue
    bname,ext = pyfile.split('.')
    if ext == 'py' and bname not in ['__init__','shorters']:
      mod = __import__(shorters.__name__+'.'+bname)
      mod = getattr(mod,bname)
      classes = inspect.getmembers(mod,lambda thing : inspect.isclass(thing) and thing != ShortenerService and issubclass(thing,ShortenerService))
      if classes:
        for name, cls in classes:
          all_s.append(cls)
  return all_s

def from_config(config_file):
  configured_s = []
  shorter_classes = all_shorters()
  class_dict = {}
  for cls in shorter_classes:
    if cls.name:
      class_dict[cls.name] = cls
  line_no = 1
  for line in config_file:
    args = None
    if line.find(' ') < 0:
      name = line
    else:
      name, argstr = line.split(' ',1)
      args = [a.strip('\n\r') for a in argstr.split(' ')]
    if name != 'defaults' and name not in class_dict:
      raise ValueError('Unknown configuration option `{}` set at line {}.'.format(name,line_no))
    elif name == 'defaults' and 'true' in args:
      configured_s += defaults
    elif name in class_dict:
      cls = class_dict[name]
      if args:
        configured_s.append(cls(*args))
      else:
        configured_s.append(cls())
    line_no += 1
  return configured_s 

class ShortenerService:

  auth_page = None
  name = None
  api_delay = 0

  def ownsURL(self,url):
    return urlparse(url).netloc == self.name

  def resolve(self,url):
    raise NotImplementedError("'resolve()' has not been implemented for class `{}`".format(__class__.__name__))

  def resolve_many(self,urls):
    """ The default method for resolving a list of URLs.
    Just calls resolve() in sequence. A sane subclass 
    will override this. 

    :params list urls: A list of str URLs, all of which belong to this shorter.
    :return: A list of expanded str URLs or Nones, the order corresponding to the input. """
    resolved = []
    for url in urls:
      resolved.append(self.resolve(url))
      time.sleep(self.api_delay)      
    return resolved

  def get(self,req_str):
    ret = None
    try:
      req = urlopen(req_str)
      response = req.read()
      ret = json.loads(response.decode('utf-8'))
    except Exception as e:
      logging.warn('Error retrieving URL `{}` in class `{}`:\n{}'.format(req_str,self.__class__.__name__, e))
    return ret
