import serial
import smbus
import RPi.GPIO as GPIO
from hx711 import HX711
import os
import urllib, pycurl

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
        self.hx.set_reference_unit(self.referenceUnit)
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

    # 7Segmentに出力
    def sevenSeg(self, number):
        s = serial.Serial('', 9600)
        s.write(str(number))

    # 読みあげ
    def TTS(self, string):
        print("Say: " + string)
        googleTranslateURL = "http://translate.google.com/translate_tts?tl=ja&"
        parameters = {'q': string}
        data = urllib.parse.urlencode(parameters)
        url = "%s%s" % (googleTranslateURL,data)
        
        fp = open(self.AUDIO_PATH, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEDATA, fp)
        curl.perform()
        curl.close()
        fp.close()

        os.system("mplayer tmp.mp3 -af extrastereo=0 &")
        
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
