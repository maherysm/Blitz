from constants import *
import pygame
import os
from controls import Controls

class SetupScreen(Controls):
    def __init__(self):
        self.titleImage = pygame.image.load(os.path.join(TITLE_SCREEN))
        self.buttonImages = {
            "play": (pygame.image.load(os.path.join(PLAY_BUTTON_A)),
                     pygame.image.load(os.path.join(PLAY_BUTTON_HOVER_A)),
                     pygame.image.load(os.path.join(PLAY_BUTTON_CLICKED_A))),
            "tutorial": (pygame.image.load(os.path.join(TUTORIAL_BUTTON)),
                         pygame.image.load(os.path.join(TUTORIAL_BUTTON_HOVER)),
                         pygame.image.load(os.path.join(TUTORIAL_BUTTON_CLICKED))),
            "options": (pygame.image.load(os.path.join(OPTIONS_BUTTON)),
                        pygame.image.load(os.path.join(OPTIONS_BUTTON_HOVER)),
                        pygame.image.load(os.path.join(OPTIONS_BUTTON_CLICKED))),
            "credits": (pygame.image.load(os.path.join(CREDITS_BUTTON)),
                        pygame.image.load(os.path.join(CREDITS_BUTTON_HOVER)),
                        pygame.image.load(os.path.join(CREDITS_BUTTON_CLICKED))),
            "exit": (pygame.image.load(os.path.join(EXIT_BUTTON)),
                     pygame.image.load(os.path.join(EXIT_BUTTON_HOVER)),
                     pygame.image.load(os.path.join(EXIT_BUTTON_CLICKED)))
        }
        self.buttons = list(self.buttonImages.keys())

    def displayTitleScreen(self, screen, buttonHovered=-1, buttonClicked=-1):
        screen.blit(self.titleImage, (0, 0))
        for i, button in enumerate(self.buttons):
            if i == buttonHovered:
                image = self.buttonImages[button][1]
            elif i == buttonClicked:
                image = self.buttonImages[button][2]
            else:
                image = self.buttonImages[button][0]
            screen.blit(image, SETUP_SCREEN_COORDS[i])
        pygame.display.update()

    def hoveringOrClickingButtons(self, screen, mousePos, buttonClicked):
        hoveringDisplayed = False
        for i in range(len(self.buttons)):
            if self.mouseInArea(mousePos, SETUP_SCREEN_COORDS[i], SETUP_SCREEN_BUTTON_SIZES[i]):
                if not buttonClicked:
                    self.displayTitleScreen(screen, i, -1)
                    hoveringDisplayed = True
                else:
                    self.displayTitleScreen(screen, -1, i)
                    pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
                    return i
        if not hoveringDisplayed:
            self.displayTitleScreen(screen, -1, -1)
        return -1
