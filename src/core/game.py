import pygame, sys, os
from pygame.locals import *
from characters.Ally import Player
from controller import PlayerController
from settings import GameSettings

class Game():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1920, 1080),display=SCALED)
        self.isRunning = False
        self.player = Player(0,0)
        self.settings = GameSettings()
        self.controller = PlayerController(self.player, self.settings.key_bindings)
        pygame.display.set_caption("First Game")
        self.screen = pygame.display.get_surface()

    def run(self):
        self.isRunning = True
        self.loop()
    
    def loop(self):
        while isRunning:
            self.controller.input(pygame.event.get()) # main event handler loop
            # update sprite group
            # pygame.display.update()
            #self.render()
            pygame.display.flip()

    def render(self):
        pass
        # self.screen.blit()


    





