from urllib import request
import configparser
import time
import json

config = configparser.ConfigParser()
config.read('settings.ini')
if config.has_section('url') and config.has_section('authentication') == False:
    print('Setting Parameters are not defined!')
    exit(1)

url = config.get('url', 'register')

data = {
    'user_id': config.get('authentication', 'id')
}

headers = {
    'Content-Type': 'application/json'
}

req = request.Request(url, json.dumps(data).encode(), headers)
with request.urlopen(req) as res:
    try:
        body = json.loads(res.read().decode('utf8'))
        device_id = body['id']
        config.set('authentication', 'device_id', device_id)
        print('デバイスの登録を完了しました')
    except urllib.HTTPError as err:
        print('デバイス登録に失敗しました')

with open('settings.ini', 'w') as file:
    config.write(file)
