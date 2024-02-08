''' 
Holds the level objects, such as doors and items
and their behaviors etc.
'''
from abc import ABC, abstractmethod
from dataclasses import dataclass
import pygame
from pygame.locals import *
from src.graphics.animation import Animation

class InteractableAction():
    '''
    class for the actions that objects can take, 
    such as a door moving you to a new level,
    or an item being placed in inventory.
    '''

    @abstractmethod
    def do_action(self):
        '''
        do the action
        '''
    @abstractmethod
    def print_action(self):
        '''
        print the action
        '''
        # print(f"Action: {self.action}")


class Interactable(pygame.sprite.Sprite, ABC):
    '''
    abstract class for objects that can be interacted with in a Level
    Each interactable shoukld have an InteractableAction object
    '''

    @abstractmethod
    def update(self):
        '''
        update the object in the game loop
        '''

    # @abstractmethod
    # def render(self,screen):
    #     '''
    #     render the object to the screen
    #     '''

    @abstractmethod
    def check_collision(self, player_rect):
        '''
        check if the player is colliding with the object
        '''


class Door(Interactable):
    '''
        destination level should be the name of the level, ie so can be called.
        
        '''
    def __init__(self, coords: tuple, destination_level: str):
        super().__init__()
        self.coords = coords
        self.text = AnimatedText((0,0), "assets/text/door_interact.png","assets/text/door_interact.json", 300, 0.3, "door_interact")
        self.is_colliding = False
        self.destination_level = destination_level
        self.image = pygame.Surface((16, 16))  # Create a surface with the size of the door
        self.rect = self.image.get_rect(topleft = coords[0])  # Get the rectangle object that has the dimensions of the image

    def check_collision(self, player_rect: Rect):
        '''
        checks for collisions between player and object
        '''
        if self.rect.colliderect(player_rect):
            top = max(self.rect.top, player_rect.top)
            print(f"Player collided with door to {self.destination_level} at {top}")
            self.is_colliding = True
            self.text.set_coords((250, 0))
            #self.door_interact_text.visible = True
            return top
        #self.door_interact_text.visible = False
        self.is_colliding = False
        return None

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def update(self, player_rect: Rect):
        self.check_collision(player_rect)
        self.objects.door_interact_text.update()

    def __str__(self):
        return f"Coords: {self.coords}, Level: {self.destination_level}"


class AnimatedText(pygame.sprite.Sprite):
    ''' the animated text that can be displayed for different game events'''
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
