# Install the Python Requests library:
# `pip install requests`

import requests
from google.protobuf.json_format import MessageToJson
from python_proto import HomeDetails_pb2
import pprint
import codecs
import json


def get_homedetails():
    # Request (2)
    # GET https://zm.zillow.com/web-services/HomeDetails

    try:
        response = requests.get(
            url="https://zm.zillow.com/web-services/HomeDetails",
            params={
                "v": "4",

                "zpid": "48700909",

                "jsonver": "1",
                "high-res": "true",
                "watch": "false",
                "device": "b2df5ee2-c554-4569-bae5-f7b0bfe976eb",
                "client": "com.zillow.android.zillowmap",
                "deviceType": "androidGCMRE",
                "zws-id": "X1-ZWz1c2fz2pfk7f_6r0dc",

                "zipcode": "98199"
            },
            headers={
                "Cookie": "zgsession=1|e4726785-54ad-4ea3-b312-c75a030f2d3b; abtest=3|DNNRuxUp8qLICMP5IA; zguid=23|%249c0fb545-e1ab-4a19-a670-4d59cfd4e248; AWSALB=GX8B+HrKOR/zOvGY9u7cc+l35MMGvm0aPAzBceQG3JKS2H/orLmZFDVMEdGD+vs7ONNHxZwadGa8rvLiZFHvQeAkldM6TFpfb60xwxlz6BPuOeeE9Qg4u2vWDlKp; JSESSIONID=694CE8958A076744C82CC9E5B4067D7A",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
            },
        )
        return response.content
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


if __name__ == '__main__':
    #r = get_homedetails()
    #if b"captcha" in r:
    #    print("we meet captcha")
    #if r:
    #    with open("homedetails.bin", "wb") as f:
    #        f.write(r)

    with open("homedetails.bin","rb") as f:
        getHomedetailresults = HomeDetails_pb2.HomeDetailsResult().FromString(f.read())

    result_json = json.loads(MessageToJson(getHomedetailresults))

    print(result_json)
    # handle some json with escape value
    s = result_json["hdpTemplateJsonString"]
    result_json["hdpTemplateJsonString"] = xx=eval('''{}'''.format(s.replace('true','True').replace('false','False').replace('null','None')))
    print(result_json)
    print(result_json.keys())
    print(result_json['hdpTemplateJsonString'])

    #pprint.pprint(result_json)
