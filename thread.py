import time
import threading
import math

class Task:
    now = 0
    isContinue = True
    
    def __init__(self, json, tools):
        self.json = json
        self.tools = tools

    def execute(self):
        while len(self.json['steps']) > self.now :
            print("Step"+str(self.now)+" Length: "+ str(len(self.json['steps'])))
            step = self.json['steps'][self.now]
            
            # TTSで読み上げ処理
            self.tools.TTS(step['description'])

            if step['type'] == 'heat':
                # 加熱処理
                while self.tools.getTemp() <= step['heat_strength']-5:
                    print(self.tools.getTemp())
                    self.tools.setPower(True)

                # 温度維持
                start = time.time()
                while time.time() - start < step['duration'] and self.isContinue:
                    print(self.tools.getTemp())
                    temp = self.tools.getTemp()
                    if step['heat_strength'] + 1 < temp:
                        self.tools.setPower(False)
                    elif step['heat_strength'] - 1 > temp:
                        self.tools.setPower(True)
                    time.sleep(0.1)
                self.tools.setPower(False)
                
            elif step['type'] == 'add':
                # 追加処理
                weight_previous = 0
                count = 0
                self.tools.TTS("調整中です。デバイスを動かさないでください。")
                time.sleep(3)
                self.tools.beep()
                self.tools.tareWeight()
                self.tools.TTS(step['description'])
                time.sleep(3)
                while self.isContinue:
                    print("--")

                    weight = self.tools.getWeight()
                    print("Now: {}C".format(weight))
                    print("Difer from previous: {}C".format(abs(weight - weight_previous)))
                    self.tools.TTS('{}グラム'.format(math.floor(weight)))
                    if abs(weight - weight_previous) < 3:
                        if step['add_grams'] - 15 < weight and step['add_grams'] + 15 > weight:
                            self.tools.TTS('{}グラム。適量です。'.format(math.floor(step['add_grams'] - weight)))
                            self.tools.beep()
                            break
                    weight_previous = weight
                    count += 1
                    time.sleep(1)
            else:
                while self.isContinue:
                    time.sleep(0.1)

            time.sleep(2)
            self.now = self.now + 1
        self.isContinue = True
        self.tools.TTS('料理が出来上がりました！')
