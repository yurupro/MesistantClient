from urllib import request
import configparser
import time
import json
from multiprocessing import Process
from tools import Tools
from thread import Task

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
        task.isContinue = False

while True:
    req = request.Request(url)
    with request.urlopen(req) as res:
        body = json.loads(res.read().decode('utf8'))

    # 認証失敗またはリクエストなし
    if body == None:
        continue

    if p != None:
        p.terminate()
    tools = Tools(nextButton) 
    task = Task(body, tools)
    p = Process(target=task.execute())
    p.start()
    p.join()

