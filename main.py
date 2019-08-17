from urllib import request
import ConfigParser
import time
import json
from multiprocessing import Process
import RPi.GPIO as GPIO

BUTTON_PIN = 1

# Reading settings from config file
config = ConfigParser.ConfigParser()
config.read('settings.ini')
if config.has_section('url') and config.has_section('authentication') == False:
    print('Setting Parameters are not defined!')
    exit(1)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=nextButton, bouncetime=300)

url = config.get('url', 'fetch')

data = {
    'token': config.get('authentication', 'token')
}

headers = {
    'Content-Type': 'application/json'
}

p = None
task = None

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
    p.join()

def nextButton(channel):
    if task != None:
        task.isContinue = False
