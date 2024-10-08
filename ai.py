from player import Player
import random
import pygame
from constants import *

class AI(Player):
    def __init__(self, playerNum):
        super().__init__(playerNum)
        self.timeDelay = 0
        self.waitTime = 0
        self.index = -1
        self.indexB = -1
        self.indices = (-1, -1)
        self.diffLevel = 1
        self.blitzPlaceAttempt = False
        self.postPilePlaceAttempt = False
        self.woodPilePlaceAttempt = False

    def attemptPlacement(self, board, indexToPlace, cardSource, indexList, playResult):
        if indexToPlace == -1:
            random.shuffle(indexList)
            for x in indexList:
                if len(cardSource) > 0 and self.playAttempt(board, x, cardSource[0]):
                    self.score = max(0, self.score - 1)
                    self.timeDelay = pygame.time.get_ticks()
                    self.waitTime = self.AIwaitTime()
                    return x
            return -1
        elif indexToPlace != -1 and pygame.time.get_ticks() > self.timeDelay + self.waitTime:
            if self.playAttempt(board, indexToPlace, cardSource[0]):
                playResult(True, board, indexToPlace)
            else:
                self.score = max(0, self.score - 1)
            return -1
        return indexToPlace

    def blitzPilePlayAttempt(self, board, dutchPileIndex):
        indexList = list(range(12))
        return self.attemptPlacement(board, dutchPileIndex, self.blitzPile, indexList, self.playResultForBlitzPile)

    def woodPilePlayAttempt(self, board, dutchPileIndex):
        indexList = list(range(12))
        return self.attemptPlacement(board, dutchPileIndex, self.woodPile, indexList, self.playResultForWoodPile)

    def postPilesPlayAttempt(self, board, dutchPileIndex, postPileIndex):
        if postPileIndex == -1:
            stackPileList = list(range(3))
            random.shuffle(stackPileList)
            for y in stackPileList:
                if len(self.postPiles[y]) > 0:
                    self.index = self.attemptPlacement(board, dutchPileIndex, self.postPiles[y], list(range(12)), lambda res, b, i: self.playResultForPostPile(res, b, i, y))
                    if self.index != -1:
                        return self.index, y
            return -1, -1
        elif postPileIndex != -1 and pygame.time.get_ticks() > self.timeDelay + self.waitTime:
            if self.attemptPlacement(board, dutchPileIndex, self.postPiles[postPileIndex], list(range(12)), lambda res, b, i: self.playResultForPostPile(res, b, i, postPileIndex)) == -1:
                return -1, -1
        return dutchPileIndex, postPileIndex

    def playCards(self, board):
        if not self.blitzPlaceAttempt and not self.postPilePlaceAttempt and not self.woodPilePlaceAttempt:
            self.index = self.blitzPilePlayAttempt(board, -1)
            if self.index != -1:
                self.blitzPlaceAttempt = True
        if not self.blitzPlaceAttempt and not self.postPilePlaceAttempt and not self.woodPilePlaceAttempt:
            self.indices = self.postPilesPlayAttempt(board, -1, -1)
            if self.indices != (-1, -1):
                self.postPilePlaceAttempt = True
        if not self.blitzPlaceAttempt and not self.postPilePlaceAttempt and not self.woodPilePlaceAttempt:
            self.indexB = self.woodPilePlayAttempt(board, -1)
            if self.indexB != -1:
                self.woodPilePlaceAttempt = True

        if self.blitzPlaceAttempt:
            if self.blitzPilePlayAttempt(board, self.index) == -1:
                self.index = -1
                self.blitzPlaceAttempt = False
                self.timeDelay = pygame.time.get_ticks()
        elif self.postPilePlaceAttempt:
            self.indices = self.postPilesPlayAttempt(board, self.indices[0], self.indices[1])
            if self.indices[0] == -1:
                self.postPilePlaceAttempt = False
                self.timeDelay = pygame.time.get_ticks()
        elif self.woodPilePlaceAttempt:
            self.indexB = self.woodPilePlayAttempt(board, self.indexB)
            if self.indexB == -1:
                self.woodPilePlaceAttempt = False
                self.timeDelay = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.timeDelay > self.waitTime:
            self.flipWoodPile()
            self.timeDelay = pygame.time.get_ticks()

    def AIwaitTime(self):
        return random.randrange(DIFF_LEVELS[self.diffLevel][0], DIFF_LEVELS[self.diffLevel][1])
