from model.ActionType import ActionType
from model.Direction import Direction
from model.Game import Game
from model.Move import Move
from model.Trooper import Trooper
from model.TrooperStance import TrooperStance
from model.TrooperType import TrooperType
from model.World import World

from SimpleStrategy import SimpleStrategy
from CommanderStrategy import CommanderStrategy


class MyStrategy:
    strategy = None

    def __init__(self):
        self.strategy = None

    def move(self, me, world, game, move):
        # initialize strategy according to trooper type
        if not self.strategy:
            if me.type == TrooperType.COMMANDER:
                self.strategy = CommanderStrategy()
            elif me.type == TrooperType.FIELD_MEDIC:
                self.strategy = SimpleStrategy()
            elif me.type == TrooperType.SOLDIER:
                self.strategy = SimpleStrategy()
            elif me.type == TrooperType.SNIPER:
                self.strategy = SimpleStrategy()
            elif me.type == TrooperType.SCOUT:
                self.strategy = SimpleStrategy()

        self.strategy.move(me, world, game, move)
