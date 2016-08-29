import requests
import json
import time


ziroom_path = 'http://interfaces.ziroom.com/index.php?_p=api_mobile&_a=get_houseList_by_xiaoqu'

ts = int(time.time())
r = requests.post(ziroom_path,data={'max_area':'',
                                    'heating':'',
                                    'house_tag[0]':0,
                                    'house_tag[1]':0,
                                    'house_tag[2]':0,
                                    'house_tag[3]':0,
                                    'house_tag[4]':0,
                                    'house_tag[5]':0,
                                    'house_tag[6]':0,
                                    'min_lng':116.335486,
                                    'end':10,
                                    'max_rentfee':'',
                                    'bizcircle_code':'',
                                    'subway_station_name':'',
                                    'min_area':'',
                                    'huxing':'',
                                    'start':'',
                                    'max_lat':40.06572,
                                    'min_lat':40.059563,
                                    'max_ing':116.41307,
                                    'city_code':110000,
                                    'min_rentfee':'',
                                    'timestamp':'1458141761',
                                    'building_code':'1111027377627',
                                    'sign':'f5644b35e8a3eb0de468b3fc400e306c',
                                    'uid':'d41432db-068e-f467-f6c9-99d7b6de009b',
                                    'house_type':'0'
                                    })

res = json.loads(r.text)
print res['status']
print len(res['data'])
