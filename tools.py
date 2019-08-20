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
    word_data = bus.read_word_data(address_adt7410, register_adt7410)
    data = (word_data & 0xff00) >> 8 | (world_data & 0xff) << 8
    data = data >> 3
    if data & 0x1000 == 0:
        return data * 0.0625
    else:
        return ((~data&0x1fff) + 1) * -0.0625

# 電源の設定(ON, OFF)
def setPower(isOn):
    pass
