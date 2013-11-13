
class Data:

    def __init__(self):
        self.players = []

    def clone(self, sourceData):
        self.strategy = sourceData.strategy

    def clearCurrent(self):
        self.log = []
