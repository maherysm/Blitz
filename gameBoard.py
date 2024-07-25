import pygame
import os


class GameBoard():
    def __init__(self, fileName, screenWidth, screenHeight):
      self.screenWidth = screenWidth
      self.screenHeight = screenHeight
      self.boardFileName = fileName
      self.boardImage = pygame.image.load(os.path.join('images', self.boardFileName))
      self.dutchPiles = [[], [], [], [], [], [], [], [], [], [], [], []]   #list of up to 12 piles of cards (with up to 10 cards per pile)
      self.usedCards = []   #list of cards

    #checks for and removes piles of 10 from the game board
    def checkForPilesToRemove(self):
      for x in range(len(self.dutchPiles)):
        if len(self.dutchPiles[x]) > 0:
          if (self.dutchPiles[x][0].number == 10):
            for y in range(len(self.dutchPiles[x])):
              self.usedCards.append(self.dutchPiles[x].pop(0))
            self.dutchPiles[x] = []

    def displayCardPiles(self, screen, pileCardCoords):
      for x in range(len(self.dutchPiles)):
        if len(self.dutchPiles[x]) > 0:
          screen.blit(self.dutchPiles[x][0].image, pileCardCoords[x])

