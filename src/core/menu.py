import pygame_menu
import pygame
from pygame.locals import *

class MainMenu():
    ''' Holds and renders the main menu '''

    def __init__(self):
        self.menu = pygame_menu.Menu('Dust', 400, 300, theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.button('Play', self.start_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def render(self, screen):
        ''' renders the main menu to the screen '''
        self.menu.draw(screen)

    def start_game(self):
        ''' starts the game '''
        self.menu.disable()
        self.menu.close()