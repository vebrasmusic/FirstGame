import pygame
from utils import images, audio

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name):
        super(Entity, self).__init__()
        self.image, self.rect = images.loadImage(image_name)
        self.rect.x = x
        self.rect.y = y
