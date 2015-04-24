import json 
import base64
from transforms import URLTransform
from urllib.parse import urlencode
from urllib.request import urlopen,Request


class URLShortener(URLTransform):

  keyword = 'shorten'

  api_root = 'https://api-ssl.bitly.com'
  api_url = api_root + '/v3/shorten'
  auth_url = api_root + '/oauth/access_token'
  
  def __init__(self,username,password,client_id,client_secret):
    
    data = urlencode({'client_id':client_id,'client_secret':client_secret}).encode('utf-8')
    req = Request(self.auth_url,data)

    auth_str = base64.b64encode((username + ':' + password).encode('utf-8'))
    req.add_headers=('Authorization','Basic '.encode('utf-8')+auth_str)
    ret = urlopen(r).read().decode('utf-8')
    if ret and 'status_code' in ret and ret['status_code'] != 200:
      raise ValueError("bit.ly: error code {} : {} when trying to gain an access token.".format(ret['status_code'],ret['status_txt']))
    self.access_token = ret
    super().__init__()

  @staticmethod
  def shorten(url,domain='bit.ly'):
    params = {'access_token':access_token,
              'domain':domain,
              'format':'json',
              'longUrl':url} 
    req_str = URLShortener.api_url + '?' + urlencode(params)
    ret = None
    try:
      req = urlopen(req_str)
      response = req.read()
      obj = json.loads(response.decode('utf-8'))
      if obj and 'data' in obj and 'expand' in obj['data'] and 'url' in obj['data']['expand'][0]:
        ret = obj['data']['expand'][0]['url']
      elif ret and 'status_code' in ret and ret['status_code'] != 200:
        logging.warn("JSON reports error code {} : {} for request {}".format(ret['status_code'],ret['status_txt'],req_str))
      else:
        logging.warn('Could not find result in response for `{}`'.format(url))
    except Exception as e:
      logging.warn('Error retrieving URL `{}` in class `{}`:\n{}'.format(req_str,self.__class__.__name__, e))
    return ret

  def supports(self,url):
    return True

  def inner_transform(self,url):
    return URLShortener.shorten(url) 
