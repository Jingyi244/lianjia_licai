# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import subprocess
import time
import json
import requests
import urllib2
import urllib
import simplejson
import random

pathMap = {
        'xiErQi':'http://www.webapi.ziroom.com/v7/room/list.json?sign=70130d9703871f160f0243592eacae17&size=10&timestamp=1492419592&feature=3&os=android%3A7.0&network=WIFI&sign_open=1&app_version=5.2.0&price=%2C3400&imei=354112070288845&ip=10.33.73.63&uid=d41432db-068e-f467-f6c9-99d7b6de009b&city_code=110000&sort=2&page=1&keywords=%E8%A5%BF%E4%BA%8C%E6%97%97&model=Nexus+6',
        'shangDi':'http://www.webapi.ziroom.com/v7/room/list.json?sign=3786e77103639fc299450c628ced7788&size=10&timestamp=1492420810&feature=3&os=android%3A7.0&network=WIFI&sign_open=1&app_version=5.2.0&price=%2C&imei=354112070288845&ip=10.33.73.63&uid=d41432db-068e-f467-f6c9-99d7b6de009b&city_code=110000&sort=2&page=1&keywords=%E4%B8%8A%E5%9C%B0&model=Nexus+6',
        'huiLongGuanPage1':'http://www.webapi.ziroom.com/v7/room/list.json?sign=d63f3eff10fd9ac7e86ece78a29fb9f0&size=10&subway_station_code=%E5%9B%9E%E9%BE%99%E8%A7%82&timestamp=1492421068&feature=3&os=android%3A7.0&network=WIFI&sign_open=1&app_version=5.2.0&price=%2C&imei=354112070288845&subway_code=13%E5%8F%B7%E7%BA%BF&ip=10.33.73.63&uid=d41432db-068e-f467-f6c9-99d7b6de009b&city_code=110000&sort=2&page=1&model=Nexus+6',
        'huiLongGuanPage2':'http://www.webapi.ziroom.com/v7/room/list.json?sign=247c975d07cda0eb387e1a947cf1ade9&size=10&subway_station_code=%E5%9B%9E%E9%BE%99%E8%A7%82&timestamp=1492421103&feature=3&os=android%3A7.0&network=WIFI&sign_open=1&app_version=5.2.0&price=%2C&imei=354112070288845&subway_code=13%E5%8F%B7%E7%BA%BF&ip=10.33.73.63&uid=d41432db-068e-f467-f6c9-99d7b6de009b&city_code=110000&sort=2&page=2&model=Nexus+6',
        'maLianWa':'http://www.webapi.ziroom.com/v7/room/list.json?suggestion_value=%E9%A9%AC%E8%BF%9E%E6%B4%BC&sign=0ebddb2bd2a9bbb568f65f1339c90592&size=10&timestamp=1492421823&feature=3&os=android%3A7.0&network=WIFI&sign_open=1&app_version=5.2.0&price=%2C&imei=354112070288845&ip=10.33.73.63&uid=d41432db-068e-f467-f6c9-99d7b6de009b&suggestion_type=1&city_code=110000&sort=2&page=1&model=Nexus+6'}
RoomMap={}
corpID = 'wxf978c2c23fa5a8c7'
corpSecret = 's0elqeqQzPVY9RFW4BrzbydrR8gVZRsceFVM2cU8HsY0C0wmNyqm77lE6iE1lbif'
def sendMsg(msgContent):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corpID,corpSecret)
    ret = urllib2.urlopen(url).read()
    retJson = json.loads(ret)
    token = retJson.get('access_token')
    if(token == ''):
        return
    #construct request data
    msgContent = "%s at %s" % (msgContent,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    data = {
        "touser" :"zhangjingyi",
        "toparty" : "",
        "totag":"",
        "msgtype":"text",
        "agentid":"0",
        "text":{
            "content":msgContent
        }
    }
    data = simplejson.dumps(data,ensure_ascii=False)
    res = urllib2.urlopen('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % (token),data).read()
    print res


def getHouses():
    for label in pathMap:
        r = requests.get(pathMap[label])
        res = json.loads(r.text)
        rooms =  res['data']['rooms']
        for room in rooms:
            cnt = RoomMap.get(room['id'], 0)
            if cnt == 0:
                print 'new'
                RoomMap[room['id']] =  1
                sendMsg(label +  room['id'])
            else:
                print room['id']
                print cnt
                RoomMap[room['id']] =  cnt + 1



#polling web pages & check if matchs
def polling():
    while(True):
        getHouses()
        time.sleep(random.randint(3,15))

if __name__ == '__main__':
# send msg to users when checkMatch return true
    polling()
