"""
This package provide some tool for effective debugging of my strategy in CodeTroopers game.
Work both with local-runner and Repeater tools.
"""

from threading import Thread
from time import sleep
import numpy
from pygame.rect import Rect
from model.ActionType import ActionType
from model.Direction import Direction

from model.BonusType import BonusType
from model.Move import Move
from model.CellType import CellType
from model.TrooperStance import TrooperStance
from model.TrooperType import TrooperType

import math
import pygame


# noinspection PyArgumentList
class Color():
    red = (255,  50, 50)
    green = (50,  255, 50)
    blue = (50,  50,  255)
    black = (0,   0,   0)
    white = (255, 255, 255)
    gray = (200, 200, 200, 200)
    dirtyGreen = (200, 255, 200)
    sludge = (150, 100, 50)

    def _fromHex(self, hexColor):
        return (hexColor >> 16) & 0xff, (hexColor >> 8) & 0xff, hexColor & 0xff

    gridDottedLine = _fromHex(None, 0xaaaaaa)
    lowObstacle = _fromHex(None, 0xcfcfcf)
    mediumObstacle = _fromHex(None, 0x9f9f9f)
    highObstacle = _fromHex(None, 0x6f6f6f)
    lowVisibility = _fromHex(None, 0xaaaaff)
    midVisibility = _fromHex(None, 0x8888ff)
    fullVisibility = _fromHex(None, 0x5555ff)
    healAction = _fromHex(None, 0x88ff88)
    attackAction = _fromHex(None, 0xff8888)
    moveAction = _fromHex(None, 0x000000)
    activeTrooperIndicator = _fromHex(None, 0xbbbbbb)


