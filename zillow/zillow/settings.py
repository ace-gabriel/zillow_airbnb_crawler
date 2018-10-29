# -*- coding: utf-8 -*-

# Scrapy settings for zillow project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import time

import yaml
with open("config.yml") as f:
  CONFIG = yaml.load(f)

BOT_NAME = 'zillow'

SPIDER_MODULES = ['zillow.spiders']
NEWSPIDER_MODULE = 'zillow.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 30

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zillow.middlewares.ZillowSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'zillow.middlewares.ZillowDownloaderMiddleware': 543,
    'zillow.downloadermiddlewares.rotate_useragent.RotateUserAgentMiddleware':560,
    #'zillow.downloadermiddlewares.rotateproxy.ProxyMiddleware':780,
    #'zillow.downloadermiddlewares.rotateproxy.TopProxyMiddleware':780,
    #'zillow.downloadermiddlewares.proxy-xun.ProxyMiddleware':790,
    'zillow.downloadermiddlewares.proxy-abuyun.ProxyMiddleware':920,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
if CONFIG['elasticsearch']['use']:
    EXTENSIONS = {
        'zillow.extensions.monitor.DumpStatsExtension':101
    }

DUMP_STATS_INTERVAL = 60

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'zillow.pipelines.ZillowPipeline': 300,
    #'zillow.pipelines.ElasticSearchPipeline':400,
    'zillow.pipelines.MongoPipeline':500
}

ELASTICSEARCH_SERVERS = CONFIG['elasticsearch']['servers']
ELASTICSEARCH_INDEX = CONFIG['elasticsearch']['index']
ELASTICSEARCH_INDEX_DATE_FORMAT = CONFIG['elasticsearch']['index_date_format']
ELASTICSEARCH_TYPE = CONFIG['elasticsearch']['type']
ELASTICSEARCH_UNIQ_KEY = CONFIG['elasticsearch'].get('uniq_key')
ELASTICSEARCH_BUFFER_LENGTH = CONFIG['elasticsearch']['buffer_length']

#Mongo Rooms
MONGO_HOST = CONFIG['mongo_rooms']['mongo_host']
MONGO_DB = CONFIG['mongo_rooms']['mongo_db']
MONGO_COLLECTION = CONFIG['mongo_rooms']['mongo_collection']


# LOG SETTING
LOG_LEVEL = 'INFO'
LOG_FILE = "zillow/logs/scrapy_%s_%s.log"%(BOT_NAME,time.time())

# Mongo Proxy
MONGO_PROXY_HOST = CONFIG['mongo_proxy']['mongo_host']
MONGO_PROXY_DB = CONFIG['mongo_proxy']['mongo_db']
MONGO_PROXY_COLLECTION = CONFIG['mongo_proxy']['mongo_collection']

# ProxyPool 
IPPOOLSTATS_INTERVAL = 1800.0 
MAX_POOL_SIZE = 300
MIN_POOL_SIZE = 3
MAINTAIN_INTERVAL = 360
POOL_WAITING = 30
BETTER_PERCENT = 0.50
BETTER_MAX_COUNT = 120

# Xun Proxy Related
PROXY_API = CONFIG['xun_proxy']['proxyHost']
PROXY_WAITING_PERIOD = 30.0
PROXY_CHANGE_PERIOD = 600.0
PROXY_API_MIN_INTERVAL = 15.0        # xun代理api调用时间最短间隔为15秒


DOWNLOAD_TIMEOUT = 180
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
## The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
## The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
## The average number of requests Scrapy should be sending in parallel to
## each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
## Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
