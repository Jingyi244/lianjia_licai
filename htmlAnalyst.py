# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import subprocess
import time
import json
import urllib2
import urllib
import simplejson

htmlPath = '/Users/zhangjingyi/lianjia_licai/licai.html'
jsPath = '/Users/zhangjingyi/lianjia_licai/licai.js'
corpID = 'wxf978c2c23fa5a8c7'
corpSecret = 's0elqeqQzPVY9RFW4BrzbydrR8gVZRsceFVM2cU8HsY0C0wmNyqm77lE6iE1lbif'

# send msg to users when checkMatch return true
def sendMsg(msgContent):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corpID,corpSecret)
    ret = urllib2.urlopen(url).read()
    retJson = json.loads(ret)
    token = retJson.get('access_token')
    if(token == ''):
        return
    #construct request data
    msgContent = "%s is aviable at %s" % (msgContent,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    data = {
        "touser" :"@all",
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

#check match result
def checkMatch():
    f = open(htmlPath)
    soup = BeautifulSoup(f.read())
    f.close()
    tbody = soup.tbody
    rows = tbody.find_all('tr')
    bids = []
    for row in rows:
        tds = row.find_all('td')
        bid = {}
        bid['name'] = tds[0].a.string
        bid['duration'] = tds[2].span.string
        bid['status'] = tds[5].string
        bids.append(bid)
    for bid in bids:
        if((bid['duration'] == u'180') and bid['status'] != u'已售罄'):
            return bid['name']
    return 'NOT AVAIBLE'


def getPage():
    return subprocess.call(['phantomjs',jsPath])

#polling web pages & check if matchs
def polling():
    while(True):
        print 'running'
        ret = getPage()
        if(ret != 0):
            continue
        ret = checkMatch()
        if(ret != 'NOT AVAIBLE'):
            sendMsg(ret.split('-')[1])
        time.sleep(150)

if __name__ == '__main__':
    polling()
