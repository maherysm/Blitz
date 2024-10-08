from card import Card
import random
import pygame
from constants import *

class Player():

    def __init__(self, playerNum):
        self.score = 0
        self.font = pygame.font.SysFont("comicsansms", 48)
        self.deck = []
        for i in range(0, 10):
            self.deck.append(Card("G", i + 1, "F", "green_" + str(i + 1) + ".png", 0, 0))
        for i in range(10, 20):
            self.deck.append(Card("Y", i + 1 - 10, "F", "yellow_" + str(i + 1 - 10) + ".png", 0, 0))
        for i in range(20, 30):
            self.deck.append(Card("R", i + 1 - 20, "M", "red_" + str(i + 1 - 20) + ".png", 0, 0))
        for i in range(30, 40):
            self.deck.append(Card("B", i + 1 - 30, "M", "blue_" + str(i + 1 - 30) + ".png", 0, 0))
        # [G1, G2, G3, G4, G5, G6, G7, G8, G9, G10,
        # R1, R2, R3, R4, R5, R6, R7, R8, R9, R10,
        # B1, B2, B3, B4, B5, B6, B7, B8, B9, B10,
        # Y1, Y2, Y3, Y4, Y5, Y6, Y7, Y8, Y9, Y10]
        self.playerNum = playerNum
        if playerNum == 1:
            self.rotationDirection = 0
        elif playerNum == 2:
            self.rotationDirection = 180
        elif playerNum == 3:
            self.rotationDirection = 270
        elif playerNum == 4:
            self.rotationDirection = 90

        self.blitzPile = []  # List of 10 cards
        self.postPile1 = []
        self.postPile2 = []
        self.postPile3 = []
        self.postPiles = [self.postPile1, self.postPile2, self.postPile3]
        self.woodPile = []
        self.cardSelected = False
        self.selectedCard = 0
        self.selectedCardIndexOnGameBoard = -1

    # self{}, screen{surface}, cardLocations{list of 5 tuples}
    def displayPlayerCards(self, screen, pileIndex):
        #if the below 5 cards exist, they will be printed to the screen in their designated locations, but only after
        #they are rotated the correct amount for each player
        if self.woodPile:
            screen.blit(pygame.transform.rotate(self.woodPile[0].image, self.rotationDirection), pileIndex[4])
        if self.blitzPile:
            screen.blit(pygame.transform.rotate(self.blitzPile[0].image, self.rotationDirection), pileIndex[3])
        if self.postPiles[0]:
            screen.blit(pygame.transform.rotate(self.postPiles[0][0].image, self.rotationDirection), pileIndex[0])
        if self.postPiles[1]:
            screen.blit(pygame.transform.rotate(self.postPiles[1][0].image, self.rotationDirection), pileIndex[1])
        if self.postPiles[2]:
            screen.blit(pygame.transform.rotate(self.postPiles[2][0].image, self.rotationDirection), pileIndex[2])

    # given the index, returns a card object if it is there. Otherwise, dont return anything
    def findSelectedCard(self, pileIndex):
        if pileIndex == 4:
            if len(self.woodPile) > 0:
                return self.woodPile[0]
        if pileIndex == 3:
            if len(self.blitzPile) > 0:
                return self.blitzPile[0]
        if pileIndex in range(0, 3):
            if len(self.postPiles[pileIndex]) > 0:
                return self.postPiles[pileIndex][0]

    def shuffleDeck(self):
        random.shuffle(self.deck)

    # Creates initial blitz pile and your three initial cards in stacking pile
    def createInitialHand(self, board):
        for x in range(10):
            self.blitzPile.append(self.deck.pop(0))
        self.postPiles[0].append(self.deck.pop(0))
        self.postPiles[1].append(self.deck.pop(0))
        self.postPiles[2].append(self.deck.pop(0))

    # returns true if the card attempted to stack is opposite gender and descending
    # number from the stack pile
    def postAttempt(self, card, cardToStack):
        if cardToStack.gender != (card.gender):
            if cardToStack.number == (card.number - 1):
                return True
        return False

    def postResultForPostPile(self, condition, postPileIndexFrom, postPileIndexTo):
        # if the stack is valid
        if condition:
            # inserts the top card from the grabbing pile into the placing pile
            (self.postPiles[postPileIndexTo]).insert(0, self.postPiles[postPileIndexFrom][0])
            # removes the "top" element from the grabbing pile
            self.postPiles[postPileIndexFrom].pop(0)

            # if the pile that was grabbed from is empty, replace with a card from the blitz pile
            if len(self.postPiles[postPileIndexFrom]) == 0:
                (self.postPiles[postPileIndexFrom]).insert(0, self.blitzPile[0])
                self.blitzPile.pop(0)

    def postResultForBlitzPile(self, condition, postPileIndex):
        # if the stack is valid
        if condition:
            # inserts the top card from the grabbing pile into the placing pile
            (self.postPiles[postPileIndex]).insert(0, self.blitzPile[0])
            # removes the "top" element from the grabbing pile
            self.blitzPile.pop(0)

    def postResultForWoodPile(self, condition, postPileIndex):
        # if the stack is valid
        if condition:
            # inserts the top card from the grabbing pile into the placing pile
            (self.postPiles[postPileIndex]).insert(0, self.woodPile.pop(0))
            # removes the "top" element from the grabbing pile

    # parameters:
    # stackingPileNum: which stacking pile that the card was taken from
    # gamePileNum: The pile that you are trying to place the card on top of (to gain a point)
    def playAttempt(self, board, dutchPileIndex, cardToPlay):
        # self.stackingPiles[stackingPileNum][0] is the card at top of stacking pile
        if (cardToPlay.number == 1):
            # if you are trying to place the card on an empty spot in the game board
            if len(board.dutchPiles[dutchPileIndex]) == 0:
                self.score = self.score + 1
                return True
        # if you try to place a card thats not 0 on an empty pile
        elif len(board.dutchPiles[dutchPileIndex]) == 0:
            return False
        # if the color of the cards are the same
        elif cardToPlay.color == board.dutchPiles[dutchPileIndex][0].color:
            # if the number is one greater than the card you are placing on
            if cardToPlay.number == ((board.dutchPiles[dutchPileIndex][0].number) + 1):
                self.score = self.score + 1
                return True

        return False

    def playResultForPostPile(self, condition, board, dutchPileIndex, postPileIndex):
        if condition:
            # inserts the card onto the spot on the gameboard that was attempted
            board.dutchPiles[dutchPileIndex].insert(0, self.postPiles[postPileIndex][0])
            # removes the card from the stackPile
            self.postPiles[postPileIndex].pop(0)
            if len(self.postPiles[postPileIndex]) == 0:
                if len(self.blitzPile) > 0:
                    (self.postPiles[postPileIndex]).insert(0, self.blitzPile.pop(0))

    def playResultForWoodPile(self, condition, board, dutchPileIndex):
        if condition:
            # inserts the card onto the spot on the gameboard that was attempted
            board.dutchPiles[dutchPileIndex].insert(0, self.woodPile.pop(0))
            # removes the card from the stackPile

    def playResultForBlitzPile(self, condition, board, dutchPileIndex):
        if condition:
            # inserts the card onto the spot on the gameboard that was attempted
            board.dutchPiles[dutchPileIndex].insert(0, self.blitzPile.pop(0))
            # removes the card from the stackPile

    # Flips 3 Cards from player deck and puts them in place pile
    def flipWoodPile(self):

        # if the deck as less than 3 cards, flip the wood pile, and put it at the bottom of the deck
        if len(self.deck) < 3:
            self.woodPile.reverse()
            for i in range(len(self.woodPile)):
                self.deck.append(self.woodPile.pop(0))

        # if the deck has at least 3 cards, flip them in the wood pile
        for i in range(3):
            self.woodPile.insert(0, self.deck.pop(0))

    def displayScore(self, screen):
        text = self.font.render(str(len(self.blitzPile)), True, (0, 0, 0))
        screen.blit(text, BLITZ_SCORE_COORDS[self.playerNum - 1])
        text = self.font.render(str(self.score), True, (0, 0, 0))
        screen.blit(text, (PLAYED_SCORE_COORDS[self.playerNum - 1]))