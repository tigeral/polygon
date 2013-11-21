from Data import Data
try:
    from debug import DebuggerWindow
    debuggerWindow = DebuggerWindow()
    debuggerWindow.start()
except ImportError:
    DebuggerWindow = None
    pass


class CommonStrategy():
    """
    This class implements some things which are common for any strategy like an analyzing the world common aspects
    and managing debugger window. For example analyze the bonuses or enemy troopers positions etc.
    """
    def __init__(self):
        if debuggerWindow is not None:
            self.debug = debuggerWindow
        self.data = Data()
        self.data.strategy = self

    def move(self, me, world, game, move):
        if DebuggerWindow is not None:
            newData = Data()
            newData.clone(self.data)
            self.data = newData
            self.debug.log(me, world, game, move, newData)
        self.data.clearCurrent()

        self.analyzeWorld(me, world, self.data)
        # implement some more actions here

    def analyzeWorld(self, me, world, data):
        #next lines were added just as an example
        enemyTroopers = []
        for trooper in world.troopers:
            if not trooper.teammate:
                enemyTroopers.append(trooper)
        data.log.append('enemy troopers: ' + str(len(enemyTroopers)))