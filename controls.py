import pygame
from constants import *

class Controls:
    @staticmethod
    def mouseInArea(mouseCoords, topLeftCoord, objSize):
        x_in_range = topLeftCoord[0] <= mouseCoords[0] <= topLeftCoord[0] + objSize[0]
        y_in_range = topLeftCoord[1] <= mouseCoords[1] <= topLeftCoord[1] + objSize[1]
        return x_in_range and y_in_range

    def hoveringOverCard(self, mouseCoords, playerCoords):
        for i, coord in enumerate(playerCoords):
            if self.mouseInArea(mouseCoords, coord, (CARD_SIZE_X, CARD_SIZE_Y)):
                return i
        return -1

    @staticmethod
    def leftButtonClick():
        return pygame.mouse.get_pressed(3)[0]

    @staticmethod
    def rightButtonClick():
        return pygame.mouse.get_pressed(3)[2]

    @staticmethod
    def getMousePos():
        return pygame.mouse.get_pos()
