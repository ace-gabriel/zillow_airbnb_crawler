import scrapy
import json
from urllib.parse import urlencode
from scrapy.shell import inspect_response
from google.protobuf.json_format import MessageToJson
from python_proto import GetZRectResults_pb2
import math
import logging
import re
import pymongo
import datetime

class ZillowApiSpider(scrapy.Spider):
    '''
      从zillow search pages页获取房源数据

    '''

    name = "ZillowAPI"
    max_homes_per_pages = 200
    count_thredshold = 1000

    def _make_paras_from_dict_and_page(self,item,page=1,lo=0,hi=5000000):
        # dict should have key southwest,northeast,regiontype,regionid
        params = urlencode(
                  {
                "v": "27",
                "southWest": item['southwest'],
                "northEast": item['northeast'],
                "legacyHdpParams": "p=android&apiver=27&skinver=8&app=com.zillow.android.zillowmap&fromApp=true&renterProfileVersion=mobile_apps_v1&showFactsAndFeatures=true&gmaps=true&streetview=true",
                "asc": "true",
                "st": "aons",       # by agent, by owner, new construction, forclosures, coming soon
                "pnd": "true",     # pending sale
                "ht": "sofat",     # house, condo, manufacture, apartment, townhouse
                "ml": "0",
                #"on": "-90",       # last one month
                "mh": "0",
                "lo": str(lo),         # # house price lower
                "res": str(self.max_homes_per_pages),    # max room number from one page
                "fmr": "frt",     # for sale, recently sold, for rent
                "regionType": str(item['regiontype']),
                "hi": str(hi),        # house price upper
                "regionId": str(item['regionid']),
                "svSize": "390x260",
                "pn": str(page),
                "sort": "change",
                "satSize": "390x260",
                "satZoom": "18",
                "device": "b2df5ee2-c554-4569-bae5-f7b0bfe976eb",
                "client": "com.zillow.android.zillowmap",
                "deviceType": "androidGCMRE",
                "zws-id": "X1-ZWz1c2fz2pfk7f_6r0dc",
            })
        return params

    def start_requests(self):
        start_urls_file = "start_urls_zipcode_full.json"
        filter_msa_file = "msa_top39_zipcodes.json"
        filter_city_file = "filter_city_file.json"
        with open(start_urls_file,encoding='utf-8') as f:
            start_json = json.load(f)

        # read two files for zipcode filtering
        with open(filter_msa_file) as fm:
          MSA = json.load(fm)
          MSA_ZIPCODES = set([i['zipcode'] for i in MSA])

        with open(filter_city_file) as fc:
          CITY = json.load(fc)
          CITY_ZIPCODES = set([i['zipcode'] for i in CITY])

        for index,region_item in enumerate(start_json):
            #if index==0:
            if not region_item.get("southwest") or not region_item.get('regiontype') or not region_item.get('regionid'):
                continue

            # only for test
            #if not region_item.get('regionid') == 99576:
            #    continue

            # msa filter for zipcodes OR city filter for zipcodes
            filter_zipcode_switch = True
            if filter_zipcode_switch:
              if not (region_item.get('region') in MSA_ZIPCODES or region_item.get('region') in CITY_ZIPCODES):
                continue

            params = self._make_paras_from_dict_and_page(region_item,page=1)
            yield scrapy.Request(
              url="https://zm.zillow.com/web-services/GetZRectResults2?"+params,
              method='GET',
              headers={
                    "Cookie": "abtest=3|DPu4JgKMpxK-cdIUnQ; zguid=23|%244ee9c335-82de-4189-86a2-999afa81c004; zgsession=1|e4726785-54ad-4ea3-b312-c75a030f2d3b; AWSALB=cZxLAlc40PQwW/3g0bzVjYl6KfesjnvQ++Vl5qhovhVyGEAY0FKnssKXKvMi4pEXnimIu9pdX+f1LMf5LWJjGMQ9zQz7t4xM5MN+Sg8yHYub/cv7lyW0aAAeOm4k; JSESSIONID=956CD3C1862B877092EA8C6E0234FFF5"

                },
              meta = {"region":region_item}
              )

    def _generate_binaray_splited_request(self,url,regionitem):
        lo = int(re.search('lo=([0-9]+)',url).group(1))
        hi = int(re.search('hi=([0-9]+)',url).group(1))
        cut_price = int((lo+hi)/2)
        self.logger.debug("Let's split the query url:{url} inteval:{bp}-{cut_price},{cut_price}-{ep}".format(
                    url=url,
                    cut_price=cut_price,
                    bp=lo,
                    ep=hi))

        # yield the upper query
        url_new = re.sub(r'lo=[0-9]+','lo={}'.format(cut_price),url)
        yield scrapy.Request(
                      url=url_new,
                      method='GET',
                      headers={
                            "Cookie": "abtest=3|DPu4JgKMpxK-cdIUnQ; zguid=23|%244ee9c335-82de-4189-86a2-999afa81c004; zgsession=1|e4726785-54ad-4ea3-b312-c75a030f2d3b; AWSALB=cZxLAlc40PQwW/3g0bzVjYl6KfesjnvQ++Vl5qhovhVyGEAY0FKnssKXKvMi4pEXnimIu9pdX+f1LMf5LWJjGMQ9zQz7t4xM5MN+Sg8yHYub/cv7lyW0aAAeOm4k; JSESSIONID=956CD3C1862B877092EA8C6E0234FFF5"

                      },
                      meta={
                      "referrer_policy":"no-referrer",
                      "region":regionitem,
                      "from_split_upper":True
                          }
                      )

        # yield the lower query
        url_new2 = re.sub(r'hi=[0-9]+','hi={}'.format(cut_price),url)
        yield scrapy.Request(
                      url=url_new2,
                      method='GET',
                      headers={
                            "Cookie": "abtest=3|DPu4JgKMpxK-cdIUnQ; zguid=23|%244ee9c335-82de-4189-86a2-999afa81c004; zgsession=1|e4726785-54ad-4ea3-b312-c75a030f2d3b; AWSALB=cZxLAlc40PQwW/3g0bzVjYl6KfesjnvQ++Vl5qhovhVyGEAY0FKnssKXKvMi4pEXnimIu9pdX+f1LMf5LWJjGMQ9zQz7t4xM5MN+Sg8yHYub/cv7lyW0aAAeOm4k; JSESSIONID=956CD3C1862B877092EA8C6E0234FFF5"

                      },
                      meta={
                      "referrer_policy":"no-referrer",
                      "region":regionitem,
                      "from_split_lower":True
                          }
                      )

    def parse_items_from_next_pages(self,response):
        url = response.url
        region_item = response.meta['region']
        getZRecResult = GetZRectResults_pb2.Results().FromString(response.body)
        result_json = json.loads(MessageToJson(getZRecResult))
        if result_json.get('homes'):
            for home in result_json['homes']:
                if home.get('homes'):
                    item_raw = home['homes'][0]
                    item_raw['spider'] = self.name
                    yield item_raw


    def parse(self,response):
        url = response.url
        region_item = response.meta['region']
        getZRecResult = GetZRectResults_pb2.Results().FromString(response.body)
        result_json = json.loads(MessageToJson(getZRecResult))

        lo = int(re.search('lo=([0-9]+)',url).group(1))
        hi = int(re.search('hi=([0-9]+)',url).group(1))

        self.logger.debug("Get query result url:{url} inteval:{bp},{ep},count:{count}".format(
                            url=url,
                            bp=lo,
                            ep=hi,
                            count=result_json.get('totalHomes')))

        if result_json.get('totalHomes'):
            if int(result_json.get('totalHomes')) > self.count_thredshold:
                for r in self._generate_binaray_splited_request(url,region_item):
                    yield r
            else:
                if result_json.get('homes'):
                    for home in result_json['homes']:
                        if home.get('homes'):
                            item_raw = home['homes'][0]
                            item_raw['spider'] = self.name
                            yield item_raw

                    max_pages = math.ceil(result_json['totalHomes']/self.max_homes_per_pages)
                    if max_pages==1:
                        self.logger.info("{},***,total:{},page:{}/{}".format(
                           region_item['region'],
                           result_json.get('totalHomes'),
                           1,
                           max_pages))
                    for page in range(2,max_pages+1):
                        self.logger.info("{},***,total:{},page:{}/{}".format(
                           region_item['region'],
                           result_json.get('totalHomes'),
                           page,
                           max_pages))
                        params = self._make_paras_from_dict_and_page(region_item,page=page,lo=lo,hi=hi)
                        yield scrapy.Request(
                              url="https://zm.zillow.com/web-services/GetZRectResults2?"+params,
                              method='GET',
                              headers={
                                    "Cookie": "abtest=3|DPu4JgKMpxK-cdIUnQ; zguid=23|%244ee9c335-82de-4189-86a2-999afa81c004; zgsession=1|e4726785-54ad-4ea3-b312-c75a030f2d3b; AWSALB=cZxLAlc40PQwW/3g0bzVjYl6KfesjnvQ++Vl5qhovhVyGEAY0FKnssKXKvMi4pEXnimIu9pdX+f1LMf5LWJjGMQ9zQz7t4xM5MN+Sg8yHYub/cv7lyW0aAAeOm4k; JSESSIONID=956CD3C1862B877092EA8C6E0234FFF5"

                                 },
                              meta={
                              "referrer_policy":"no-referrer",
                              "region":region_item,
                              "next_page":True
                                  },
                              callback = self.parse_items_from_next_pages
                              )





