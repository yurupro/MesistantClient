import serial
import smbus
import RPi.GPIO as GPIO
from hx711 import HX711
import configparser
import os
import urllib, pycurl
import base64, json, requests
import math
import time
from mutagen.mp3 import MP3 as mp3

class Tools:
    RELAY_PIN = 17
    BUTTON_PIN = 27
    AUDIO_PATH = 'tmp.mp3'

    def __init__(self, callback):
        # Callback設定
        self.callback = callback
       
        # HX711設定
        self.referenceUnit = 1
        self.hx = HX711(5, 6)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(224)
        self.hx.reset()
        self.hx.tare()

        # 温度センサー
        self.i2c = smbus.SMBus(1)
        self.i2caddr=0x5a
       
        # GPIO設定
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_PIN, GPIO.IN)
        GPIO.add_event_detect(self.BUTTON_PIN, GPIO.FALLING, callback=self.callback, bouncetime=300)
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)

    def isButton(self):
        return GPIO.input(self.BUTTON_PIN)
    # 7Segmentに出力
    def sevenSeg(self, number):
        s = serial.Serial('', 9600)
        s.write(str(number))

    # 読みあげ
    def TTS(self, string):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        key = config.get('authentication', 'tts_key')
        url = "https://texttospeech.googleapis.com/v1beta1/text:synthesize?key=" + key
        print("Say: " + string)
        str_json_data = {
                'input': {
                    'text': string
                    },
                'voice': {
                    'languageCode': 'ja-JP',
                    'name': 'ja-JP-Wavenet-A',
                    'ssmlGender': 'FEMALE'
                    },
                'audioConfig': {
                    'audioEncoding': 'MP3'
                    }
                }
        jd = json.dumps(str_json_data)


        r = requests.post(url, data=jd, headers={'Content-type': 'application/json'})
        if r.status_code == 200:
            parsedBody = json.loads(r.text)
            with open(self.AUDIO_PATH, "wb") as outmp3:
                outmp3.write(base64.b64decode(parsedBody['audioContent']))
            mp3_length = mp3("tmp.mp3").info.length
            os.system("mpg123 tmp.mp3 &")
            time.sleep(mp3_length + 1)# 再生時間分sleep

    def beep(self):
        mp3_length = mp3("beep.mp3").info.length
        os.system("mpg123 beep.mp3 &")
        time.sleep(mp3_length + 1)# 再生時間分sleep
        
    # 重さ風袋調整
    def tareWeight(self):
        self.hx.tare()

    # 重さ測定
    def getWeight(self):
        return self.hx.get_weight(5)

    # 温度測定
    def getTemp(self):
        Atemp = self.i2c.read_i2c_block_data(self.i2caddr,0x6,3)
        Otemp1 = self.i2c.read_i2c_block_data(self.i2caddr,0x7,3)
        AmbientTemp = ((Atemp[1]*256 + Atemp[0]) *0.02 -273.15)
        ObjectTemp1 = ((Otemp1[1]*256 + Otemp1[0]) *0.02 -273.15)
        return round(ObjectTemp1,2)

    # 電源の設定(ON, OFF)
    def setPower(self, isOn):
        if isOn:
            GPIO.output(self.RELAY_PIN, GPIO.HIGH)
        else:
            GPIO.output(self.RELAY_PIN, GPIO.LOW)
