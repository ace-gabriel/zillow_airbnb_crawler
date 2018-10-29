import logging

from twisted.internet import task

from scrapy.exceptions import NotConfigured
from scrapy import signals

logger = logging.getLogger(__name__)


class IpLogStats(object):
  """Log basic scraping stats periodically"""

  def __init__(self, crawler, intervalip=300.0):
    self.crawler = crawler
    self.intervalip = intervalip
    self.taskip = None

  @classmethod
  def from_crawler(cls, crawler):
    intervalip = crawler.settings.getfloat('IPPOOLSTATS_INTERVAL')
    if not intervalip:
      raise NotConfigured
    o = cls(crawler,intervalip)
    crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
    crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
    return o

  def spider_opened(self, spider):
    self.taskip = task.LoopingCall(self.logip,spider)
    self.taskip.start(self.intervalip)

  def logip(self,spider): 
    # TODO: there must be an easy way to navigate
    proxy =[o for o in self.crawler.engine.downloader.middleware.middlewares if "proxy" in o.__str__()]
    if not proxy.__len__() == 2:
      raise("Founded Proxy middlwares is not equal to 2! ")
    proxyobj = proxy[-1]

    logger.info('[*******] %d Current unique proxy condition' % len(proxyobj.agent_list))
    logger.info('                              Proxy              | Success  |       Total.Request      | Percentage      | label')
    for _ag in proxyobj.agent_list:
      ag_str = "{:<30} {:<6} {:<7} {:.2%} {:<8}".format(str(_ag.proxy),str(_ag.success),str(_ag.total),_ag.percentage,_ag.label)
      logger.info(ag_str)

  def spider_closed(self, spider, reason):
    if self.taskip and self.taskip.running:
      self.taskip.stop()
