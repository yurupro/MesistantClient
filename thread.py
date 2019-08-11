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

    def exec(self):
        step = self.json['stpes'][now]

        # TTSで読み上げ処理

        lock = True
        if step['type'] == 'heat':
            # 加熱処理
            lock = False
        else:
            # 追加処理
            # 重量を測って所定の重量になるまで
            lock = False
