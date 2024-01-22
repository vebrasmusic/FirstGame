import pygame
from src.utils import images, audio

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Entity, self).__init__()
