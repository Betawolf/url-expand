import json
import time
import logging
from transforms import URLTransform
from urllib.request import urlopen,Request
from urllib.parse import urlencode,urlparse


services_url = 'http://api.longurl.org/v2/services'
expander_url = 'http://api.longurl.org/v2/expand'


def make_request(url,useragent):
  val = None
  try:
    req = Request(url)
    req.add_header('user_agent',useragent)
    ret = urlopen(req).read()
    val = json.loads(ret.decode('utf-8'))
  except Exception as e:
    logging.warn("Error making request `{}`".format(url))
    logging.warn(e)
  return val


def get_services(useragent=None):
  params={'format':'json'}
  url = services_url + '?' + urlencode(params)
  val = make_request(url,useragent)
  return val.keys() 


def expand_url(url, useragent=None, options=[]):
  params={'format':'json',
          'url':url}
  for o in options:
    params[o] = 1
  url = expander_url + '?' + urlencode(params)
  val = make_request(url,useragent)
  return val


class URLExpander(URLTransform):

  application_name = 'url-expander'
  version = 0.2
  keyword = 'expand'
  delay = 1


  def __init__(self,useragent=None):
    self.useragent = useragent if useragent else '{}/{}'.format(URLExpander.application_name,URLExpander.version)
    self.supported = get_services(self.useragent)
    super().__init__()


  def supports(self,url):
    domain = urlparse(url).netloc
    return domain in self.supported


  def inner_transform(self,url):
    result = expand_url(url,useragent=self.useragent)
    if result and 'long-url' in result:
      return result['long-url']
    else:
      return None
