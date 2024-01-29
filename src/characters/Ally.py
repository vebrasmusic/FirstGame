import pygame
from .Entity import Entity
from src.graphics.animation import *

class Player(Entity):
    
    def __init__(self, x, y, display_size):
        super(Player, self).__init__(x, y) #probably put default player image here
        self.screen_width, self.screen_height = display_size
        self.player_speed = 3
        self.idle_animation = Animation("assets/player/idle.png", "assets/player/idle.json", 100)
        self.run_animation =  Animation("assets/player/walk.png", "assets/player/walk.json", 100)

        self.animation_state = "idle"
        self.facing_right = True

        self.image = self.idle_animation.update()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mask = pygame.mask.from_surface(self.image)  # Create a mask
        self.level_type = "outside"


    def set_level_type(self, level_type):
        '''
        string, this will determine whether to do side scrolling or allow up and down as well.
        
        '''
        self.level_type = level_type

    def calculate_mask_bounds(self):
        mask_outline = self.mask.outline()
        if not mask_outline:
            return 0, 0, self.rect.width, self.rect.height

        min_x = min(mask_outline, key=lambda p: p[0])[0]
        max_x = max(mask_outline, key=lambda p: p[0])[0]
        min_y = min(mask_outline, key=lambda p: p[1])[1]
        max_y = max(mask_outline, key=lambda p: p[1])[1]

        return min_x, min_y, max_x - min_x, max_y - min_y

    def move(self, direction):

        if self.level_type == "inside":
            if direction == "left":
                self.rect.x = max(self.rect.x - self.player_speed, -110)
                self.facing_right = False
                self.animation_state = "running"
            elif direction == "right":
                self.rect.x = min(self.rect.x + self.player_speed, self.screen_width - self.rect.width+110)
                self.facing_right = True
                self.animation_state = "running"
            elif direction == "down":
                self.rect.y = min(self.rect.y + self.player_speed, self.screen_height - self.rect.height+80)
                self.animation_state = "running"
            elif direction == "up":
                self.rect.y = max(self.rect.y - self.player_speed,  -80)
                self.animation_state = "running"
            elif direction == "idle":
                self.animation_state = "idle"
        else:
            if direction == "left":
                self.rect.x = max(self.rect.x - self.player_speed, -110)
                self.facing_right = False
                self.animation_state = "running"
            elif direction == "right":
                self.rect.x = min(self.rect.x + self.player_speed, self.screen_width - self.rect.width+110)
                self.facing_right = True
                self.animation_state = "running"
            elif direction == "idle":
                self.animation_state = "idle"

        # Update the mask after moving
        self.mask = pygame.mask.from_surface(self.image)
        

    def update(self):
        # Handle other animations (idle, running) here
        if self.animation_state == "idle":
            self.image = self.idle_animation.update(flip_x=not self.facing_right)
        elif self.animation_state == "running":
            self.image = self.run_animation.update(flip_x=not self.facing_right)

        # Update the mask based on the current frame
        self.mask = pygame.mask.from_surface(self.image)



    



