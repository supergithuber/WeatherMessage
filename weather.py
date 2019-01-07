# -*- coding:UTF-8 -*-

import requests
import json
import sys
import os
from twilio.rest import Client
from git import Repo


reload(sys)
sys.setdefaultencoding('utf-8')

## 配置项目路径
PROJECT_PATH = "/root/Documents/pyProject/WeatherMessage"

## git 部分


## 天气部分

def saveToFile(location, message):
    fileName = PROJECT_PATH + "/" + location + ".txt"
    with open(fileName, "a") as f:
        message = message + ",\n"
        f.write(message.encode("gbk"))
        f.close()
    return None

def pushToRemote():
    ## 如果使用crond配置定时任务，这里要配置绝对路径，否则就用currentPath取代absolutePath
    currentPath = os.getcwd()

    repo = Repo(PROJECT_PATH)
    git = repo.git
    git.add([PROJECT_PATH + '/'])
    git.commit('-m', 'get today weather')
    repo.remotes.origin.pull()
    repo.remotes.origin.push()
    return None

def getWeather():
    xinzhi_apiKey = "junmywaobnqxw8zl"
    location = "shenzhen"
    url = "https://api.thinkpage.cn/v3/weather/daily.json?key=%s&location=%s&language=zh-Hans&unit=c&start=0&days=2" % (xinzhi_apiKey, location)
    # 获取天气预报信息
    # 此处只取今天和明天2天的预报
    r = requests.get(url)
    w = r.json()["results"][0]["daily"]

    todayJsonString = json.dumps(w[0], ensure_ascii=False)
    saveToFile(location, todayJsonString)


    today = "今天是%s，白天%s，晚上%s，气温%s-%s" % (w[0]["date"], w[0]["text_day"], w[0]["text_night"], w[0]["high"], w[0]["low"])
    tomorrow = "明天是%s，白天%s，晚上%s，气温%s-%s" % (w[1]["date"], w[1]["text_day"], w[1]["text_night"], w[1]["high"], w[1]["low"])
    message = tomorrow
    return message

def sendMessage(message):
    # 设置twilio账户信息
    twilio_account_sid = "AC5bf3f9be7a84e1dc1555ee11b06d38ec"
    twilio_auth_token = "b3f2f395c3d6fc51c842cd46a4d73b3f"
    client = Client(twilio_account_sid, twilio_auth_token)

    # 注意to和from_两个参数所代表的手机号，都需要带有国家代码。如中国大陆手机号即+86开头再加上自己的手机号。from_中的号码直接复制twilio提供的号码即可
    client.messages.create(to="+8615626474791", from_="+18508208255", body=message)
    return None

if __name__ == "__main__":
    weather = getWeather()
    print(weather)
    # pushToRemote()
    sendMessage(weather)