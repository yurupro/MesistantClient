from urllib import request
import ConfigParser
import time
import json

config = ConfigParser.ConfigParser()
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
    body = json.loads(res.read().decode('utf8'))
    # エラーの場合の処理は後ほど追加
    device_id = body['id']
    config.set('authentication', 'device_id', device_id)
    print('デバイスの登録を完了しました')

with open('settings.ini', 'w') as file:
    config.write(file)
