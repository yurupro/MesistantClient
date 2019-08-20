import serial
import smbus

# 7Segmentに出力
def sevenSeg(number):
    s = serial.Serial('', 9600)
    s.write(str(number))

# 読みあげ
def TTS(string):
    pass

# 重さ測定
def getWeight():
    pass

# 温度測定
def getTemp():
    i2c = smbus.SMBus(1)
    addr=0x5a
    
    Atemp = i2c.read_i2c_block_data(addr,0x6,3)
    Otemp1 = i2c.read_i2c_block_data(addr,0x7,3)
    AmbientTemp = ((Atemp[1]*256 + Atemp[0]) *0.02 -273.15)
    ObjectTemp1 = ((Otemp1[1]*256 + Otemp1[0]) *0.02 -273.15)
    return ObjectTemp1

# 電源の設定(ON, OFF)
def setPower(isOn):
    pass
