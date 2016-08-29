# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import subprocess
import time
import json
import requests
import urllib2
import urllib
import simplejson

htmlPath = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT'
corpID = 'wxf978c2c23fa5a8c7'
corpSecret = 's0elqeqQzPVY9RFW4BrzbydrR8gVZRsceFVM2cU8HsY0C0wmNyqm77lE6iE1lbif'

seat_code_map = {'商务座':'swz_num', '特等座':'', '一等座':'zy_num', '二等座':'ze_num', '高级软卧':'',
                '软卧':'rw_num', '硬卧':'yw_num', '软座':'', '硬座':'yz_num', '无座':'wz_num'}

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
        "touser" :"zhangjingyi|QiQing",
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


def checkTicketStatus(date,from_station,to_station,seat_class='二等座'):
    cur_html_path = htmlPath % (date, from_station, to_station)
    r = requests.get(cur_html_path,verify=False)

    res = json.loads(r.text)
    data =  res['data']
    train_number_map = {}
    for train in data:
        dto = train['queryLeftNewDTO']
        train_number = dto['station_train_code']
        tmp_dict = {}
        tmp_dict['start'] = dto['start_time']
        tmp_dict['canWebBuy'] = dto['canWebBuy']
        tmp_dict['ticketLeftNumbers'] = dto[seat_code_map[seat_class]]
        train_number_map[train_number] = tmp_dict

    dream_train_list = ['G355','G115','G117','G323','G163']
    ret_list = []
    for train in dream_train_list:
        train_info = train_number_map.get(train)
        if train_info is None:
            continue
        if (train_info['ticketLeftNumbers'] != '--') and (train_info['ticketLeftNumbers'] != '无'):
            ret_list.append(train)

    return ret_list

#polling web pages & check if matchs
def polling():
    while(True):

        ava_train_list = checkTicketStatus('2016-09-15','BJP','TMK')
        if(len(ava_train_list) == 0):
            print '还未发售'
        else:
            print '可以购买'
            sendMsg('order now, 2016-09-15 Beijing->Taian ' + str(ava_train_list) + ' is avilable')

        time.sleep(150)

if __name__ == '__main__':
# send msg to users when checkMatch return true
    polling()
