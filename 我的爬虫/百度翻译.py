# 百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8

import hashlib
import http.client
import json
import random
import urllib

appid = '20201013000588180'  # 填写你的appid
secretKey = 'ke6GkrLjSywGXXMKx5cu'  # 填写你的密钥

httpClient = None
myurl = '/api/trans/vip/translate'

fromLang = 'auto'  # 原文语种
toLang = 'zh'  # 译文语种
salt = random.randint(32768, 65536)
q = 'apple'  # 原文
sign = appid + q + str(salt) + secretKey
sign = hashlib.md5(sign.encode()).hexdigest()

myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
    q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign


def get():
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        print(result)
        trans_result = result['trans_result'][0]['dst']
        print(trans_result)

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


def post():
    form_data = {
        'fromLang': fromLang,
        'toLang': toLang,
        'to': 'zh',
        'appid': appid,
        'selectKey': secretKey,
        'q': q,
        'sign': sign,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('POST', myurl, body=form_data)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        print(result)
        trans_result = result['trans_result'][0]['dst']
        print(trans_result)

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


if __name__ == '__main__':
    post()
