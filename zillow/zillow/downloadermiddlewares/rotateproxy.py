import logging
import pymongo
import random
from six.moves.urllib.parse import urljoin
from urllib.parse import urlparse
from six.moves.urllib.parse import urlsplit
from w3lib.url import safe_url_string
from twisted.web._newclient import ResponseNeverReceived,ParseError
from twisted.internet.error import TimeoutError,ConnectionRefusedError, ConnectError,ConnectionLost,TCPTimedOutError,ConnectBindError
from scrapy.utils.response import response_status_message
from scrapy.exceptions import IgnoreRequest
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

from twisted.internet import task
from scrapy import signals
import math

from .agent_proxy import Agent


logger = logging.getLogger(__name__)

class ProxyMiddleware(object):
  """ Customized Proxy Middleware
      No matter success or fail, change proxy for every request 
  """
  # Change another proxy instead of passing to RetryMiddlewares when met these errors
  DONT_RETRY_ERRORS = (TimeoutError,ConnectionRefusedError,TCPTimedOutError,
                      ResponseNeverReceived, ConnectError, ConnectBindError, TunnelError)

  agent_list = []

  def __init__(self,settings):
    self.client = pymongo.MongoClient(settings['MONGO_PROXY_HOST'])
    self.db = self.client[settings['MONGO_PROXY_DB']]
    self.mongo_collection = self.db[settings['MONGO_PROXY_COLLECTION']]

  @classmethod
  def from_crawler(cls, crawler):  
    settings = crawler.settings
    o = cls(settings)
    crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
    crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
    return o

  def readProxyfile(self):
    logger.debug("Starting getting fresh proxies")
    # fetch _id value
    for document in self.mongo_collection.find():
      agent = Agent(document['_id'])
      if agent not in self.agent_list:
        self.agent_list.append(agent)

  def maintaining_agent(self):
    """ if available agent number is below some level such as 80, we fill up the agent list
    """
    # remove invalid
    self.agent_list = list(filter(lambda x: x.is_valid(),self.agent_list))

    # handle increasing size problem- max size = 500
    max_proxy_size = 300
    if len(self.agent_list)>max_proxy_size:
      logger.debug("Proxy list is too big, here cuts the low part")
      sortedagentlist = sorted(self.agent_list, key = lambda i: i.percentage)
      self.agent_list = sortedagentlist[len(self.agent_list)-max_proxy_size:]

    # add more proxy into pool
    self.readProxyfile()

  def get_proxy_slot(self, proxy):
    """
    Return downloader slot for a proxy.
    By default it doesn't take port in account, i.e. all proxies with
    the same hostname / ip address share the same slot.
    """
    return urlsplit(proxy).hostname

  def process_request(self, request, spider):
    """ Make request with agent
    """
    request.meta['agent'] = random.choice(list(filter(lambda x: x.is_valid(),self.agent_list)))
    request.meta['proxy'] = request.meta['agent'].proxy
    request.meta['download_slot'] = self.get_proxy_slot(request.meta['proxy'])
    logger.debug("Request %(request)s using proxy:%(proxy)s",
                    {'request':request, 'proxy':request.meta['proxy']})

  def _new_request_from_response(self,request):
    new_request = request.copy() 
    new_request.dont_filter = True
    return new_request

  def process_response(self, request, response, spider):
    """ Check response status and other validation info to decide whether to change a proxy or not
    """
    agent = request.meta.get('agent')
    reason = response_status_message(response.status)
    if response.status == 200:
      if response.body:     # sometimes empty return page but with 200 code
        logger.debug("Good proxy:{} for processing {}".format(request.meta['proxy'],response))
        agent.stronger()
      else:
        logger.debug("Fake  proxy:{} for processing {}".format(request.meta['proxy'],response))
        agent.weaken()  
        return self._new_request_from_response(request)           
      return response

    elif response.status ==403:
      agent.set_invalid()
      logger.info("Proxy: {} meet {} ".format(agent.proxy,reason))
      return self._new_request_from_response(request)

    return response

  def process_exception(self, request, exception, spider):
    """Handle some connection error, make another request when these error happens
    """        
    agent = request.meta.get('agent')
    for i in range(2):
      agent.weaken()
    if isinstance(exception,self.DONT_RETRY_ERRORS):
      logger.debug("Normal exception happened proxy:{} for processing {}".format(request.meta['proxy'],request.url))
      agent.weaken()
      return self._new_request_from_response(request)

  def spider_opened(self,spider):
    self.task = task.LoopingCall(self.maintaining_agent)
    self.task.start(360)  # every 1 min = 60s

  def spider_closed(self, spider, reason):
    if self.task and self.task.running:
      self.task.stop()
    self.client.close()

class TopProxyMiddleware(ProxyMiddleware):
  """
      Make statistics for the proxies during certain period, then random choose one from the top 8(default) valided proxies to use
  """

  def process_request(self, request, spider):
    """  Proxy choose strategy:
        
        Choose the top (toppercent %) best proxy
    """
    toppercent= 0.60     # if this value is too small, that means that used proxy converges to a small set
    randomize_top = True     # randomly choose one 
    valid_proxy_list = list(filter(lambda x:x.is_valid(),self.agent_list))
    topindex =  math.ceil(toppercent*len(valid_proxy_list)) 

    #self.maintaining_agent()
    sortedagentlist = sorted(valid_proxy_list, key = lambda i: i.percentage)
    while len(valid_proxy_list) < 10:
      logger.info("Proxy list are nearly used up, let's have a rest")
      self.maintaining_agent()
      valid_proxy_list = list(filter(lambda x:x.is_valid(),self.agent_list))
      sortedagentlist = sorted(valid_proxy_list, key = lambda i: i.percentage)
      time.sleep(30)
    request.meta['agent'] =  random.choice(sortedagentlist[-topindex: ]) if randomize_top else sortedagentlist[-1]
    request.meta['proxy'] = request.meta['agent'].proxy
    request.meta['download_slot'] = self.get_proxy_slot(request.meta['proxy'])
    logger.debug("Request %(request)s using proxy:%(proxy)s",
                    {'request':request, 'proxy':request.meta['proxy']})
