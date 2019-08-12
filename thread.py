class Task:
    json = {}
    now = 0
    lock = False

    def __init__(self, json):
        self.json = json

    def next(self):
        if lock == False:
            self.now = self.now + 1
        else:
            # 強制履行の警告
            lock = False

    def excute(self):
        step = self.json['steps'][now]

        # TTSで読み上げ処理
        TTS(step['description'])
        lock = True
        if step['type'] == 'heat':
            # 加熱処理
            start = time.time()
            while time.time() - start < step['duration']:
                temp = getTemp()
                if step['heat_strength'] + 5 < temp:
                    setPower(False)
                elif step['heat_strength'] - 5 > temp:
                    setPower(True)

                setPower(True)

            lock = False
        else:
            # 追加処理
            # 重量を測って所定の重量になるまで
            lock = False
