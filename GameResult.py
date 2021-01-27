class GameResult(object):
    def __init__(self, s, a, r, s2, t):
        self.s = s
        self.a = a
        self.r = r
        self.s2 = s2
        self.t = t

    def to_record(self):  # sqliteに保存できるタイプのレコードに変更
        s = "".join([str(i) for i in self.s])
        a = self.a
        r = self.r
        s2 = "".join([str(i) for i in self.s2])
        t = self.t

        return [s, a, r, s2, t]

    @classmethod
    def record_to_game_result(cls, record):
        s = [int(i) for i in list(record[0])]
        a = record[1]
        r = record[2]
        s2 = [int(i) for i in list(record[3])]
        t = record[4]
        return GameResult(s, a, r, s2, t)
