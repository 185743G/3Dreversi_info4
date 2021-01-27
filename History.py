class History(object):
    def __init__(self):
        self.gameResults = []

    def addGameResults(self, gameResult):
        self.gameResults.append(gameResult)

    def setGameResults(self, gameResults):
        self.gameResults = gameResults