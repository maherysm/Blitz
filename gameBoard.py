import pygame
import os

class GameBoard:
    def __init__(self, fileName, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.boardFileName = fileName
        self.boardImage = pygame.image.load(os.path.join('images', self.boardFileName))
        self.dutchPiles = [[] for _ in range(12)]  # list of up to 12 piles of cards (with up to 10 cards per pile)
        self.usedCards = []  # list of cards

    def checkForDutchPilesToRemove(self):
        self.dutchPiles = [pile if not (pile and pile[0].number == 10) else self.removeDutchPile(pile) for pile in self.dutchPiles]

    def removeDutchPile(self, pile):
        self.usedCards.extend(pile)
        return []

    def displayCardPiles(self, screen, pileCardCoords):
        for pile, coord in zip(self.dutchPiles, pileCardCoords):
            if pile:
                screen.blit(pile[0].image, coord)
