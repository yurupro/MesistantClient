import serial
import smbus
import RPi.GPIO as GPIO
from hx711 import HX711

# 7Segmentに出力
def sevenSeg(number):
    s = serial.Serial('', 9600)
    s.write(str(number))

# 読みあげ
def TTS(string):
    pass

# 重さ測定
def getWeight():
    referenceUnit = 1
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()

    return hx.get_weight(5)

# 温度測定
def getTemp():
    i2c = smbus.SMBus(1)
    addr=0x5a
    
    Atemp = i2c.read_i2c_block_data(addr,0x6,3)
    Otemp1 = i2c.read_i2c_block_data(addr,0x7,3)
    AmbientTemp = ((Atemp[1]*256 + Atemp[0]) *0.02 -273.15)
    ObjectTemp1 = ((Otemp1[1]*256 + Otemp1[0]) *0.02 -273.15)
    return round(ObjectTemp1,2)

# 電源の設定(ON, OFF)
def setPower(isOn):
    RELAY_PIN = 17

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)

    if isOn:
        GPIO.output(RELAY_PIN, GPIO.HIGH)
    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)
