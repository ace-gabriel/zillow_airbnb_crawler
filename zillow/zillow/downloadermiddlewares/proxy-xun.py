import random
import math
import os
from queue import Queue
import logging
import pymongo
from six.moves.urllib.parse import urljoin
from urllib.parse import urlparse
from w3lib.url import safe_url_string
from datetime import datetime, timedelta
from six.moves.urllib.parse import urlsplit
import time
from twisted.web._newclient import ResponseNeverReceived,ParseError
from twisted.internet.error import TimeoutError,ConnectionRefusedError, ConnectError,ConnectionLost,TCPTimedOutError
from scrapy.utils.response import response_status_message
from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet.defer import _DefGen_Return

from scrapy.http import Request
import requests
import re
from twisted.internet import task
from scrapy import signals

logger = logging.getLogger(__name__)


class Agent(object):
  """ Specify single proxy agent object
      Atttribute:
          proxy: like "http://45.78.34.180:8080"
          success: this proxy's life value (just like solder's blood value in game),\
                  it minus one if failed and plus one if successed
          percentage: proxy's percentage of successful useage, successful_times/total_using-times,default 100%
          absolute_threshold:
          percentage_threshold:
          label: valid or invalid
          last_condition: the success condition of last useage
  """
  def __init__(self,proxy, success=800, percentage=0.8, absolute_threshold=300, percentage_threshold=0.50):
    self.proxy = "http://" + str(proxy)   if not proxy.startswith("http://") else proxy
    self.success = int(success) 
    self.percentage = percentage
    self.total = int(self.success/self.percentage)
    self.absolute_threshold = absolute_threshold
    self.percentage_threshold = percentage_threshold 
    self._set_label()
    self._set_last_condition()  
    self.refercount = 0

  def _set_label(self):
    """set label according to other absolute and relative parameter
    """
    if self.success < self.absolute_threshold or \
        self.percentage < self.percentage_threshold:
      self.label = "invalid" 
    else:
      self.label = 'valid'

  def _set_last_condition(self,condition=True):
    """ Set last success use condition of the agent: True or False
    """
    self.last_condition = True if condition else False

  def weaken(self):
    """ After an failed usage
    """  
    self.total = self.total + 1
    self.success = self.success - 1
    self.percentage = self.success/self.total
    self._set_last_condition(condition=False)
    self._set_label()

  def stronger(self):         
    """ After a successful usage
    """       
    self.total = self.total + 1
    self.success = self.success + 1
    self.percentage = self.success/self.total
    self._set_last_condition(condition=True)
    self._set_label()

  def set_invalid(self):
    """direct way to change validation condition
    """
    self.last_condition = False
    self.label = "invalid"

  def is_valid(self):
    """bool"""
    return self.label == "valid"

  def is_invalid(self):
    """bool"""
    return self.label == "invalid"

  def __eq__(self,other):
    return self.proxy == other.proxy



class ProxyMiddleware(object):
    # Change another proxy instead of passing to RetryMiddlewares when met these errors
  DONT_RETRY_ERRORS = (TimeoutError,ConnectionRefusedError,TCPTimedOutError,
                      ResponseNeverReceived, ConnectError, ConnectionLost, TunnelError, _DefGen_Return)
  agent_list = []

  def __init__(self,settings):
    self.proxy_api = settings['PROXY_API']
    self.proxy_waiting_period = settings.get('PROXY_WAITING_PERIOD',30.0)
    self.proxy_change_period = settings.get('PROXY_CHANGE_PERIOD',600.0)
    self.proxy_api_min_interval = settings.get('PROXY_API_MIN_INTERVAL',15.0)
    self.maintaining_agent()


  @classmethod
  def from_crawler(cls, crawler):  
    settings = crawler.settings
    o = cls(settings)
    o.crawler=crawler
    return o

  def process_request(self, request, spider):
    """ Make request with agent
    """
    if self.agent_list[0].is_invalid():
      logger.info("Invalid proxy which is a situation we dont want to see")
      time.sleep(self.proxy_waiting_period)
      self.get_new_proxy_list()
    agent = self.agent_list[0]
    request.meta['agent'] = agent
    request.meta['proxy'] = request.meta['agent'].proxy
    request.meta['download_slot'] = self.get_proxy_slot(agent.proxy)

    logger.debug("Request %(request)s using proxy:%(proxy)s",
                    {'request':request, 'proxy':request.meta['proxy']})

  def process_response(self, request, response, spider):
    agent = request.meta.get('agent')
    """ Check response status and other validation info to decide whether to change a proxy or not
    """
    if response.status == 200:
      if response.body:     # sometimes empty return page but with 200 code
        logger.debug("Good proxy:{} for processing {}".format(request.meta['proxy'],response))
        agent.stronger()
      else:
        logger.info("Fake  proxy:{} for processing {}".format(request.meta['proxy'],response))
        agent.weaken()  
        return self._new_request_from_response(request)           
      return response

    elif response.status in [307]:
      # Redirecting (302) to <GET https://www.zillow.com/captcha/?dest=qiMbUzSCa1MGIlhrB-2stg> from <GET https://www.zillow.com/
      location = safe_url_string(response.headers['location'])
      redirected_url = urljoin(request.url, location)
      
      if b'captcha' in response.headers[b'Location']:
        logger.info("Redirecting (307) to captcha including url, so we make a new request for url:{}".format(request))
        for k in range(2):
          agent.weaken()
        return self._new_request_from_response(request=Request(url=response.url))
      return response

    elif response.status ==403:
      if 'zillow.com' in response.url:
        agent.set_invalid()
        logger.info("Proxy: {} meet {} ".format(agent.proxy,reason))
        return self._new_request_from_response(request)
      else:
        raise IgnoreRequest
    return response

  def _new_request_from_response(self,request):
    new_request = request.copy() 
    new_request.dont_filter = True
    return new_request

  def get_new_proxy_list(self):
    # fresh proxy list
    logger.info("Starting getting fresh proxies")
    try:
      r = requests.get(self.proxy_api)
    except:
      logger.warning("Maybe request connetion error1")
      return
    while not r.text or 'RESULT' in r.text:
      time.sleep(self.proxy_api_min_interval+1)
      logger.info("Api error:{}, try again".format(r.text))
      try:
        r = requests.get(self.proxy_api)
      except:
        logger.warning("Maybe request connetion error2")
        return
    proxy = r.text.strip("\n")
    self.agent_list = [Agent(proxy)]
    logger.info("New Proxy:{}".format(proxy))

  def maintaining_agent(self):
    """ maintain agent list every certain seconds
    """
    self.get_new_proxy_list()

  def get_proxy_slot(self, proxy):
      """
      Return downloader slot for a proxy.
      By default it doesn't take port in account, i.e. all proxies with
      the same hostname / ip address share the same slot.
      """
      # FIXME: an option to use website address as a part of slot as well?
      return urlsplit(proxy).hostname

  def process_exception(self, request, exception, spider):
    """Handle some connection error, make another request when these error happens
    """        
    logger.debug(exception)
    agent = request.meta.get('agent')
    for i in range(3):
      agent.weaken()
    if isinstance(exception,self.DONT_RETRY_ERRORS):
      logger.debug("Normal exception happened proxy:{} for processing {}".format(request.meta['proxy'],request.url))
      return self._new_request_from_response(request)

  def spider_opened(self,spider):
    # maintain proxy pool every certain seconds
    self.task = task.LoopingCall(self.maintaining_agent)
    self.task.start(self.proxy_change_period)  # every 1 min = 60s

  def spider_closed(self, spider, reason):
    if self.task and self.task.running:
      self.task.stop()
