from urllib import request
import ConfigParser
import time
import threading
import json

config = ConfigParser.ConfigParser()
config.read('settings.ini')
if config.has_section('url') and config.has_section('token') == False:
    print('Setting Parameters are not defined!')
    exit(1)

url = config.get('url', 'ur;')

data = {
    'token': config.get('token', 'token')
}

headers = {
    'Content-Type': 'application/json'
}

while True:
    req = request.Request(url, json.dumps(data).encode(), headers)
    with request.urlopen(req) as res:
        body = json.loads(res.read().decode('utf8'))
        task = Task(body)        
        
    time.sleep(1)
