# Install the Python Requests library:
# `pip install requests`

import requests
import subprocess
import json
from google.protobuf.json_format import MessageToJson
from python_proto import GetZRectResults_pb2
import pprint


def get_rect_region_result(southwest,northeast,regiontype,regionid,page="1"):
    # Request
    # POST https://zm.zillow.com/web-services/GetZRectResults2

    try:
        response = requests.post(
            url="https://zm.zillow.com/web-services/GetZRectResults2",
            params={
                "v": "27",
                "southWest": southwest,
                "northEast": northeast,
                "legacyHdpParams": "p=android&apiver=27&skinver=8&app=com.zillow.android.zillowmap&fromApp=true&renterProfileVersion=mobile_apps_v1&showFactsAndFeatures=true&gmaps=true&streetview=true",
                "asc": "true",
                "st": "aons",       # by agent, by owner, new construction, forclosures, coming soon
                "pnd": "true",     # pending sale
                "ht": "sofat",     # house, condo, manufacture, apartment, townhouse
                "ml": "0",
                #"on": "-90",
                "mh": "0",
                "lo": "0",
                "res": "1",    # max room number from one page
                "fmr": "frt",
                "regionType": regiontype,
                "hi": "0",
                "regionId": regionid,
                "svSize": "390x260",
                "pn": page,
                "sort": "change",
                "satSize": "390x260",
                "satZoom": "18",
                "device": "b2df5ee2-c554-4569-bae5-f7b0bfe976eb",
                "client": "com.zillow.android.zillowmap",
                "deviceType": "androidGCMRE",
                "zws-id": "X1-ZWz1c2fz2pfk7f_6r0dc",
            },
            headers={
                "Cookie": "abtest=3|DPu4JgKMpxK-cdIUnQ; zguid=23|%244ee9c335-82de-4189-86a2-999afa81c004; zgsession=1|e4726785-54ad-4ea3-b312-c75a030f2d3b; AWSALB=cZxLAlc40PQwW/3g0bzVjYl6KfesjnvQ++Vl5qhovhVyGEAY0FKnssKXKvMi4pEXnimIu9pdX+f1LMf5LWJjGMQ9zQz7t4xM5MN+Sg8yHYub/cv7lyW0aAAeOm4k; JSESSIONID=956CD3C1862B877092EA8C6E0234FFF5",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
            },
        )
        return response.content
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


if __name__ == '__main__':
    r = get_rect_region_result(southwest="47.556932,-122.425436",
                                northeast="47.59526,-122.37907",
                                regiontype="7",
                                regionid="99576")
    if b"captcha" in r:
        print("we meet captcha")
    if r:
        with open("zrectresult.bin", "wb") as f:
            f.write(r)

    with open("zrectresult.bin","rb") as f:
        getZRecResults = GetZRectResults_pb2.Results().FromString(f.read())
    result_json = json.loads(MessageToJson(getZRecResults))
    print(result_json)



    pprint.pprint(result_json)
