# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch, helpers
from six import string_types
import pymongo

import logging
import hashlib
import types
import datetime


logger = logging.getLogger(__name__)

class InvalidSettingsException(Exception):
    pass

class ZillowPipeline(object):
    def process_item(self, item, spider):
        if item.get('close'):   # 应该是页面都不存在的房源
            return item

        item = self._build_location(item)
        if spider.name == 'ZillowAPI' and not item.get('timeOnZillow'):
            item['timeOnZillow'] = "0"   # some room has no timeOnZillow field
        return item

    def _build_location(self,item):
        item['location_point'] = "{},{}".format(item['latitude'],item['longitude'])
        item['location'] = {
                              "type": "point",
                              "coordinates": [
                                item['longitude'],
                                item['latitude']
                              ]
                            }
        item['loc'] = [item['longitude'],item['latitude']]
        return item


class MongoPipeline(object):

    def __init__(self, settings):
        self.collection_rooms = settings['MONGO_COLLECTION']
        self.client = pymongo.MongoClient(settings['MONGO_HOST'])
        self.db = self.client[settings['MONGO_DB']]

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def process_item(self,item,spider):
        d = datetime.date.today()
        item['updated_at'] = datetime.datetime.combine(d, datetime.time.min)
        if item.get('close'):
            item['close_date'] = item['updated_at']
            self.writing_to_db(item)
        else:
            item = self.process_apt_item(item)
            self.writing_to_db(item)
        return item

    def process_apt_item(self,item):
        # status: FOR_SALE,PENDING,FOR_RENT,SOLD
        if item['homeStatus'] == "FOR_RENT":
            item['status'] = 1
        elif item['homeStatus'] == "FOR_SALE":
            item['status'] = 2
        elif item['homeStatus'] == "PENDING":
            item['status'] = 2
        elif item['homeStatus'] == "FORECLOSED":
            item['status'] = 5
        elif item['homeStatus'] == "SOLD":
            item['status'] = 4
        elif item['homeStatus'] == "RECENTLY_SOLD":
            item['status'] = 4
        elif item['homeStatus'] == "OTHER":
            item['status'] = 3
        # where is the off-market house status=3
        item['status_details'] = item['homeStatus']

        if "hdpUrl" in item.keys() and item['hdpUrl']:
            item['url'] = "https://zillow.com"+item.pop('hdpUrl')
        else:
            item['url'] = "https://zillow.com/homedetails/{}_zpid".format(item['zpid'])
        item['addr'] = item['streetAddress']
        item['room_type'] = item['homeType']

        if item.get('tvHighResImageLink'):
            item['pict_urls'] = item['tvHighResImageLink']
        item['year_built'] = item['yearBuilt']


        # 从接口请求的卖掉的房子，daysOnZillow恐怕一直是-1了
        if item['spider']=="ZillowAPI":
            item['online_date'] = item['updated_at'] - datetime.timedelta(days=int(item['daysOnZillow'])) if item.get('daysOnZillow') or item['daysOnZillow']==0 else None
            if item['online_date'] and item['online_date'] > item['updated_at']:
                item['online_date'] = None
            item['last_sold_date'] = datetime.datetime.utcfromtimestamp(float(item['dateSold'])/1000)

        item['sale_or_rent_price'] = item.get('price')
        item['zestimate'] = item.get('festimate')
        item['rent_zestimate'] = item.get('rentZestimate')
        item['beds'] = item.get('bedrooms')
        item['baths'] = item.get('bathrooms')
        item['size'] = item.get('livingArea')

        today = datetime.datetime(year=datetime.date.today().year,month=datetime.date.today().month,day=datetime.date.today().day,hour=0)
        price_condition = {'sale_or_rent_price':item.get('sale_or_rent_price'),
                        'status':item.get('status'),
                        'zestimate':item.get('zestimate'),
                        'rent_zestimate':item.get('rent_zestimate'),
                        'date':today}
        item['price_history_accumulate'] = price_condition

        return item

    def writing_to_db(self,item):
        # 如果是pricehistory爬虫的话，增加一个字段吧
        if item['spider']=="ZillowPriceHistory" or item['spider']=="ZillowPriceHistory2":
            item['pricehistory_crawled_date'] = item['updated_at']

        if item.get('close'):
            self.db[self.collection_rooms].update(
                {'zpid':item['zpid']},
                {'$set':{'close':item['close'], 
                        'close_date': item['close_date'],
                        'updated_at':item['updated_at'],
                        'pricehistory_crawled_date':datetime.datetime(year=2100,month=1,day=1),
                        'status':0,
                        'spider':item.get('spider'),
                        }
                },upsert=True,multi=True)
        else:
            update = {k:v for k,v in item.items() if k!='price_history_accumulate'}
            history = item['price_history_accumulate']
            self.db[self.collection_rooms].update({'zpid':item['zpid']},{'$set':update, '$push':{'price_history_accumulate':history}},upsert=True,multi=True)

    def close_spider(self, spider):
        self.client.close()