class ZillowApiSpiderdb(scrapy.Spider):
    '''
      从app中获取到一个price history的接口，顺便补充一些房源字段

    '''
    name = "ZillowPriceHistory"
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS":{
          'accept': '*/*',
          'origin': 'https://www.zillow.com',
          'content-type': 'text/plain',
          'referer': 'https://www.zillow.com/homedetail/MobileAppHomeDetailsServicePage.htm?fromApp=true&p=android',
          'accept-encoding': 'gzip, deflate',
          'accept-language': 'zh-CN,en-US;q=0.9',
          'x-requested-with': 'com.zillow.android.zillowmap',
          'Pragma': 'no-cache',
          'Cache-Control': 'no-cache'
                                },
        "CONCURRENT_REQUESTS":100
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider._set_crawler(crawler)
        spider.client = pymongo.MongoClient(crawler.settings['MONGO_HOST'])
        spider.database_name = crawler.settings['MONGO_DB']
        spider.collection_name = crawler.settings['MONGO_COLLECTION']
        return spider

    def start_requests(self):
        now = datetime.datetime.now()
        self.cursor = self.client[self.database_name][self.collection_name].find(
          {'pricehistory_crawled_date':{"$lte":now}},
          {'zpid':1,'pricehistory_crawled_date':1,'_id':0},
          no_cursor_timeout=True).sort('pricehistory_crawled_date',1).limit(1800000)
          # we only get 200 every day 
          # 200 wan * 1 week = 1400 wan
        ids = list(self.cursor)
        self.logger.info("Process the older properties, count:{}".format(len(ids)))

        # add local file
        # ids =[]
        # larger = 5000
        # smaller = 0
        # with open("zpids_from_db.csv") as f:
            # for index,line in enumerate(f):
                # if index<larger and index>smaller:
                    # doc=dict()
                    # doc['zpid'] = int(line.split(',')[0])
                    # ids.append(doc)
                # while index>larger:
                    # break

        for doc in ids:
            # 初次从数据库中爬取的时候pricehistory_crawled_date字段为空；
            # 下次访问的时候可以用时间来过过滤, 比如和当前时间差7天
            LONG_CRAWLED_PERIODS_DAYS = 7
            if not doc.get('pricehistory_crawled_date') or (now - doc['pricehistory_crawled_date']).days > LONG_CRAWLED_PERIODS_DAYS:
                zpid = str(doc['zpid'])
                request_data = '{"operationName":"PriceTaxQuery","variables":{"zpid":#ZPID#},"query":"query PriceTaxQuery($zpid: ID!) {\\n  property(zpid: $zpid) {\\n  hdpUrl\\n  zpid\\n  state\\n  county\\n  city\\n zipcode\\n  neighborhoodId\\n homeType\\n festimate\\n rentZestimate\\n zestimate\\n homeStatus\\n streetAddress\\n price\\n  nearbySchools {\\n distance\\n name\\n rating\\n level\\n studentsPerTeacher\\n assigned\\n grades\\n link\\n type\\n size\\n}\\n propertyTaxRate\\n  bedrooms\\n bathrooms\\n livingArea\\n lotSize\\n yearBuilt\\n latitude\\n longitude\\n  countyFIPS\\n    parcelId\\n hoaFee\\n  taxHistory {\\n      time\\n      taxPaid\\n      taxIncreaseRate\\n      value\\n      valueIncreaseRate\\n    }\\n    priceHistory {\\n      time\\n      price\\n      priceChangeRate\\n      event\\n      source\\n      buyerAgent {\\n        photo {\\n          url\\n        }\\n        profileUrl\\n        name\\n      }\\n      sellerAgent {\\n        photo {\\n          url\\n        }\\n        profileUrl\\n        name\\n      }\\n      showCountyLink\\n    }\\n    currency\\n  }\\n}\\n","clientVersion":"home-details/5.28.0.10.master.caf361e"}'.replace("#ZPID#",zpid)

                # url maybe has two possiblity
                # url1: https://gdp.zillow.com/api/
                # url2: https://www.zillow.com/graphql/
                yield scrapy.Request(url='https://gdp.zillow.com/api/',
                          method='POST',
                          body=request_data,
                          meta={'zpid':doc['zpid']})

    def parse(self,response):
        zpid = response.meta['zpid']
        #inspect_response(response,self)
        data = json.loads(response.text)
        if "data" in data.keys():
          if data['data']['property']:
            item_raw = data['data']['property']
            item_raw['spider'] = self.name
            item_raw['close'] = False
            return item_raw
          else:
            return {'close':True,'zpid':zpid,"spider":self.name}


    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            spider.client.close()
            return closed(reason)



