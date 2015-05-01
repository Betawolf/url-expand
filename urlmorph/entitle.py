import urlmorph.expander as expander

class URLTitler(expander.URLExpander):
  
  application_name = 'url-titler'
  keyword = 'title'

  def __init__(self,quotechars=['(',')'],useragent=None):
    self.quotechars = quotechars
    super().__init__(useragent if useragent else None)

  def inner_transform(self,url):
    result = expander.expand_url(url,options=['title'])
    if result and 'long-url' in result:
      if len(self.quotechars) == 2:
        return self.quotechars[0]+result['long-url']+self.quotechars[1]
      elif len(self.quotechars) == 1:
        return self.quotechars[0]+result['long-url']+self.quotechars[0]
      else:
        return result['long-url']
    else:
      return None 
