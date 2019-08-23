from urllib import request
import configparser
import time
import json
from multiprocessing import Process
from tools import Tools
from thread import Task
from record import Record

# Reading settings from config file
config = configparser.ConfigParser()
config.read('settings.ini')
if config.has_section('url') and config.has_section('authentication') == False:
    print('Setting Parameters are not defined!')
    exit(1)


url = config.get('url', 'fetch').format(config.get('authentication', 'device_id'))

p = None
task = None

def nextButton(channel):
    if task != None:
        print("aaaaa")
        task.isContinue = False

tools = Tools(nextButton) 
tools.beep()

time.sleep(1)
while True:
    if tools.isButton() == 1:
        tools.TTS("レシピアップロードモードだお")
        task = Task({}, tools)
        uploadJSON = task.record()

        uploadUrl = config.get('url', 'upload')
        userID = config.get('authentication', 'id')
        uploadJSON['user_id'] = userID
        uploadJSON['name'] = "デバイスからアップロードされたレシピ"
        print(uploadJSON)
        req = request.Request(
            uploadUrl,
            data=json.dumps(uploadJSON).encode(),
            method="POST",
            headers={'Content-type': 'application/json'}
        )
        with request.urlopen(req) as res:
            print(res)
            if res.getcode() == 200:
                tools.TTS("アップロード完了")
        
    else:
        tools.TTS("レシピダウンロードモードだお")
        time.sleep(3)
        req = request.Request(url)
        with request.urlopen(req) as res:
            body = json.loads(res.read().decode('utf8'))

        # 認証失敗またはリクエストなし
        print(res)
        if body == None:
            continue

        if p != None:
            p.terminate()
        print(tools.isButton())
        task = Task(body, tools)
        p = Process(target=task.execute())
        p.start()
        p.join()

