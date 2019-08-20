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
    data = int((hex(int("b406b5"+str(hex(Atemp[0])[2:])+str(hex(Atemp[1])[2:]),16)) )[:-1],16)
    
    data =data <<8
    length = len(bin(data)[2:])
    for i in range(length):
            if int(bin(data)[2:3],2) == 1 : #MSB =1
                    nokori = bin(data)[11:]
                    sentou = (int(bin(data)[2:11],2)) ^ (int('100000111',2))
                    data = int((str(bin(sentou)[2:11])+str(nokori)),2)
            data=int(bin(data),2)
            if len(str(bin(data)[2:]))<9:
                    return(hex(data))
    return crc8atm(data),"<-calculated"

# 電源の設定(ON, OFF)
def setPower(isOn):
    pass