class ElasticSearchPipeline(object):
    settings = None
    es = None
    items_buffer = []

    @classmethod
    def validate_settings(cls, settings):
        def validate_setting(setting_key):
            if settings[setting_key] is None:
                logger.error('%s is not defined in settings.py' % setting_key)

        required_settings = {'ELASTICSEARCH_INDEX', 'ELASTICSEARCH_TYPE'}

        for required_setting in required_settings:
            validate_setting(required_setting)

    @classmethod
    def init_es_client(cls, crawler_settings):
        auth_type = crawler_settings.get('ELASTICSEARCH_AUTH')
        es_timeout = crawler_settings.get('ELASTICSEARCH_TIMEOUT',60)

        es_servers = crawler_settings.get('ELASTICSEARCH_SERVERS', 'localhost:9200')
        es_servers = es_servers if isinstance(es_servers, list) else [es_servers]

        if auth_type == 'NTLM':
            from .transportNTLM import TransportNTLM
            es = Elasticsearch(hosts=es_servers,
                               transport_class=TransportNTLM,
                               ntlm_user= crawler_settings['ELASTICSEARCH_USERNAME'],
                               ntlm_pass= crawler_settings['ELASTICSEARCH_PASSWORD'],
                               timeout=es_timeout)

            return es

        es_settings = dict()
        es_settings['hosts'] = es_servers
        es_settings['timeout'] = es_timeout

        if 'ELASTICSEARCH_USERNAME' in crawler_settings and 'ELASTICSEARCH_PASSWORD' in crawler_settings:
            es_settings['http_auth'] = (crawler_settings['ELASTICSEARCH_USERNAME'], crawler_settings['ELASTICSEARCH_PASSWORD'])

        if 'ELASTICSEARCH_CA' in crawler_settings:
            import certifi
            es_settings['port'] = 443
            es_settings['use_ssl'] = True
            es_settings['ca_certs'] = crawler_settings['ELASTICSEARCH_CA']['CA_CERT']
            es_settings['client_key'] = crawler_settings['ELASTICSEARCH_CA']['CLIENT_KEY']
            es_settings['client_cert'] = crawler_settings['ELASTICSEARCH_CA']['CLIENT_CERT']

        es = Elasticsearch(**es_settings)
        return es

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        cls.validate_settings(ext.settings)
        ext.es = cls.init_es_client(crawler.settings)
        return ext

    def process_unique_key(self, unique_key):
        if isinstance(unique_key, list):
            unique_key = unique_key[0].encode('utf-8')
        elif isinstance(unique_key, string_types):
            unique_key = unique_key.encode('utf-8')
        elif isinstance(unique_key,int):
            unique_key = str(unique_key).encode('utf-8')
        else:
            raise Exception('unique key must be str or unicode')

        return unique_key

    def get_id(self, item):
        item_unique_key = item[self.settings['ELASTICSEARCH_UNIQ_KEY']]
        if isinstance(item_unique_key, list):
            item_unique_key = '-'.join(item_unique_key)

        unique_key = self.process_unique_key(item_unique_key)
        item_id = hashlib.sha1(unique_key).hexdigest()
        return item_id

    def index_item(self, item):

        index_name = self.settings['ELASTICSEARCH_INDEX']
        index_suffix_format = self.settings.get('ELASTICSEARCH_INDEX_DATE_FORMAT', None)
        index_suffix_key = self.settings.get('ELASTICSEARCH_INDEX_DATE_KEY', None)
        index_suffix_key_format = self.settings.get('ELASTICSEARCH_INDEX_DATE_KEY_FORMAT', None)

        if index_suffix_format:
            if index_suffix_key and index_suffix_key_format:
                dt = datetime.strptime(item[index_suffix_key], index_suffix_key_format)
            else:
                dt = datetime.datetime.now()
            index_name += "-" + datetime.datetime.strftime(dt,index_suffix_format)
        elif index_suffix_key:
            index_name += "-" + index_suffix_key

        index_action = {
            '_index': index_name,
            '_type': self.settings['ELASTICSEARCH_TYPE'],
            '_source': dict(item)
        }

        if self.settings['ELASTICSEARCH_UNIQ_KEY'] is not None:
            item_id = self.get_id(item)
            index_action['_id'] = item_id
            logging.debug('Generated unique key %s' % item_id)

        self.items_buffer.append(index_action)

        if len(self.items_buffer) >= self.settings.get('ELASTICSEARCH_BUFFER_LENGTH', 500):
            self.send_items()
            self.items_buffer = []

    def send_items(self):
        helpers.bulk(self.es, self.items_buffer)

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            self.index_item(item)
            logging.debug('Item sent to Elastic Search %s' % self.settings['ELASTICSEARCH_INDEX'])
            return item

    def close_spider(self, spider):
        if len(self.items_buffer):
            self.send_items()
