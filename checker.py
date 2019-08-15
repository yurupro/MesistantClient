from urllib import request
import ConfigParser
import time
import json
from multiprocessing import Process

config = ConfigParser.ConfigParser()
config.read('settings.ini')
if config.has_section('url') and config.has_section('authentication') == False:
    print('Setting Parameters are not defined!')
    exit(1)

url = config.get('url', 'fetch')

data = {
    'token': config.get('authentication', 'token')
}

headers = {
    'Content-Type': 'application/json'
}

thread = None
p = None
while True:
    req = request.Request(url, json.dumps(data).encode(), headers)
    with request.urlopen(req) as res:
        body = json.loads(res.read().decode('utf8'))

    # 認証失敗またはリクエストなし
    if body == None:
        continue

    if p != None:
        p.terminate()
    task = Task(body)
    p = Process(target=task.execute())
    p.start()
    
    time.sleep(1)