class DebuggerWindow(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.game = None
        self.me = []
        self.world = []
        self.move = []
        self.data = []
        self.historyPoint = 0
        self.trackMouseDown = False
        self.isReplay = False
        self.isPaused = False

    def run(self):
        while True:
            if len(self.data) > 0:
                break
            sleep(1)
            continue

        pygame.init()
        pygame.font.init()
        self.gameWidth = int(self.world[0].width * _cellSize)
        self.gameHeight = int(self.world[0].height * _cellSize)
        self.canvasWidth = self.gameWidth + _textBlockWidth
        self.canvasHeight = self.gameHeight + _footerHeight
        self.trackLineSize = _maxTrackLineItemsCount
        self.trackLinePos = 0
        self.trackLineWidth = self.canvasWidth - _playPauseBtnWidth
        self.trackLineHeight = _footerHeight
        self.playPauseBtnWidth = _playPauseBtnWidth
        self.playPauseBtnHeight = _playPauseBtnHeight
        self.canvas = pygame.display.set_mode((self.canvasWidth, self.canvasHeight))
        self.font = pygame.font.SysFont('Courier New', 14)
        self.textLineNo = 0
        self.textOutCoord = (self.gameWidth + _textBlockPadding, _textBlockPadding)
        self.isDirty = False

        clock = pygame.time.Clock()
        while True:
            if not self.isPaused and self.historyPoint < len(self.data) - 1:
                self.historyPoint += 1
                self.isDirty = True
            else:
                self.isPaused = True

            if self.historyPoint < 0:
                self.historyPoint = 0
            if self.historyPoint >= len(self.data):
                self.historyPoint = len(self.data) - 1
            if self.data[self.historyPoint] is None:
                for i in range(self.historyPoint, 0, -1):
                    if self.data[i] is not None:
                        self.historyPoint = i
                        break

            if self.isDirty:
                self.draw()

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # self.checkAndProcessTankDetails()
                    self.checkAndProcessTrackLine()
                    self.checkAndProcessPlayPauseBtn()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.trackMouseDown = False
                if event.type == pygame.MOUSEMOTION and self.trackMouseDown:
                    self.checkAndProcessTrackLine()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.historyPoint -= 1
                    self.isDirty = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.historyPoint += 1
                    self.isDirty = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.replay()

            clock.tick(60)

    def println(self, text, color=Color.black):
        textSurface = self.font.render("%s" % text, 1, color)
        textCoord = (self.textOutCoord[0], self.textOutCoord[1] + self.font.get_height() * self.textLineNo)
        self.canvas.blit(textSurface, textCoord)
        self.textLineNo += 1

    def log(self, me, world, game, move, data):
        if hasattr(world, "isReplay") and world.isReplay:
            return

        if self.historyPoint == len(self.data) - 1:
            self.isPaused = False
        self.me.append(me)
        self.game = game
        self.move.append(move)
        self.world.append(world)
        self.data.append(data)

        self.isDirty = True

    def draw(self):
        #read data to quick access
        game = self.game
        me = self.me[self.historyPoint]
        world = self.world[self.historyPoint]
        move = self.move[self.historyPoint]
        data = self.data[self.historyPoint]

        #clear canvas
        self.canvas.fill(Color.white)
        self.textLineNo = 0

        #draw grid with heights map. Draw this data only once to gameFieldCanvas and then just copy it to self.canvas
        if not hasattr(self, 'mapCanvas'):
            self.gameFieldCanvas = pygame.Surface((self.canvasWidth, self.canvasHeight))
            self.drawGameField(self.gameFieldCanvas, world)
        self.canvas.blit(self.gameFieldCanvas, (0, 0))

        self.highlightVisibleArea(self.canvas, world)

        #draw bonuses
        for bonus in world.bonuses:
            self.drawBonus(self.canvas, bonus)

        #draw units
        for unit in world.troopers:
            self.drawUnit(self.canvas, unit, me)

        #draw action
        self.drawAction(self.canvas, move, me, world, game)

        #draw text data
        self.println("Global strategy: " + data.strategy.name)
        self.println("turn #%s" % world.move_index)
        self.println("history point #%s" % self.historyPoint)

        #draw text from data log
        for logItem in data.log:
            self.println(logItem)

        #draw history navigation progress bar
        self.drawTrackLine()

        pygame.display.flip()
        self.isDirty = False

    def drawUnit(self, canvas, unit, me):
        #load bonuses image file
        if not hasattr(self, 'unitsImage'):
            self.unitsImage = pygame.image.load_extended('res/units.png')
        unitBufCanvas = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
        #draw player color
        if unit.teammate:
            pygame.draw.circle(unitBufCanvas, Color.green, (25, 25), 0)
        else:
            pygame.draw.circle(unitBufCanvas, Color.red, (25, 25), 0)
        #copy image according to trooper type
        if unit.type is TrooperType.COMMANDER:
            unitBufCanvas.blit(self.unitsImage, (15, 14), (0, 0, 35, 22))
        elif unit.type is TrooperType.FIELD_MEDIC:
            unitBufCanvas.blit(self.unitsImage, (15, 14), (0, 22, 35, 22))
        elif unit.type is TrooperType.SOLDIER:
            unitBufCanvas.blit(self.unitsImage, (15, 14), (0, 44, 35, 22))
        elif unit.type is TrooperType.SNIPER:
            unitBufCanvas.blit(self.unitsImage, (15, 14), (0, 66, 35, 22))
        elif unit.type is TrooperType.SCOUT:
            unitBufCanvas.blit(self.unitsImage, (15, 14), (0, 88, 35, 22))
        #draw health indicator
        if unit.hitpoints > unit.maximal_hitpoints:
            extraHitPoints = unit.hitpoints - unit.maximal_hitpoints
            pygame.draw.rect(unitBufCanvas, Color.green, (10, 10, 30, 6), 0)
            pygame.draw.rect(unitBufCanvas, Color.blue, (10, 10, extraHitPoints * 30 / unit.maximal_hitpoints, 6), 0)
        else:
            pygame.draw.rect(unitBufCanvas, Color.green, (10, 10, unit.hitpoints * 30 / unit.maximal_hitpoints, 6), 0)
        pygame.draw.rect(unitBufCanvas, Color.gray, (10, 10, 30, 6), 1)
        #draw owned bonuses
        if unit.holding_grenade:
            unitBufCanvas.blit(self.unitsImage, (12, 32), (0, 110, 8, 8))
        if unit.holding_medikit:
            unitBufCanvas.blit(self.unitsImage, (24, 32), (8, 110, 8, 8))
        if unit.holding_field_ration:
            unitBufCanvas.blit(self.unitsImage, (36, 32), (16, 110, 8, 8))
        #draw indicator if it's an active trooper
        if unit.id == me.id:
            pygame.draw.lines(unitBufCanvas, Color.activeTrooperIndicator, True, [(20, 0), (28, 0), (24, 5)], 10)
            pygame.draw.lines(unitBufCanvas, Color.activeTrooperIndicator, True, [(23, 6), (27, 6), (25, 8)], 3)
            pygame.draw.lines(unitBufCanvas, Color.black, True, [(15, 0), (35, 0), (25, 10)], 1)
        #draw to canvas
        x = unit.x * _cellSize - 10
        y = unit.y * _cellSize - 10
        canvas.blit(unitBufCanvas, (x, y))

    def drawBonus(self, canvas, bonus):
        #load bonuses image file
        if not hasattr(self, 'bonusesImage'):
            self.bonusesImage = pygame.image.load_extended('res/bonuses.png')

        x = bonus.x * _cellSize + 3
        y = bonus.y * _cellSize + 5
        #draw bonus type image
        if bonus.type is BonusType.GRENADE:
            canvas.blit(self.bonusesImage, (x, y), (0, 0, 25, 20))
        elif bonus.type is BonusType.MEDIKIT:
            canvas.blit(self.bonusesImage, (x, y), (0, 20, 25, 20))
        elif bonus.type is BonusType.FIELD_RATION:
            canvas.blit(self.bonusesImage, (x, y), (0, 40, 25, 20))

    # noinspection PyStringFormat
    def drawAction(self, canvas, move, me, world, game):
        col, row, actionPoints, hitPoints, damage, trooperType, stance, newStance = (0, 0, 0, 0, 0, '', '', '')
        # determine which cell will be affected by this action
        if move.direction:
            if move.direction is Direction.NORTH:
                row = me.x
                col = me.y - 1
            elif move.direction is Direction.EAST:
                row = me.x + 1
                col = me.y
            elif move.direction is Direction.SOUTH:
                row = me.x
                col = me.y + 1
            elif move.direction is Direction.WEST:
                row = me.x - 1
                col = me.y
        else:
            row = move.x
            col = move.y
        # determine if some trooper is placed in target cell
        target = None
        for trooper in world.troopers:
            if trooper.x == col and trooper.y == row:
                target = trooper
        if move.action is ActionType.MOVE:
            if me.stance is TrooperStance.STANDING:
                actionPoints = me.action_points - game.standing_move_cost
            elif me.stance is TrooperStance.KNEELING:
                actionPoints = me.action_points - game.kneeling_move_cost
            elif me.stance is TrooperStance.PRONE:
                actionPoints = me.action_points - game.prone_move_cost
            self.println('action: move')
            self.println('action points: %d -> %d' % (me.action_points, actionPoints))
            self.highlightTargetCell(canvas, row, col, Color.moveAction)
        elif move.action is ActionType.SHOOT:
            if me.stance is TrooperStance.STANDING:
                actionPoints = me.action_points - game.standing_move_cost
                damage = me.standing_damage
            elif me.stance is TrooperStance.KNEELING:
                actionPoints = me.action_points - game.kneeling_move_cost
                damage = me.kneeling_damage
            elif me.stance is TrooperStance.PRONE:
                actionPoints = me.action_points - game.prone_move_cost
                damage = me.prone_damage
            hitPoints = target.hitpoints - damage
            self.println('action: shoot')
            self.println('hit points: %d -> %d' % (target.hitpoints, hitPoints) + '(dead)' if hitPoints <= 0 else '')
            self.println('action points: %d -> %d' % (me.action_points, actionPoints))
            self.highlightTargetCell(canvas, row, col, Color.attackAction)
        elif move.action is ActionType.THROW_GRENADE:
            actionPoints = me.action_points - game.grenade_throw_cost
            self.println('action: throw grenade')
            for trooper in world.troopers:
                if numpy.absolute(trooper.x - col) + numpy.absolute(trooper.y - row) == 0:
                    damage = game.grenade_direct_damage
                elif numpy.absolute(trooper.x - col) + numpy.absolute(trooper.y - row) == 0:
                    damage = game.grenade_collateral_damage
                else:
                    continue
                hitPoints = trooper.hitpoints - damage
                if trooper.type is TrooperType.COMMANDER:
                    trooperType = 'commander'
                elif trooper.type is TrooperType.FIELD_MEDIC:
                    trooperType = 'medic'
                elif trooper.type is TrooperType.SCOUT:
                    trooperType = 'scout'
                elif trooper.type is TrooperType.SNIPER:
                    trooperType = 'sniper'
                elif trooper.type is TrooperType.SOLDIER:
                    trooperType = 'soldier'
                self.println('%s HP: %d -> %d' % (trooperType, trooper.hitpoints, hitPoints)
                             + '(dead)' if trooper.hitpoints - damage <= 0 else '')
            self.println('action points: %d -> %d' % (me.action_points, actionPoints))
            self.highlightTargetCell(canvas, row, col, Color.attackAction)
            self.highlightTargetCell(canvas, row + 1, col, Color.attackAction)
            self.highlightTargetCell(canvas, row, col + 1, Color.attackAction)
            self.highlightTargetCell(canvas, row - 1, col, Color.attackAction)
            self.highlightTargetCell(canvas, row, col - 1, Color.attackAction)
        elif move.action is ActionType.EAT_FIELD_RATION:
            actionPoints = me.action_points + game.field_ration_bonus_action_points - game.field_ration_eat_cost
            self.println('action: eat ration')
            self.println('action points: %d -> %d' % (me.action_points, actionPoints))
        elif move.action is ActionType.END_TURN:
            self.println('--- end turn ---')
            self.println('action points: %d' % me.action_points)
        elif move.action is ActionType.USE_MEDIKIT:
            if target.id == me.id:
                hitPoints = numpy.minimum(me.hitpoints + game.medikit_heal_self_bonus_hitpoints, me.maximal_hitpoints)
            else:
                hitPoints = numpy.minimum(target.hitpoints + game.medikit_bonus_hitpoints, target.maximal_hitpoints)
            self.println('action: use medikit')
            self.println('hit points: %d -> %d' % (target.hitpoints, hitPoints))
            self.println('action points: %d -> %d' % (me.action_points, me.action_points - game.medikit_use_cost))
            self.highlightTargetCell(canvas, row, col, Color.healAction)
        elif move.action is ActionType.HEAL:
            if target.id == me.id:
                hitPoints = numpy.minimum(me.hitpoints + game.field_medic_heal_self_bonus_hitpoints,
                                          me.maximal_hitpoints)
            else:
                hitPoints = numpy.minimum(target.hitpoints + game.field_medic_heal_bonus_hitpoints,
                                          target.maximal_hitpoints)
            self.println('action: heal')
            self.println('hit points: %d -> %d' % (target.hitpoints, hitPoints))
            self.println('action points: %d -> %d' % (me.action_points, me.action_points - game.field_medic_heal_cost))
            self.highlightTargetCell(canvas, row, col, Color.healAction)
        elif move.action is ActionType.LOWER_STANCE:
            if me.stance is TrooperStance.STANDING:
                stance = 'standing'
                newStance = 'kneeling'
            elif me.stance is TrooperStance.KNEELING:
                stance = 'kneeling'
                newStance = 'prone'
            self.println('action: lower stance')
            self.println('stance: %s -> %s' % (stance, newStance))
            self.println('action points: %d -> %d' % (me.action_points, me.action_points - game.stance_change_cost))
        elif move.action is ActionType.RAISE_STANCE:
            if me.stance is TrooperStance.KNEELING:
                stance = 'kneeling'
                newStance = 'standing'
            elif me.stance is TrooperStance.PRONE:
                stance = 'prone'
                newStance = 'kneeling'
            self.println('action: raise stance')
            self.println('stance: %s -> %s' % (stance, newStance))
            self.println('action points: %d -> %d' % (me.action_points, me.action_points - game.stance_change_cost))
        elif move.action is ActionType.REQUEST_ENEMY_DISPOSITION:
            self.println('action: request enemy disposition')
            self.println('action points: %d -> %d' %
                         (me.action_points, me.action_points - game.commander_request_enemy_disposition_cost))

    def highlightVisibleArea(self, canvas, world):
        myTroopers = []
        for trooper in world.troopers:
            if trooper.teammate:
                myTroopers.append(trooper)
        for row in range(0, world.height):
            for col in range(0, world.width):
                if world.cells[col][row] is CellType.FREE:
                    visibility = 3  # trooper stance STANDING + 1
                    for trooper in myTroopers:
                        for targetStance in range(visibility - 1, 0, -1):
                            if world.is_visible(trooper.vision_range, trooper.x, trooper.y, trooper.stance,
                                                col, row, targetStance):
                                visibility = targetStance
                            else:
                                break
                    if visibility is 0:
                        color = Color.fullVisibility
                    elif visibility is 1:
                        color = Color.midVisibility
                    elif visibility is 2:
                        color = Color.lowVisibility
                    else:
                        continue
                    pygame.draw.rect(canvas, color,
                                     (col * _cellSize + 1, row * _cellSize + 1, _cellSize - 2, _cellSize - 2), 0)

    def highlightTargetCell(self, canvas, row, col, color):
        lineLength = 10
        pygame.draw.line(canvas, color, (col * _cellSize, row * _cellSize),
                                        (col * _cellSize + lineLength, row * _cellSize), 1)
        pygame.draw.line(canvas, color, ((col + 1) * _cellSize - lineLength, row * _cellSize),
                                        ((col + 1) * _cellSize, row * _cellSize), 1)
        pygame.draw.line(canvas, color, ((col + 1) * _cellSize, row * _cellSize),
                                        ((col + 1) * _cellSize, row * _cellSize + lineLength), 1)
        pygame.draw.line(canvas, color, ((col + 1) * _cellSize, (row + 1) * _cellSize - lineLength),
                                        ((col + 1) * _cellSize, (row + 1) * _cellSize), 1)
        pygame.draw.line(canvas, color, ((col + 1) * _cellSize, (row + 1) * _cellSize),
                                        ((col + 1) * _cellSize - lineLength, (row + 1) * _cellSize), 1)
        pygame.draw.line(canvas, color, (col * _cellSize + lineLength, (row + 1) * _cellSize),
                                        (col * _cellSize, (row + 1) * _cellSize), 1)
        pygame.draw.line(canvas, color, (col * _cellSize, (row + 1) * _cellSize),
                                        (col * _cellSize, (row + 1) * _cellSize - lineLength), 1)
        pygame.draw.line(canvas, color, (col * _cellSize, row * _cellSize + lineLength),
                                        (col * _cellSize, row * _cellSize), 1)

    def drawGameField(self, canvas, world):
        canvas.fill(Color.white)
        #draw grid
        for row in range(0, world.height):
            drawDottedLine(canvas, Color.gray, (0, row * _cellSize),
                           (self.gameWidth, row * _cellSize), 5)
        for col in range(0, world.width):
            drawDottedLine(canvas, Color.gridDottedLine, (col * _cellSize, 0),
                           (col * _cellSize, self.gameHeight), 5)
        #draw obstacles
        for row in range(0, world.height):
            for col in range(0, world.width):
                cell = world.cells[col][row]
                if cell == CellType.FREE:
                    continue
                elif cell == CellType.LOW_COVER:
                    color = Color.lowObstacle
                elif cell == CellType.MEDIUM_COVER:
                    color = Color.mediumObstacle
                elif cell == CellType.HIGH_COVER:
                    color = Color.highObstacle
                # noinspection PyUnboundLocalVariable
                canvas.fill(color, Rect(col * _cellSize, row * _cellSize, _cellSize, _cellSize))
        #draw game field borders
        pygame.draw.rect(canvas, Color.black, Rect(0, 0, self.gameWidth, self.gameHeight), 1)

    def drawTrackLine(self):
        pygame.draw.rect(self.canvas, Color.gray,
                         (self.playPauseBtnWidth, self.gameHeight, self.trackLineWidth, self.trackLineHeight))
        x = len(self.data) * self.trackLineWidth / self.trackLineSize
        pygame.draw.rect(self.canvas, Color.dirtyGreen,
                         (self.playPauseBtnWidth, self.gameHeight, x, self.trackLineHeight))
        if self.isPaused:
            pygame.draw.polygon(self.canvas, Color.black,
                                ((5, self.gameHeight + 5), (15, self.gameHeight + 10), (5, self.gameHeight + 15)), 3)
        else:
            pygame.draw.line(self.canvas, Color.black, (8, self.gameHeight + 5), (8, self.gameHeight + 15), 3)
            pygame.draw.line(self.canvas, Color.black, (12, self.gameHeight + 5), (12, self.gameHeight + 15), 3)
        x = self.historyPoint * self.trackLineWidth / self.trackLineSize + self.playPauseBtnWidth
        pygame.draw.line(self.canvas, Color.black, (x, self.gameHeight), (x, self.gameHeight + self.trackLineHeight), 3)

    def replay(self):
        world = self.world[self.historyPoint]
        world.isReplay = True
        self.data[self.historyPoint].strategy.move(self.me[self.historyPoint], world, self.game, Move())

    def checkAndProcessTrackLine(self):
        pos = pygame.mouse.get_pos()
        if pos[1] > self.gameHeight:
            if pos[0] <= self.playPauseBtnWidth and self.trackMouseDown:
                self.historyPoint = 0
            elif pos[0] > self.playPauseBtnWidth:
                self.trackMouseDown = True
                self.historyPoint = int((pos[0] - self.playPauseBtnWidth) * self.trackLineSize / self.trackLineWidth)
                self.isPaused = True
            self.isDirty = True
        else:
            self.trackMouseDown = False

    def checkAndProcessPlayPauseBtn(self):
        pos = pygame.mouse.get_pos()
        if pos[1] > self.gameHeight and pos[0] < self.playPauseBtnWidth:
            self.isPaused = not self.isPaused

    def checkAndProcessUnitDetails(self):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.gameWidth or pos[1] > self.gameHeight:
            return

        world = self.world[self.historyPoint]
        for tank in world.tanks:
            if tank.get_distance_to(pos[0], pos[1]) < tank.height:
                self.selectedTankDetails = tank.id
                self.isDirty = True
                return


def drawDottedLine(surface, color, startPoint, endPoint, interval):
    lineLength = int(math.hypot(endPoint[0] - startPoint[0], endPoint[1] - startPoint[1]))
    for posOnLine in range(0, lineLength, interval):
        x = startPoint[0] + int((endPoint[0] - startPoint[0]) * posOnLine / lineLength)
        y = startPoint[1] + int((endPoint[1] - startPoint[1]) * posOnLine / lineLength)
        surface.set_at((x, y), color)


_cellSize = 30
_footerHeight = 20
_textBlockWidth = 400
_textBlockPadding = 5
_maxTrackLineItemsCount = 200
_playPauseBtnWidth = 20
_playPauseBtnHeight = _footerHeight
