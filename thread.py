from tools import getTemp, getWeight, TTS, sevenSeg  
import time
import threading

class Task:
    json = {}
    now = 0
    lock = False

    def __init__(self, json):
        self.json = json

    def next(self):
        if self.lock == False:
            self.now = self.now + 1
        else:
            # 強制履行の警告
            TTS('ボタンをもう一回押すと次のステージに移動します')
            self.lock = False

    def excute(self):
        while self.json['steps'][self.now] != None:
            step = self.json['steps'][self.now]
            
            # TTSで読み上げ処理
            TTS(step['description'])
            self.lock = True

            if step['type'] == 'heat':
                # 加熱処理
                start = time.time()
                while time.time() - start < step['duration']:
                    if now != self.now:
                        break
                    temp = getTemp()
                    if step['heat_strength'] + 5 < temp:
                        setPower(False)
                    elif step['heat_strength'] - 5 > temp:
                        setPower(True)
                    setPower(True)
                    time.sleep(0.1)
                setPower(False)
                self.lock = False
            else:
                # 追加処理
                while True:
                    start = time.time()
                    if now != self.now:
                        break

                    weight = getWeight()
                    sevenSeg(weight)
                    if step['add_grams'] - 10 < weight and step['add_grams'] + 10 > weight:
                        self.lock = False
                    else:
                        if start % 15 == 0:
                            if step['add_gram'] > weight:
                                TTS('あと{}グラムを入れてください'.format(step['add_grams'] - weight))
                            else:
                                TTS('あと{}グラムを抜いてください'.format(weight - step['add_grams']))
                        self.lock = True
                    time.sleep(0.1)
            self.now = self.now + 1
