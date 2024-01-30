import pygame, sys, os
from pygame.locals import *
from src.characters.Ally import Player
from .controller import PlayerController
from .settings import GameSettings
from .level import Level

class Game():
    def __init__(self):
        pygame.init()


        self.settings = GameSettings()
        self.window = pygame.display.set_mode(self.settings.scaled_resolution)
        self.isRunning = False
        pygame.display.set_caption("First Game")

        self.base_surface = pygame.Surface(self.settings.base_resolution)  # Surface for base resolution

        self.level1 = Level("level1")

        self.player_spawn = self.level1.player_spawn

        self.player = Player(self.player_spawn[0], self.player_spawn[1], self.settings.base_resolution)
        self.clock = pygame.time.Clock()
        self.group = pygame.sprite.Group(self.player)
        self.controller = PlayerController(self.player, self.settings.key_bindings)

        
        

    def run(self):
        self.isRunning = True
        self.loop()
    
    def loop(self):
        while self.isRunning:
            # Event handling loop
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.isRunning = False

            # Handle continuous key presses
            self.controller.handle_keys(events)
            self.group.update()  # Update all sprites
            self.render()  # Render the scene
            pygame.display.flip()  # Update the full display
            self.clock.tick(60)  # Maintain 60 FPS

    def render(self):
        # self.screen.fill((0, 0, 0))  # Fill the screen with black (or any bg color)
        # self.level1.terrain.render(self.screen)
        # self.group.draw(self.screen)  # Draw all sprites

        self.base_surface.fill((0, 0, 0))  # Fill the base surface
        
        self.level1.render(self.base_surface)  # Render terrain to base surface
        self.group.draw(self.base_surface)  # Draw sprites to base surface

        # Scale the base surface
        scaled_surface = pygame.transform.scale(self.base_surface, self.settings.scaled_resolution)

        # Draw the scaled surface onto the window
        self.window.blit(scaled_surface, (0, 0))



    





