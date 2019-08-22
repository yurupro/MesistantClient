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
        self.tools.setPower(True)
        time.sleep(2)
        self.tools.setPower(False)
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
                    if step['heat_strength'] + 5 < temp:
                        self.tools.setPower(False)
                    elif step['heat_strength'] - 5 > temp:
                        self.tools.setPower(True)
                    time.sleep(0.1)
                self.tools.setPower(False)
                
            elif step['type'] == 'add':
                # 追加処理
                weight_previous = 0
                count = 0
                weight_zero = 0
                self.tools.TTS("調整中です。デバイスを動かさないでください。")
                while True:
                    if abs(self.tools.getWeight() - weight_previous) < 15:
                        self.tools.TTS("調整完了しました。")
                        weight_zero = self.tools.getWeight()
                        print("weight_zero: {}".format(weight_zero))
                        break
                    weight_previous = self.tools.getWeight()
                    time.sleep(1)
                self.tools.TTS(step['description'])
                time.sleep(2)
                while self.isContinue:
                    print("--")

                    weight = self.tools.getWeight() - weight_zero
                    print("Zero: {}C".format(weight_zero))
                    print("Now: {}C".format(weight))
                    print("Difer from previous: {}C".format(abs(weight - weight_previous)))
                    if abs(weight - weight_previous) < 15:
                        if step['add_grams'] - 15 < weight and step['add_grams'] + 15 > weight:
                            self.tools.TTS('{}グラム。適量です。'.format(math.floor(step['add_grams'] - weight)))
                            break
                        else:
                            if count % 5 == 0:
                                if step['add_grams'] > weight:
                                    self.tools.TTS('あと{}グラムを入れてください'.format(math.floor(step['add_grams'] - weight)))
                                else:
                                    self.tools.TTS('あと{}グラムを抜いてください'.format(math.floor(weight - step['add_grams'])))
                    weight_previous = weight
                    count += 1
                    time.sleep(1)
            else:
                while self.isContinue:
                    time.sleep(0.1)

            self.now = self.now + 1
        self.isContinue = True
        self.tools.TTS('料理が出来上がりました！')
