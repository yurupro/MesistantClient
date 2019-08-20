import time
import threading

class Task:
    now = 0
    isContinue = True
    
    def __init__(self, json, tools):
        self.json = json
        self.tools = tools

    def execute(self):
        while self.json['steps'][self.now] != None:
            step = self.json['steps'][self.now]
            
            # TTSで読み上げ処理
            self.tools.TTS(step['description'])

            if step['type'] == 'heat':
                # 加熱処理
                start = time.time()
                while time.time() - start < step['duration'] and self.isContinue:
                    temp = self.tools.getTemp()
                    if step['heat_strength'] + 5 < temp:
                        self.tools.setPower(False)
                    elif step['heat_strength'] - 5 > temp:
                        self.tools.setPower(True)
                    time.sleep(0.1)
                self.tools.setPower(False)
                
                # Nextを押すまでに待機
                while self.isContinue:
                    time.sleep(0.1)
            elif step['type'] == 'add':
                # 追加処理
                weight_zero = self.tools.getWeight()
                while self.isContinue:
                    start = time.time()

                    weight = self.tools.getWeight() - weight_zero
                    if step['add_grams'] - 10 < weight and step['add_grams'] + 10 > weight:
                        self.tools.TTS('適量です'.format(step['add_grams'] - weight))
                    else:
                        if start % 15 == 0:
                            if step['add_gram'] > weight:
                                self.tools.TTS('あと{}グラムを入れてください'.format(step['add_grams'] - weight))
                            else:
                                self.tools.TTS('あと{}グラムを抜いてください'.format(weight - step['add_grams']))
                    time.sleep(0.1)
            else:
                while self.isContinue:
                    time.sleep(0.1)

            self.now = self.now + 1
        self.isContinue = True
        self.tools.TTS('料理が出来上がりました！')
