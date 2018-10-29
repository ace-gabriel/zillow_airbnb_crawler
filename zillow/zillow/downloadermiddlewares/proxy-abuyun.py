import base64


class ProxyMiddleware(object):


  def __init__(self,settings):
    self.proxy_info = settings['CONFIG']['abuyun_proxy']

  @classmethod
  def from_crawler(cls, crawler):  
    settings = crawler.settings
    o = cls(settings)
    o.crawler=crawler
    return o

  def process_request(self, request, spider):
    proxyUser = self.proxy_info['proxyUser']
    proxyPass = self.proxy_info['proxyPass']
    proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

    request.meta['proxy'] = "http://{}:{}".format(self.proxy_info['proxyHost'],self.proxy_info['proxyPort'])
    request.headers['Proxy-Authorization'] = proxyAuth

