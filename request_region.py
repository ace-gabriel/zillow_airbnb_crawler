import requests
from google.protobuf.json_format import MessageToJson
from python_proto import LocationLookup_pb2
import pprint
import codecs
import json
from multiprocessing import Manager, Pool

cookies = {
    'abtest': '3|DLnihUPLmZKtqatO7g',
    'zguid': '23|%24f0c37fa1-7f18-4331-b2f7-1d818e712d5b',
    'zgsession': '1|4ebd80b7-1c31-4719-a5d2-8f2fc74e31c0',
    '_pxvid': '20126360-aaa2-11e8-90bb-f97381c66358',
    'frmpp': '2|BHRydWU',
    'JSESSIONID': 'A9C550E092D36408C06A91ADEBF96ECB',
    'AWSALB': 'AVS3PQusEbChho1eftsNvAbvC0FNPJf8K8Mv4Ma/nu0ttVyKXsSsEaO32+HxaQUGVinSu8TJrKSVbTagmXGycCSjDAxjTsSLp8sr9muPPBI1MlR5z0ot/R5PB4uH',
}

headers = {
    'X-PX-AUTHORIZATION': '3:5a1d8ce6f25558bd453b929830e2a690e5b5bef3de33aaf686fc2c6e770c93da:T9Rjw0GzKNk3fRkaCBtlIGTzXe7QEJLDmqcKUaH9H4UNMN2IeWB/yf7Kj2wCDPZtn5EoD44MmIfj2qAT1OsYww==:1000:WDLWAsTdVIeGX5dbCgYzwiuOQsz+XOWl3Tc8mCAVyaOf2OnWZ/5DLT6GqhCbG/svUosMXLWuciy9g9QkZWSaVGDH9rBzvEO45bXa3JIpbNPV/37WK5pc2nbAJ16lLSrRMRH1iXcWHFD4Iydzf8gpJ6fd7XtCOKnSwQOabCZk3lE=',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Redmi 3S MIUI/V8.1.5.0.MALCNDI)',
    'Host': 'zm.zillow.com',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

RegionType = {
    "continent":0,
    "country": 1,
    "state": 2,
    "county": 4,
    "city": 6,
    "zipcode": 7,
    "borough": 17,
    "neighborhood": 8,
    "flex": 31,
    "place": 9,
    "unknown": 255,
    "subdivision": 19,
    "community": 18,
    "metro": 14,
    "dma": 10,
    "schoolDistrict": 21,
    "elementarySchool": 22,
    "middleSchool": 23,
    "highSchool": 24,
    "schoolFragment": 25,
    "university": 26
}

def request_region_protobuf(region):
    # region name, for example: Newark NJ
    params = (
        ('zws-id', 'X1-ZWz1c2fz2pfk7f_6r0dc'),
        ('client', 'com.zillow.android.zillowmap'),
        ('device', '03cbcbb1-cd07-4abc-ae43-c30dc0a7d68a'),
        ('deviceType', 'androidGCMRE'),
        ('v', '26'),
        ('text', region),
        ('satSize', '390x260'),
        ('satZoom', '18'),
        ('svSize', '390x260'),
        ('legacyHdpParams', 'p=android&apiver=27&skinver=8&app=com.zillow.android.zillowmap&fromApp=true&renterProfileVersion=mobile_apps_v1&showFactsAndFeatures=true&gmaps=true&streetview=true'),
    )
    try:
        response = requests.get('https://zm.zillow.com/web-services/LocationLookup', headers=headers, params=params, cookies=cookies)
        return response.content
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def get_region_dict(region):
    r = request_region_protobuf(region=region)
    getlocationlookupresults = LocationLookup_pb2.LocationResult().FromString(r)

    result_json = json.loads(MessageToJson(getlocationlookupresults))
    result = {}
    result['region'] = region
    if not result_json.get('southLatitude') or not result_json.get('region'):
        return result
    result['southwest'] = "{},{}".format(result_json['southLatitude'],result_json['westLongitude'])
    result['northeast'] = "{},{}".format(result_json['northLatitude'],result_json['eastLongitude'])
    result['regiontype'] = RegionType[result_json['region']['regionType']]
    result['regionid'] = result_json['region']['regionId']
    result['regiontype_name'] = result_json['region']['regionType']
    return result

def process_msa_city():
    MSA_CITY_LIST_NAME = 'msa_city_list.json'
    START_URLS_JSON = 'start_urls.json'

    results = []

    with open(MSA_CITY_LIST_NAME,"r") as f:
        cities = json.loads(f.read())

    # calculate total number
    total = 0
    for k in cities.values():
        total += len(k)

    for msa,cs in cities.items():
        for c in cs:
            region_dict = get_region_dict(c)
            region_dict['msa'] = msa
            print("{}/{}".format(len(results),total),region_dict)
            results.append(region_dict)

    with open(START_URLS_JSON,'w') as f:
        json.dump(results,f)



if __name__ == '__main__':

    ZIPCODE_INPUT_FILE = "zipcode.txt"
    ZIPCODE_OUTPUT_JSON = "start_urls_zipcode.json"

    manager = Manager()
    results = manager.list()


    with open(ZIPCODE_INPUT_FILE,"r") as f:
        zipcodes = ["{:0>5}".format(z) for z in f.read().split("\n") if z]

    def get_region_and_append_to_array(c):
        region_dict = get_region_dict(c)
        results.append(region_dict)
        print(region_dict)

    p = Pool(10)
    p.map(get_region_and_append_to_array,zipcodes)
    p.close()


    #for c in zipcodes[3500:4000]:
    #    region_dict = get_region_dict(c)
    #    results.append(region_dict)
    #    count+=1
    #    print(count,region_dict)

    results_list = [i for i in results]
    with open(ZIPCODE_OUTPUT_JSON,'w') as f:
        json.dump(results_list,f)


