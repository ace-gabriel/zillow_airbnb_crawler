#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import random
import os
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

logger = logging.getLogger(__name__)


class RotateUserAgentMiddleware(UserAgentMiddleware):
  """useragent middleware"""

  useragent_list = []
  #useragentFile = os.path.dirname(os.getcwd()) + '/useragentlist.txt'
  useragentFile = './useragentlist.txt'

  def __init__(self,user_agent="Scrapy"):
    self.user_agent = user_agent
    self.readuseragentfile()

  def process_request(self,request,spider):
    ua = random.choice(self.useragent_list)
    #logger.debug("Request {} using ua:{}".format(request,ua))
    if ua:            
        request.headers['User-Agent']=ua

  def readuseragentfile(self):
    """Read to useragent_list from file"""
    with open(self.useragentFile) as f:
      for line in f:
        self.useragent_list.append(line.strip('\n'))
      return len(self.useragent_list)