class ZillowApiSpiderdb2(ZillowApiSpiderdb):
    '''
      一些失去链接的房源或offmarket的房源，无法从search pages获得最新的status，所以需要一个爬虫处理一下

    '''
    name = "ZillowPriceHistory2"

    def start_requests(self):
        now = datetime.datetime.now()
        TWO_DAYS = 2
        SEVEN_DAYS = 7
        self.logger.info("Time range:{}-{}".format(now-datetime.timedelta(days=TWO_DAYS),now-datetime.timedelta(days=SEVEN_DAYS)))
        self.cursor = self.client[self.database_name][self.collection_name].find(
          {'updated_at':{"$lt":now-datetime.timedelta(days=TWO_DAYS),
                        "$gte":now-datetime.timedelta(days=SEVEN_DAYS)},
            'status':{"$in":[1,2,5]}},
          {'zpid':1,'close':1,'status':1,'_id':0},
          no_cursor_timeout=True).limit(1500000)

        ids = list(self.cursor)
        self.logger.info("Process the updated_at older properties, count:{}".format(len(ids)))

        for doc in ids:
            #if doc.get('close') != True:  # refresh一遍，所以可以重复
            zpid = str(doc['zpid'])
            request_data = '{"operationName":"PriceTaxQuery","variables":{"zpid":#ZPID#},"query":"query PriceTaxQuery($zpid: ID!) {\\n  property(zpid: $zpid) {\\n  hdpUrl\\n  zpid\\n  state\\n  county\\n  city\\n zipcode\\n  neighborhoodId\\n homeType\\n festimate\\n rentZestimate\\n zestimate\\n homeStatus\\n streetAddress\\n price\\n  nearbySchools {\\n distance\\n name\\n rating\\n level\\n studentsPerTeacher\\n assigned\\n grades\\n link\\n type\\n size\\n}\\n propertyTaxRate\\n  bedrooms\\n bathrooms\\n livingArea\\n lotSize\\n yearBuilt\\n latitude\\n longitude\\n  countyFIPS\\n    parcelId\\n hoaFee\\n  taxHistory {\\n      time\\n      taxPaid\\n      taxIncreaseRate\\n      value\\n      valueIncreaseRate\\n    }\\n    priceHistory {\\n      time\\n      price\\n      priceChangeRate\\n      event\\n      source\\n      buyerAgent {\\n        photo {\\n          url\\n        }\\n        profileUrl\\n        name\\n      }\\n      sellerAgent {\\n        photo {\\n          url\\n        }\\n        profileUrl\\n        name\\n      }\\n      showCountyLink\\n    }\\n    currency\\n  }\\n}\\n","clientVersion":"home-details/5.28.0.10.master.caf361e"}'.replace("#ZPID#",zpid)

            # url maybe has two possiblity
            # url1: https://gdp.zillow.com/api/
            # url2: https://www.zillow.com/graphql/
            yield scrapy.Request(url='https://gdp.zillow.com/api/',
                      method='POST',
                      body=request_data,
                      meta={'zpid':doc['zpid']})
