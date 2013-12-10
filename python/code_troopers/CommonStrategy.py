from collections import deque
from Data import Data
from model.BonusType import BonusType
from model.CellType import CellType
from model.Trooper import Trooper
from model.TrooperType import TrooperType

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
        self.data.clearCurrent(DebuggerWindow is not None)

        self.analyzeWorld(me, world, self.data)
        # implement some more actions here

    def analyzeWorld(self, me, world, data):
        if world.move_index == 0:
            # collect enemyPlayers into separate list
            if not data.enemyPlayers:
                for player in world.players:
                    if player.id != me.player_id:
                        data.enemyPlayers[player.id] = player
            # collect my troopers just for some intermediate data
            myTroopers = []
            for myTrooper in world.troopers:
                if myTrooper.teammate:
                    myTroopers.append(myTrooper)
            # check initial position of players troopers
            if not data.enemyTroopers:
                for myTrooper in myTroopers:
                    for player in data.enemyPlayers.values():
                        trooperId = (player.id - 1) * len(myTroopers) + myTrooper.teammate_index + 1
                        if player.id % 2 != me.player_id % 2:
                            # flip y
                            trooperY = world.height - 1 - myTrooper.y
                        else:
                            trooperY = myTrooper.y
                        if player.id + me.player_id != 5:
                            # flip x
                            trooperX = world.width - 1 - myTrooper.x
                        else:
                            trooperX = myTrooper.x
                        data.enemyTroopers[trooperId] = Trooper(trooperId, trooperX, trooperY, player.id,
                                                                myTrooper.teammate_index, False, myTrooper.type,
                                                                myTrooper.stance, myTrooper.hitpoints,
                                                                myTrooper.maximal_hitpoints, myTrooper.action_points,
                                                                myTrooper.initial_action_points, myTrooper.vision_range,
                                                                myTrooper.shooting_range, myTrooper.shoot_cost,
                                                                myTrooper.standing_damage, myTrooper.kneeling_damage,
                                                                myTrooper.prone_damage, myTrooper.damage,
                                                                myTrooper.holding_grenade, myTrooper.holding_medikit,
                                                                myTrooper.holding_field_ration)
            # remember order in which different types of troopers makes their turn
            data.troopersOrderByType.append(me.type)

        # check if new positions of enemy troopers were disclosed
        for trooper in world.troopers:
            if not trooper.teammate:
                trooper.detectionTurn = world.move_index
                data.enemyTroopers[trooper.id] = trooper

        # calculate greed
        data.

    def getBonusGreedMultiplier(self, bonus, me, world):
        if bonus.type is BonusType.FIELD_RATION:
            result = 10.0  # field_ration general greed ratio
            if me.holding_field_ration:
                return 0
            if me.holding_grenade:
                result *= 2.0
            if me.type is TrooperType.SOLDIER:
                result *= 2.0
        if bonus.type is BonusType.GRENADE:
            result = 10.0
            if me.holding_grenade:
                return 0
            if me.holding_field_ration:
                result *= 2.0
            if me.type is TrooperType.SOLDIER:
                result *= 2.0
        if bonus.type is BonusType.MEDIKIT:
            result = 40.0
            if me.holding_medikit:
                return 0

        # calculate distance multiplier
        path = self.getPathTo(bonus.x, bonus.y, world)
        distance = path[me.x, me.y]
        if distance < 3:
            result *= (3.0 - distance)
        if distance < 7:
            result *= (7.0 - distance) / 4
        else:
            result *= 0.2

    def getPathTo(self, targetX, targetY, world):
        path = self.data.pathTo[targetY][targetX]
        if path[targetX, targetY]:
            return path
        path[targetX, targetY] = 0
        steps = deque([(targetX, targetY)])
        while steps:
            cur = steps.popleft()
            x = cur[0]
            y = cur[0]
            stepIndex = path[x][y]
            if x > 0 and y > 0 and path[x - 1][y - 1] is None and world.cells[x - 1][y - 1] is CellType.FREE:
                steps.append((x - 1, y - 1))
                path[x - 1][y - 1] = stepIndex + 1
            if y > 0 and path[x][y - 1] is None and world.cells[x][y - 1] is CellType.FREE:
                steps.append((x, y - 1))
                path[x][y - 1] = stepIndex + 1
            if x < 29 and y > 0 and path[x + 1][y - 1] is None and world.cells[x + 1][y - 1] is CellType.FREE:
                steps.append((x + 1, y - 1))
                path[x + 1][y - 1] = stepIndex + 1
            if x < 29 and path[x + 1][y] is None and world.cells[x + 1][y] is CellType.FREE:
                steps.append((x + 1, y))
                path[x + 1][y] = stepIndex + 1
            if x < 29 and y < 19 and path[x + 1][y + 1] is None and world.cells[x + 1][y + 1] is CellType.FREE:
                steps.append((x + 1, y + 1))
                path[x + 1][y + 1] = stepIndex + 1
            if y < 19 and path[x][y + 1] is None and world.cells[x][y + 1] is CellType.FREE:
                steps.append((x, y + 1))
                path[x][y + 1] = stepIndex + 1
            if x > 0 and y < 19 and path[x - 1][y + 1] is None and world.cells[x - 1][y + 1] is CellType.FREE:
                steps.append((x - 1, y + 1))
                path[x - 1][y + 1] = stepIndex + 1
            if x > 0 and path[x - 1][y] is None and world.cells[x - 1][y] is CellType.FREE:
                steps.append((x - 1, y))
                path[x - 1][y] = stepIndex + 1
        return path