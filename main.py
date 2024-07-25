import pygame
import os
from constants import *
from gameBoard import GameBoard
from player import Player
from ai import AI
from controls import Controls
from sounds import Sounds

pygame.init()
sound = Sounds()

# Load images
titleImage = pygame.image.load(os.path.join(TITLE_SCREEN))
winImage = pygame.image.load(os.path.join('images', END_SCREENS[0]))
loseImage = pygame.image.load(os.path.join('images', END_SCREENS[1]))
buttonImages = {
    'play': (pygame.image.load(os.path.join('images/buttons', PLAY_BUTTON)),
             pygame.image.load(os.path.join('images/buttons', PLAY_BUTTON_CLICKED))),
    'dark': (pygame.image.load(os.path.join('images/buttons', DARK_BUTTON)),
             pygame.image.load(os.path.join('images/buttons', DARK_BUTTON_CLICKED))),
    'light': (pygame.image.load(os.path.join('images/buttons', LIGHT_BUTTON)),
              pygame.image.load(os.path.join('images/buttons', LIGHT_BUTTON_CLICKED))),
    'ready': (pygame.image.load(os.path.join('images/buttons', READY_BUTTON)),
              pygame.image.load(os.path.join('images/buttons', READY_BUTTON_CLICKED)))
}


def main():
    darkOrLightState = 0
    boards = [GameBoard(GAME_BOARD_IMAGES[0], SCREEN_WIDTH, SCREEN_HEIGHT),
              GameBoard(GAME_BOARD_IMAGES[1], SCREEN_WIDTH, SCREEN_HEIGHT)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BlitzOn!")

    players = [Player(1), AI(2), AI(3), AI(4)]
    for player in players:
        player.shuffleDeck()
        player.createInitialHand(boards[darkOrLightState])

    player1, player2, player3, player4 = players
    controls = Controls()
    runTitleScreen, runGame = True, True
    clock = pygame.time.Clock()

    while runTitleScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        clock.tick(60)
        screen.blit(titleImage, (0, 0))
        screen.blit(buttonImages['play'][0], PLAY_BUTTON_COORDS)
        if darkOrLightState == 0:
            screen.blit(buttonImages['dark'][0], DARK_LIGHT_BUTTON_COORDS)
        else:
            screen.blit(buttonImages['light'][0], DARK_LIGHT_BUTTON_COORDS)

        if controls.leftButtonClick():
            mousePos = controls.getMousePos()
            if controls.mouseInArea(mousePos, PLAY_BUTTON_COORDS, PLAY_BUTTON_SIZE):
                sound.buttonClick.play()
                screen.blit(buttonImages['play'][1], PLAY_BUTTON_COORDS)
                pygame.display.update()
                pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
                runTitleScreen = False
            if controls.mouseInArea(mousePos, DARK_LIGHT_BUTTON_COORDS, DARK_LIGHT_BUTTON_SIZE):
                sound.buttonClick.play()
                state_key = 'dark' if darkOrLightState == 0 else 'light'
                screen.blit(buttonImages[state_key][1], DARK_LIGHT_BUTTON_COORDS)
                pygame.display.update()
                pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
                darkOrLightState = 1 - darkOrLightState

        pygame.display.update()

    while runGame:
        clock.tick(60)

        screen.fill((0, 0, 0))
        screen.blit(boards[darkOrLightState].boardImage, (0, 0))
        screen.blit(buttonImages['ready'][0], READY_BUTTON_COORDS)

        for player, coords in zip(players, [P1_CARD_COORDS, P2_CARD_COORDS, P3_CARD_COORDS, P4_CARD_COORDS]):
            player.displayPlayerCards(screen, coords)
            player.displayScore(screen)

        boards[darkOrLightState].displayCardPiles(screen, PILE_CARD_COORDS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if controls.leftButtonClick() and player1.selectedCardIndexOnGameBoard == -1:
            mousePos = controls.getMousePos()
            player1.selectedCardIndexOnGameBoard = controls.hoveringOverCard(mousePos, P1_CARD_COORDS)

            if player1.selectedCardIndexOnGameBoard in range(0, 5):
                selectedCard = player1.findSelectedCard(player1.selectedCardIndexOnGameBoard)
                if selectedCard:
                    player1.selectedCard = selectedCard
                    player1.cardSelected = True
            elif controls.mouseInArea(mousePos, READY_BUTTON_COORDS, READY_BUTTON_SIZE):
                sound.buttonClick.play()
                screen.blit(buttonImages['ready'][1], READY_BUTTON_COORDS)
                pygame.display.update()
                pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
                player1.flipWoodPile()
                for player in players[1:]:
                    player.flipWoodPile()

        if controls.leftButtonClick() and player1.cardSelected:
            mousePos = controls.getMousePos()
            placeDownPosIndex = controls.hoveringOverCard(mousePos, PILE_CARD_COORDS)
            stackingPosIndex = controls.hoveringOverCard(mousePos, P1_CARD_COORDS)

            if placeDownPosIndex in range(0, 12):
                if player1.playAttempt(boards[darkOrLightState], placeDownPosIndex, player1.selectedCard):
                    if player1.selectedCardIndexOnGameBoard in range(2, 5):
                        player1.playResultForPostPile(True, boards[darkOrLightState], placeDownPosIndex,
                                                      player1.selectedCardIndexOnGameBoard - 2)
                    elif player1.selectedCardIndexOnGameBoard == 0:
                        player1.playResultForWoodPile(True, boards[darkOrLightState], placeDownPosIndex)
                    elif player1.selectedCardIndexOnGameBoard == 1:
                        player1.playResultForBlitzPile(True, boards[darkOrLightState], placeDownPosIndex)
                    sound.cardPlace.play()
                    player1.selectedCardIndexOnGameBoard = -1
                    player1.cardSelected = False
                    pygame.time.wait(250)

            elif stackingPosIndex in range(2, 5):
                if player1.stackAttempt(player1.postPiles[stackingPosIndex - 2][0], player1.selectedCard):
                    if player1.selectedCardIndexOnGameBoard in range(2, 5):
                        player1.playResultForPostPile(True, boards[darkOrLightState], stackingPosIndex - 2,
                                                      player1.selectedCardIndexOnGameBoard - 2)
                    elif player1.selectedCardIndexOnGameBoard == 0:
                        player1.playResultForPostPile(True, boards[darkOrLightState], stackingPosIndex - 2,
                                                      player1.selectedCardIndexOnGameBoard - 2)
                    elif player1.selectedCardIndexOnGameBoard == 1:
                        player1.playResultForBlitzPile(True, boards[darkOrLightState], stackingPosIndex - 2)
                    sound.cardPlace.play()
                    player1.selectedCardIndexOnGameBoard = -1
                    player1.cardSelected = False
                    pygame.time.wait(250)

        if controls.rightButtonClick():
            player1.selectedCardIndexOnGameBoard = -1
            player1.cardSelected = False

        if player1.cardSelected:
            mousePos = controls.getMousePos()
            clickedCardPos = (mousePos[0] - 74 / 2, mousePos[1] - 108 / 2)
            screen.blit(player1.selectedCard.image, clickedCardPos)

        for player in players[1:]:
            player.playCards(boards[darkOrLightState])

        boards[darkOrLightState].checkForDutchPilesToRemove()
        pygame.display.update()

        if any(len(player.blitzPile) == 0 for player in players):
            runGame = False

    while not runGame:
        screen.fill((0, 0, 0))
        screen.blit(boards[darkOrLightState].boardImage, (0, 0))
        screen.blit(buttonImages['ready'][0], READY_BUTTON_COORDS)

        for player, coords in zip(players, [P1_CARD_COORDS, P2_CARD_COORDS, P3_CARD_COORDS, P4_CARD_COORDS]):
            player.displayPlayerCards(screen, coords)
            player.displayScore(screen)

        boards[darkOrLightState].displayCardPiles(screen, PILE_CARD_COORDS)

        player1_scores = player1.score - 2 * len(player1.blitzPile)
        ai_scores = [player.score - 2 * len(player.blitzPile) for player in players[1:]]
        if player1_scores >= max(ai_scores):
            screen.blit(winImage, END_MESSAGE_COORDS)
            sound.win.play()
        else:
            screen.blit(loseImage, END_MESSAGE_COORDS)
            sound.lose.play()

        pygame.display.update()
        pygame.time.wait(10000)
        pygame.quit()
        return


main()
