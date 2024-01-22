import pygame, sys, os
from pygame.locals import *
from src.characters.Ally import Player
from .controller import PlayerController
from .settings import GameSettings

class Game():
    def __init__(self):
        pygame.init()
        self.settings = GameSettings()
        self.window = pygame.display.set_mode(self.settings.display_size)
        self.isRunning = False
        self.player = Player(0,0, self.settings.display_size)
        self.clock = pygame.time.Clock()
        self.group = pygame.sprite.Group(self.player)
        self.controller = PlayerController(self.player, self.settings.key_bindings)
        pygame.display.set_caption("First Game")
        self.screen = pygame.display.get_surface()

    def run(self):
        self.isRunning = True
        self.loop()
    
    def loop(self):
        while self.isRunning:
            # Event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
            
            # Handle continuous key presses
            self.controller.handle_keys()
            self.group.update()  # Update all sprites
            self.render()  # Render the scene
            pygame.display.flip()  # Update the full display
            self.clock.tick(60)  # Maintain 60 FPS

    def render(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black (or any bg color)
        self.group.draw(self.screen)  # Draw all sprites


    





