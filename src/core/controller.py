import pygame
from pygame.locals import *


class PlayerController():
    def __init__(self, player, key_bindings):
        self.player = player
        self.key_bindings = key_bindings

    def input(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:  # Check for key press
                for action in ["left", "right", "up", "down"]:
                    if event.key == self.key_bindings.getKey(action):
                        self.player.move(action)
            elif event.type == KEYUP:
                self.player.move("idle")
                # Handle other keys as needed