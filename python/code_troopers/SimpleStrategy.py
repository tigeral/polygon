from CommonStrategy import CommonStrategy


class SimpleStrategy(CommonStrategy):
    def __init__(self):
        CommonStrategy.__init__(self)
        self.name = "Simple strategy"
        self.phase = 0
        self.availableTactics = []

    def move(self, me, world, game, move):
        CommonStrategy.move(self, me, world, game, move)
        data = self.data
        # self.analyzeEnemies(me, world, data)
        #
        # if data.totalThreat > data.totalBonusesAttraction:
        #     data.moveMode = "hide"
        # else:
        #     data.moveMode = "collect"
        # data.log.append("moveMode: %s" % data.moveMode)
        #
        # for tactic in self.tactics:
        #     tactic.move(me, world, move, data)

