import pygame
from .Entity import Entity
from src.graphics.animation import Animation

class Player(Entity):
    def __init__(self, x, y, display_size):
        super(Player, self).__init__(x, y) #probably put default player image here
        self.screen_width, self.screen_height = display_size
        self.player_speed = 3
        self.idle_sprite_props = [
            (0, 0 , 32, 35), 
            (0, 35, 32, 35), 
            (0, 70, 32, 35),
            (0, 105, 32, 35),
            (0, 140, 32, 35),
            (0, 175, 32, 35)
        ]
        self.run_sprite_props = [
            (0,0,32,35),
            (0, 35, 32, 34),
            (0, 69, 32, 33 ),
            (0, 102, 32, 36),
            (0, 138, 34, 37),
            (0, 175, 34, 34),
            (0, 209, 34, 33),
            (0, 244, 34, 37)
        ]
        self.idle_animation = Animation(self.idle_sprite_props, "assets/player/idle.png", 100)
        self.run_animation = Animation(self.run_sprite_props, "assets/player/run.png", 100)
        self.animation_state = "idle"
        self.facing_right = True
        self.image = self.idle_animation.update()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask
        self.mask = pygame.mask.from_surface(self.image)

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

        min_x, min_y, mask_width, mask_height = self.calculate_mask_bounds()

        if direction == "left":
            self.rect.x = max(self.rect.x - self.player_speed, min_x)
            self.facing_right = False
            self.animation_state = "running"
        elif direction == "right":
            self.rect.x = min(self.rect.x + self.player_speed, self.screen_width - mask_width - min_x)
            self.facing_right = True
            self.animation_state = "running"
        # Add more directions (up, down) as needed
        elif direction == "down":
            self.rect.y = min(self.rect.y + self.player_speed, self.screen_height - mask_height - min_y)
            self.animation_state = "running"
        # Add more directions (up, down) as needed
        elif direction == "up":
            self.rect.y = max(self.rect.y - self.player_speed, 0 - min_y)
            self.animation_state = "running"
        elif direction == "idle":
            self.animation_state = "idle"

        self.mask = pygame.mask.from_surface(self.image)
        # Add more directions (up, down) as needed

    def update(self):
        # Select and update the current animation based on the player's state
        if self.animation_state == "idle":
            self.image = self.idle_animation.update(flip_x=not self.facing_right)
        elif self.animation_state == "running":
            self.image = self.run_animation.update(flip_x=not self.facing_right)
        self.mask = pygame.mask.from_surface(self.image)  # Update the mask


    



