import pygame
import os
from constants import *
from gameBoard import GameBoard
from player import Player
from ai import AI
from controls import Controls
from sounds import Sounds
from setupScreen import SetupScreen

##################################################################################
pygame.init()
sound = Sounds()

titleImage = pygame.image.load(os.path.join(TITLE_SCREEN))
winImage = pygame.image.load(os.path.join('images', END_SCREENS[0]))
loseImage = pygame.image.load(os.path.join('images', END_SCREENS[1]))
playButtonImage = pygame.image.load(os.path.join('images/buttons', PLAY_BUTTON))
playButtonClickedImage = pygame.image.load(os.path.join('images/buttons', PLAY_BUTTON_CLICKED))
FlipButtonImage = pygame.image.load(os.path.join('images/buttons', FLIP_BUTTON))
FlipButtonClickedImage = pygame.image.load(os.path.join('images/buttons', FLIP_BUTTON_CLICKED))


##################################################################################

def start():
    darkOrLightState = 0
    board = [GameBoard(GAME_BOARD_IMAGES[0], SCREEN_WIDTH, SCREEN_HEIGHT),
             GameBoard(GAME_BOARD_IMAGES[1], SCREEN_WIDTH, SCREEN_HEIGHT)]

    player1 = Player(1)
    player1.shuffleDeck()
    player1.createInitialHand(board[darkOrLightState])
    controls = Controls()

    player2 = AI(2)
    player2.shuffleDeck()
    player2.createInitialHand(board[darkOrLightState])

    player3 = AI(3)
    player3.shuffleDeck()
    player3.createInitialHand(board[darkOrLightState])

    player4 = AI(4)
    player4.shuffleDeck()
    player4.createInitialHand(board[darkOrLightState])

    return board, player1, player2, player3, player4, controls


