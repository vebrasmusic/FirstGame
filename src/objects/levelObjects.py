import pygame
from pygame.locals import *
from src.graphics.animation import *


class Door(pygame.sprite.Sprite):
    '''
        desitnation level should be string name of level
        
        '''
    def __init__(self, coords, destination_level):
        self.coords = coords
        self.destination_level = destination_level
        self.image = pygame.Surface((16, 16))  # Create a surface with the size of the door
        self.rect = self.image.get_rect(topleft=(coords[0]))  # Get the rectangle object that has the dimensions of the image

    def is_collision(self, player_rect):
        if self.rect.colliderect(player_rect):
            top = max(self.rect.top, player_rect.top)
            return True, top
        else:
            return False, None

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


    def __str__(self):
        return f"Coords: {self.coords}, Level: {self.destination_level}"


class AnimatedText(pygame.sprite.Sprite):
    def __init__(self,coords, graphics_filepath, json_filepath, speed, scale, id):
        self.id = id
        self.visible = False

        self.animation = Animation(graphics_filepath, json_filepath, speed, scale)

        self.image = self.animation.update()
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = coords

    def set_coords(self, coords):
        self.rect.x, self.rect.y = coords

    def render(self, screen):
        if self.visible:
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.image = self.animation.update()





    