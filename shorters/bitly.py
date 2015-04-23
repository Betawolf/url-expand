import logging
import base64
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from shorters.shorters import ShortenerService

class BitlyShortenerService(ShortenerService):

  auth_page = 'https://bitly.com/a/oauth_apps'
  name = 'bit.ly'

  api_root = 'https://api-ssl.bitly.com'
  api_url = api_root + '/v3/expand'
  auth_url = 'https://api-ssl.bitly.com/oauth/access_token'
  
  def __init__(self,username,password,client_id,client_secret):
    
    auth_str = base64.b64encode((username + ':' + password).encode('utf-8'))
    r = Request(self.auth_url,data=urlencode({'client_id':client_id,'client_secret':client_secret}).encode('utf-8'),headers={'Authorization':'Basic '.encode('utf-8')+auth_str})
    ret = urlopen(r).read().decode('utf-8')
    if ret and 'status_code' in ret and ret['status_code'] != 200:
      raise ValueError("bit.ly: error code {} : {} when trying to gain an access token.".format(ret['status_code'],ret['status_txt']))
      
    self.access_token = ret

  def resolve(self,url):
    req_str = self.api_url + '?' + urlencode({'access_token':self.access_token, 'shortUrl':url})
    ret = self.get(req_str)
    if ret and 'data' in ret and 'expand' in ret['data'] and 'long_url' in ret['data']['expand'][0]:
      return ret['data']['expand'][0]['long_url']
    elif ret and 'status_code' in ret and ret['status_code'] != 200:
      logging.warn("JSON reports error code {} : {} for request {}".format(ret['status_code'],ret['status_txt'],req_str))
    else:
      logging.warn('Could not find result in response for `{}`'.format(url))
    return None

