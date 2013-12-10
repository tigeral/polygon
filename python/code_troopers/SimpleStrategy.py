from CommonStrategy import CommonStrategy
from model.ActionType import ActionType
from model.TrooperType import TrooperType


class SimpleStrategy(CommonStrategy):
    def __init__(self):
        CommonStrategy.__init__(self)
        self.name = "Simple strategy"
        self.phase = 0
        self.availableTactics = []

    def move(self, me, world, game, move):
        CommonStrategy.move(self, me, world, game, move)
        data = self.data
        if me.type == TrooperType.COMMANDER and world.move_index == 0:
            move.action = ActionType.REQUEST_ENEMY_DISPOSITION
