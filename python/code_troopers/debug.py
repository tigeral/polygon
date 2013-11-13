"""
This package provide some tool for effective debugging of my strategy in CodeTroopers game.
Work both with local-runner and Repeater tools.
"""

from threading import Thread
from time import sleep
from pygame.rect import Rect

from model.BonusType import BonusType
from model.Move import Move
from model.CellType import CellType
from model.TrooperType import TrooperType

import math
import pygame


class DebuggerWindow(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.me = []
        self.world = []
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

    def println(self, text):
        textSurface = self.font.render("%s" % text, 1, Color.black)
        textCoord = (self.textOutCoord[0], self.textOutCoord[1] + self.font.get_height() * self.textLineNo)
        self.canvas.blit(textSurface, textCoord)
        self.textLineNo += 1

    def log(self, me, world, data):
        if hasattr(world, "isReplay") and world.isReplay:
            return

        if self.historyPoint == len(self.data) - 1:
            self.isPaused = False
        self.me.append(me)
        self.world.append(world)
        self.data.append(data)

        self.isDirty = True

    def draw(self):
        #read data to quick access
        me = self.me[self.historyPoint]
        world = self.world[self.historyPoint]
        data = self.data[self.historyPoint]

        #clear canvas
        self.canvas.fill(Color.white)
        self.textLineNo = 0

        #draw grid with heights map. Draw this data only once to gameFieldCanvas and then just copy it to self.canvas
        if not hasattr(self, 'mapCanvas'):
            self.gameFieldCanvas = pygame.Surface((self.canvasWidth, self.canvasHeight))
            self.drawGameField(self.gameFieldCanvas, world)
        self.canvas.blit(self.gameFieldCanvas, (0, 0))

        #draw bonuses
        for bonus in world.bonuses:
            self.drawBonus(self.canvas, bonus)

        #draw units
        for unit in world.troopers:
            self.drawUnit(self.canvas, unit)

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

    def drawUnit(self, canvas, unit):
        #load bonuses image file
        if not hasattr(self, 'unitsImage'):
            self.unitsImage = pygame.image.load_extended('units.png')
        unitBufCanvas = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
        #draw player color
        if unit.teammate:
            pygame.draw.circle(unitBufCanvas, Color.green, (25, 25), 13)
        else:
            pygame.draw.circle(unitBufCanvas, Color.red, (25, 25), 13)
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
        #draw to canvas
        x = unit.x * _cellSize - 10
        y = unit.y * _cellSize - 10
        canvas.blit(unitBufCanvas, (x, y))

    def drawBonus(self, canvas, bonus):
        #load bonuses image file
        if not hasattr(self, 'bonusesImage'):
            self.bonusesImage = pygame.image.load_extended('bonuses.png')

        x = bonus.x * _cellSize + 3
        y = bonus.y * _cellSize + 5
        #draw bonus type image
        if bonus.type is BonusType.GRENADE:
            canvas.blit(self.bonusesImage, (x, y), (0, 0, 25, 20))
        elif bonus.type is BonusType.MEDIKIT:
            canvas.blit(self.bonusesImage, (x, y), (0, 20, 25, 20))
        elif bonus.type is BonusType.FIELD_RATION:
            canvas.blit(self.bonusesImage, (x, y), (0, 40, 25, 20))

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
        self.data[self.historyPoint].globalStrategy.move(self.me[self.historyPoint], world, Move())

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


_cellSize = 30
_footerHeight = 20
_textBlockWidth = 400
_textBlockPadding = 5
_maxTrackLineItemsCount = 200
_playPauseBtnWidth = 20
_playPauseBtnHeight = _footerHeight
