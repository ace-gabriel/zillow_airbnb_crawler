import logging
import pprint
import datetime

from twisted.internet.task import LoopingCall
from scrapy import signals
from zillow.pipelines import ElasticSearchPipeline

logger = logging.getLogger(__name__)

class _LoopingExtension(object):

    def setup_looping_task(self, task, crawler, interval):
        self._interval = interval
        self._task = LoopingCall(task)
        crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self):
        self._task.start(self._interval, now=False)

    def spider_closed(self):
        if self._task.running:
            self._task.stop()


class DumpStatsExtension(_LoopingExtension):
    """
      Enable this extension to log Scrapy stats periodically, not only
      at the end of the crawl.
    """
    def __init__(self, crawler, interval, pipeline_ext=None):
        self.stats = crawler.stats
        self.pipeline_ext = pipeline_ext
        self.crawler = crawler
        self.setup_looping_task(self.logger_stats, crawler, interval)

    def logger_stats(self):
        stats = self.stats.get_stats()
        stats['spider'] = self.crawler.spider.name
        stats['current_time'] = datetime.datetime.now()
        stats['log_file'] = self.crawler.settings['LOG_FILE']
        pages = self.stats.get_value('response_received_count',0)
        stats['speed/rpm'] = int(pages/((stats['current_time'] - self.stats.get_value('start_time')).seconds/60.0))
        
        if self.pipeline_ext is not None:
            self.pipeline_ext.index_item(stats)
        else:
            logger.info("Scrapy stats:\n" + pprint.pformat(stats))

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat("DUMP_STATS_INTERVAL", 60.0)
        elasticsearch_ext = ElasticSearchPipeline.from_crawler(crawler)
        es_required_settings = {'ELASTICSEARCH_INDEX', 'ELASTICSEARCH_TYPE'}
        for setting_key in es_required_settings:
            if crawler.settings[setting_key] is None:
                elasticsearch_ext = None

        es_required_settings = {'ELASTICSEARCH_INDEX', 'ELASTICSEARCH_TYPE'}
        return cls(crawler, interval, elasticsearch_ext)
