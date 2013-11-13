from model.ActionType import ActionType
from model.Direction import Direction
from model.Game import Game
from model.Move import Move
from model.Trooper import Trooper
from model.TrooperStance import TrooperStance
from model.World import World

from SimpleStrategy import SimpleStrategy


class MyStrategy:
    strategy = None

    def __init__(self):
        self.strategy = SimpleStrategy()

    def move(self, me, world, game, move):
        self.strategy.move(me, world, game, move)
