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

htmlPath = 'http://www.ziroom.com/index.php?_p=map&_a=room&projectcode=1111027377627&jg=&js=&xn%5B%5D=116.3245&xn%5B%5D=40.057187&xb%5B%5D=116.3245&xb%5B%5D=40.070219&dnn%5B%5D=116.37502&dnn%5B%5D=40.057187&db%5B%5D=116.37502&db%5B%5D=40.070219&p=1'
corpID = 'wxf978c2c23fa5a8c7'
corpSecret = 's0elqeqQzPVY9RFW4BrzbydrR8gVZRsceFVM2cU8HsY0C0wmNyqm77lE6iE1lbif'
STATUS = 'failure'
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
        "touser" :"zhangjingyi|lijinqi",
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
    ziroom_path = 'http://interfaces.ziroom.com/index.php?_p=api_mobile&_a=searchHouse'
    r = requests.post(ziroom_path,data={'city_code':'110000',
                                        'length' : 8,
                                        'sort' : -1,
                                        'sign':'1d8e52dbeb0cb84387922423685f5f86',
                                        'uid':'d41432db-068e-f467-f6c9-99d7b6de009b',
                                        'keywords': '空军机械家属院',
                                        'timestamp':'1459251745'
                                        })

    res = json.loads(r.text)
    print res['status']
    return res['status']
#polling web pages & check if matchs
def polling():
    global lastHouseCnt
    while(True):
        houseStatus = getHouseAmount()
        if( STATUS  == houseStatus):
            print 'failure'
        else:
            print 'status changed'
            sendMsg('rent now !!!!!! status: ' + houseStatus)
        time.sleep(random.randint(3,15))

if __name__ == '__main__':
# send msg to users when checkMatch return true
    polling()
    #getHouseAmount()
