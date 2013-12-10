import copy


class Data:
    MODE_EXPLORE = 0
    MODE_DEFEND = 1
    MODE_SAFE_ATTACK = 2
    MODE_FULL_ATTACK = 3

    __mode = MODE_EXPLORE
    __enemyPlayers = {}
    __enemyTroopers = {}
    __troopersOrderByType = []
    __pathTo = [[[[None for tx in xrange(30)] for ty in xrange(20)] for x in xrange(30)] for y in xrange(20)]
    __cells = [[None for x in xrange(30)] for y in xrange(20)]

    def __init__(self):
        self.mode = Data.__mode
        self.enemyPlayers = Data.__enemyPlayers
        self.enemyTroopers = Data.__enemyTroopers
        self.troopersOrderByType = Data.__troopersOrderByType
        self.pathTo = Data.__pathTo
        self.log = []
        self.requestDisposition = False
        self.greedTargets = []
        self.threatTargets = []
        self.safetyTargets = []

    def clone(self, sourceData):
        self.strategy = sourceData.strategy
        self.mode = sourceData.mode
        self.log = sourceData.log
        Data.__enemyPlayers = copy.deepcopy(Data.__enemyPlayers)
        self.enemyPlayers = Data.__enemyPlayers
        Data.__enemyTroopers = copy.deepcopy(Data.__enemyTroopers)
        self.enemyTroopers = Data.__enemyTroopers
        Data.__pathTo = copy.deepcopy(Data.__pathTo)
        self.pathTo = Data.__pathTo
        Data.__mode = copy.copy(Data.__mode)
        self.mode = Data.__mode
        self.requestDisposition = sourceData.requestDisposition

    def clearCurrent(self, isDebug):
        self.log = []

