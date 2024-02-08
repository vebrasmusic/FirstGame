''' This file contains the Entity class, which is the base class for all characters in the game. '''
import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
