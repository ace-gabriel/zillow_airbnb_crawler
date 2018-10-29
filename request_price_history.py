import requests
import pprint

headers = {
    'accept': '*/*',
    'origin': 'https://www.zillow.com',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi 3S Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 ZillowApp/1.0',
    'content-type': 'text/plain',
    'referer': 'https://www.zillow.com/homedetail/MobileAppHomeDetailsServicePage.htm?fromApp=true&p=android',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,en-US;q=0.9',
    'x-requested-with': 'com.zillow.android.zillowmap',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

def request_json_data_from_zpid(zpid):
    data = '{"operationName":"PriceTaxQuery","variables":{"zpid":#ZPID#},"query":"query PriceTaxQuery($zpid: ID!) {\\n  property(zpid: $zpid) {\\n  hdpUrl\\n  zpid\\n  state\\n  county\\n  city\\n zipcode\\n  neighborhoodId\\n homeType\\n rentZestimate\\n zestimate\\n homeStatus\\n streetAddress\\n price\\n  nearbySchools {\\n distance\\n name\\n rating\\n level\\n studentsPerTeacher\\n assigned\\n grades\\n link\\n type\\n size\\n}\\n propertyTaxRate\\n  bedrooms\\n bathrooms\\n livingArea\\n lotSize\\n yearBuilt\\n latitude\\n longitude\\n  countyFIPS\\n    parcelId\\n hoaFee\\n  taxHistory {\\n      time\\n      taxPaid\\n      taxIncreaseRate\\n      value\\n      valueIncreaseRate\\n    }\\n    priceHistory {\\n      time\\n      price\\n      priceChangeRate\\n      event\\n      source\\n      buyerAgent {\\n        photo {\\n          url\\n        }\\n        profileUrl\\n        name\\n      }\\n      sellerAgent {\\n        photo {\\n          url\\n        }\\n        profileUrl\\n        name\\n      }\\n      showCountyLink\\n    }\\n    currency\\n  }\\n}\\n","clientVersion":"home-details/5.28.0.10.master.caf361e"}'.replace("#ZPID#",zpid)

    response = requests.post('https://gdp.zillow.com/api/',
                             headers=headers, 
                             data=data)
    return response


response = request_json_data_from_zpid("28364484")
pprint.pprint(response.json())
