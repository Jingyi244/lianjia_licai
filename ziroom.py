# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import subprocess
import time
import json
import requests
import urllib2
import urllib
import simplejson

htmlPath = 'http://www.ziroom.com/index.php?_p=map&_a=room&projectcode=1111027377627&jg=&js=&xn%5B%5D=116.3245&xn%5B%5D=40.057187&xb%5B%5D=116.3245&xb%5B%5D=40.070219&dnn%5B%5D=116.37502&dnn%5B%5D=40.057187&db%5B%5D=116.37502&db%5B%5D=40.070219&p=1'
corpID = 'wxf978c2c23fa5a8c7'
corpSecret = 's0elqeqQzPVY9RFW4BrzbydrR8gVZRsceFVM2cU8HsY0C0wmNyqm77lE6iE1lbif'
lastHouseCnt = 0
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


def getPageLen():
    src = urllib2.urlopen(htmlPath).read()
    retJson = json.loads(src)
    length = len(retJson['list'])
    return length
def getHouseAmount():
    ziroom_path = 'http://interfaces.ziroom.com/index.php?_p=api_mobile&_a=get_houseList_by_xiaoqu'
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
    data =  res['data']
    for d in data:
        if d['house_code'] == '60095205':
            status = d['house_tags'][4]
    print status

#polling web pages & check if matchs
def polling():
    global lastHouseCnt
    while(True):
        houseCnt = getHouseAmount()
        if(lastHouseCnt == houseCnt):
            print 'no new house found'
        elif(lastHouseCnt < houseCnt):
            print 'new house found'
            sendMsg('new house found, now ' + str(houseCnt))
            lastHouseCnt = houseCnt
        else:
            print 'house rented'
            lastHouseCnt = houseCnt
        time.sleep(150)

if __name__ == '__main__':
# send msg to users when checkMatch return true
    getHouseAmount() 
