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
        self.tools.setPower(False)
        while len(self.json['steps']) > self.now :
            print("Step"+str(self.now)+" Length: "+ str(len(self.json['steps'])))
            step = self.json['steps'][self.now]
            

            if step['type'] == 'heat':
                count = 0
                # TTSで読み上げ処理
                self.tools.TTS(step['description'])
                # 温度維持
                self.tools.TTS("{}秒間熱します。".format(step['duration']))
                start = time.time()
                print("----")
                print(time.time() - start)
                self.isContinue = True
                print(self.isContinue)
                while time.time() - start < step['duration'] and self.isContinue:
                    print(self.tools.getTemp())
                    temp = self.tools.getTemp()
                    if step['heat_strength'] + 1 < temp:
                        self.tools.setPower(False)
                    elif step['heat_strength'] - 1 > temp:
                        self.tools.setPower(True)
                        time.sleep(0.1)
                        self.isContinue = True
                    time.sleep(1)
                self.tools.setPower(False)
                time.sleep(0.1)
                self.isContinue = True
                
            elif step['type'] == 'add':
                # 追加処理
                # TTSで読み上げ処理
                self.tools.TTS(step['description'])

                weight_previous = 0
                count = 0
                self.tools.beep()
                self.tools.tareWeight()

                self.isContinue = True
                print(self.isContinue)
                while self.isContinue:
                    print("--")

                    weight = self.tools.getWeight()
                    print("Now: {}C".format(weight))
                    print("Difer from previous: {}C".format(abs(weight - weight_previous)))
                    if abs(weight - weight_previous) < 3:
                        if step['add_grams'] - 15 < weight and step['add_grams'] + 15 > weight:
                            self.tools.beep()
                            self.tools.TTS('{}グラム。適量です。'.format(math.floor(weight)))
                            break
                    if count % 4 == 0:
                        self.tools.TTS('{}グラム'.format(math.floor(weight)))
                    weight_previous = weight
                    count += 1
                    time.sleep(1)
            else:
                self.tools.TTS(step['description'])
                self.tools.TTS('完了しましたらボタンを押してください。')
                self.isContinue = True
                while self.isContinue:
                    time.sleep(0.1)

            time.sleep(2)
            self.now = self.now + 1
        self.tools.TTS('料理が出来上がりました！')
        






    def record(self):
        count = 0
        self.json = {}
        self.json["steps"] = []
        zero_temp = self.tools.getTemp()

        def recordTemp():
            print("温度を記録")
            self.tools.beep()
            self.tools.TTS("加熱処理を記録します")
            self.isContinue = True
            while True:
                # print("温度変化: {}".format(self.tools.getTemp() - zero_temp))
                if not self.isContinue:
                    self.json["steps"].append({
                        "type": "heat",
                        "description": "加熱する",
                        "heat_strength": math.floor(self.tools.getTemp()),
                        })
                    self.tools.TTS("ステップ{}、加熱処理を完了します。".format(str(len(self.json["steps"])+1)))
                    zero_temp = self.tools.getTemp()
                    break
                time.sleep(1)
            time.sleep(4)

        def recordWeight(): 
            print("重量を記録")
            self.tools.TTS("追加処理を記録します")
            self.isContinue = True
            while True:
                print("重量変化: {}".format(self.tools.getWeight()))
                if not self.isContinue:
                    self.json["steps"].append({
                        "type": "add",
                        "description": "追加する",
                        "add_grams": math.floor(self.tools.getWeight()),
                        })
                    self.tools.tareWeight()
                    self.tools.TTS("ステップ{}、追加処理を完了します。".format(str(len(self.json["steps"])+1)))
                    break
                time.sleep(1)

        while True:
            self.tools.TTS("作業を開始してください。")
            start = time.time()
            zero_temp = self.tools.getTemp()
            self.tools.tareWeight()
            self.isContinue = True
            while True:
                self.isContinue = True
                # self.tools.TTS("ステップ"+str(len(self.json["steps"])+1))
                print("温度変化: {}".format(self.tools.getTemp() - zero_temp))
                print("重量変化: {}".format(self.tools.getWeight()))
                if self.tools.getTemp() - zero_temp > 10:
                    recordTemp()

                elif self.tools.getWeight() > 50:
                    recordWeight()
                elif not self.isContinue:
                    self.tools.TTS("記録を終了します。")
                    print(self.json)
                    self.isContinue = True
                    return self.json
                time.sleep(1)