def game(screen, sound, board, player1, player2, player3, player4, controls):
    runGame = True
    gameEnded = False
    clock = pygame.time.Clock()
    darkOrLightState = 0

    while runGame and not gameEnded:
        clock.tick(60)
        screen.fill((0, 0, 0))
        screen.blit(board[darkOrLightState].boardImage, (0, 0))
        screen.blit(FlipButtonImage, FLIP_BUTTON_COORDS)
        player1.displayPlayerCards(screen, P1_CARD_COORDS)
        player2.displayPlayerCards(screen, P2_CARD_COORDS)
        player3.displayPlayerCards(screen, P3_CARD_COORDS)
        player4.displayPlayerCards(screen, P4_CARD_COORDS)
        board[darkOrLightState].displayCardPiles(screen, PILE_CARD_COORDS)

        player1.displayScore(screen)
        player2.displayScore(screen)
        player3.displayScore(screen)
        player4.displayScore(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
                pygame.quit()

        # if the mouse is clicked and no card is selected
        if controls.leftButtonClick() and player1.selectedCardIndexOnGameBoard == -1:
            mousePos = controls.getMousePos()
            player1.selectedCardIndexOnGameBoard = controls.hoveringOverCard(mousePos, P1_CARD_COORDS)

            # if the mouse is on top of a valid card spot (index 0-4)
            if player1.selectedCardIndexOnGameBoard in range(0, 5):
                # if there is a card to select
                if (player1.findSelectedCard(player1.selectedCardIndexOnGameBoard)):
                    # card object stored
                    player1.selectedCard = player1.findSelectedCard(player1.selectedCardIndexOnGameBoard)
                    player1.cardSelected = True
            # Checks to see if mouse clicked the flip button
            elif controls.mouseInArea(mousePos, FLIP_BUTTON_COORDS, FLIP_BUTTON_SIZE):
                sound.buttonClick.play()

                screen.blit(FlipButtonClickedImage, FLIP_BUTTON_COORDS)
                pygame.display.update()
                pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
                screen.blit(FlipButtonImage, FLIP_BUTTON_COORDS)
                pygame.display.update()
                player1.flipWoodPile()

        # if the mouse is clicked and a card is selected, it will try to place the card down
        if controls.leftButtonClick() and player1.cardSelected:
            mousePos = controls.getMousePos()
            placeDownPosIndex = controls.hoveringOverCard(mousePos, PILE_CARD_COORDS)
            # Returns index of stacking pile you are trying to place on top of
            stackingPosIndex = controls.hoveringOverCard(mousePos, P1_CARD_COORDS)

            # if hovering over cards on the game pile
            if placeDownPosIndex in range(0, 12):
                # if the play attempt is valid
                if player1.playAttempt(board[darkOrLightState], placeDownPosIndex, player1.selectedCard):
                    if player1.selectedCardIndexOnGameBoard in range(0, 3):
                        player1.playResultForPostPile(True, board[darkOrLightState], placeDownPosIndex,
                                                      (player1.selectedCardIndexOnGameBoard))
                    if player1.selectedCardIndexOnGameBoard == 4:
                        player1.playResultForWoodPile(True, board[darkOrLightState], placeDownPosIndex)
                    if player1.selectedCardIndexOnGameBoard == 3:
                        player1.playResultForBlitzPile(True, board[darkOrLightState], placeDownPosIndex)
                    sound.cardPlace.play()
                    player1.selectedCardIndexOnGameBoard = -1
                    player1.cardSelected = False
                    pygame.time.wait(250)

            # if hovering over cards in the stacking pile
            elif stackingPosIndex in range(0, 3):
                if player1.postAttempt(player1.postPiles[stackingPosIndex][0], player1.selectedCard):
                    if player1.selectedCardIndexOnGameBoard in range(0, 3):
                        player1.postResultForPostPile(True, player1.selectedCardIndexOnGameBoard,
                                                      stackingPosIndex)
                    if player1.selectedCardIndexOnGameBoard == 4:
                        player1.postResultForWoodPile(True, stackingPosIndex)
                    if player1.selectedCardIndexOnGameBoard == 3:
                        player1.postResultForBlitzPile(True, stackingPosIndex)
                    sound.cardPlace.play()
                    player1.selectedCardIndexOnGameBoard = -1
                    player1.cardSelected = False
                    pygame.time.wait(250)

        if controls.rightButtonClick():
            player1.selectedCardIndexOnGameBoard = -1
            player1.cardSelected = False

        # if the card is selected, the card will move around the screen with the cursor
        if player1.cardSelected:
            mousePos = controls.getMousePos()
            clickedCardPos = (mousePos[0] - 74 / 2, mousePos[1] - 108 / 2)
            screen.blit(player1.selectedCard.image, clickedCardPos)

        player2.playCards(board[darkOrLightState])
        player3.playCards(board[darkOrLightState])
        player4.playCards(board[darkOrLightState])


        # checks for and removes piles of 10 from the game board
        board[darkOrLightState].checkForDutchPilesToRemove()

        pygame.display.update()

        if len(player1.blitzPile) == 0 or len(player2.blitzPile) == 0 or len(player3.blitzPile) == 0 or len(
                player4.blitzPile) == 0:
            runGame = False
            gameEnded = True

    return runGame, gameEnded


def end(screen, sound, board, player1, player2, player3, player4, controls):
    gameEnded = True
    clock = pygame.time.Clock()
    darkOrLightState = 0

    # Displays whether the user wins or loses based on which players blitz pile ran out first

    clock.tick(60)
    screen.fill((0, 0, 0))
    screen.blit(board[darkOrLightState].boardImage, (0, 0))
    screen.blit(FlipButtonImage, FLIP_BUTTON_COORDS)
    player1.displayPlayerCards(screen, P1_CARD_COORDS)
    player2.displayPlayerCards(screen, P2_CARD_COORDS)
    player3.displayPlayerCards(screen, P3_CARD_COORDS)
    player4.displayPlayerCards(screen, P4_CARD_COORDS)
    board[darkOrLightState].displayCardPiles(screen, PILE_CARD_COORDS)

    player1.displayScore(screen)
    player2.displayScore(screen)
    player3.displayScore(screen)
    player4.displayScore(screen)

    if player1.score - 2 * len(player1.blitzPile) >= player2.score - 2 * len(player2.blitzPile) \
            and player1.score - 2 * len(player1.blitzPile) >= player3.score - 2 * len(player3.blitzPile) \
            and player1.score - 2 * len(player1.blitzPile) >= player4.score - 2 * len(player4.blitzPile):

        screen.blit(winImage, END_MESSAGE_COORDS)
        player1.displayScore(screen)
        pygame.display.update()
        sound.win.play()

    else:
        screen.blit(loseImage, END_MESSAGE_COORDS)
        pygame.display.update()
        sound.lose.play()

    pygame.time.wait(5000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False

    return True


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BlitzOn!")
    runTitleScreen = True
    controls = Controls()
    clock = pygame.time.Clock()

    while runTitleScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        clock.tick(60)
        screen.blit(titleImage, (0, 0))
        screen.blit(playButtonImage, PLAY_BUTTON_COORDS)

        if controls.leftButtonClick():
            mousePos = controls.getMousePos()
            if controls.mouseInArea(mousePos, PLAY_BUTTON_COORDS, PLAY_BUTTON_SIZE):
                sound.buttonClick.play()
                screen.blit(playButtonClickedImage, PLAY_BUTTON_COORDS)
                pygame.display.update()
                pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
                runTitleScreen = False

        pygame.display.update()

    while True:
        board, player1, player2, player3, player4, controls = start()
        runGame, gameEnded = game(screen, sound, board, player1, player2, player3, player4, controls)

        if gameEnded:
            restart = end(screen, sound, board, player1, player2, player3, player4, controls)
            if not restart:
                break


main()
