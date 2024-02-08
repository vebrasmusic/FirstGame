"""
handles the player character and other characters
"""

import pygame
from src.graphics.animation import Animation
from src.audio.sounds import PlayerSounds
from .Entity import Entity

class Player(Entity):
    def __init__(self, x, y, display_size):
        super().__init__(x, y) #probably put default player image here
        self.screen_width, self.screen_height = display_size
        self.player_scale = 0.8
        self.player_speed = 3 * (1 - self.player_scale)
        self.idle_animation = Animation("assets/player/idle.png", "assets/player/idle.json", 100, self.player_scale)
        self.run_animation =  Animation("assets/player/walk.png", "assets/player/walk.json", 50,  self.player_scale)


        self.animation_state = "idle"
        self.facing_right = True

        self.image = self.idle_animation.update()
        self.rect = self.image.get_rect()

        hitbox_shrink_factor = 0.3  # Adjust this value to your needs
        self.rect.inflate_ip(-self.rect.width * (1 - hitbox_shrink_factor), -self.rect.height * (1 - hitbox_shrink_factor))
        self.rect.x = x
        self.rect.y = y

        self.mask = pygame.mask.from_surface(self.image)  # Create a mask
        self.level_type = "outside"

        self.sounds = PlayerSounds("assets/audio/player/walk")
        self.sound_cooldown = 0  # Add a cooldown counter for the sound
        self.cooldown_factor = 10


    def set_level_type(self, level_type: str):
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
                if self.sound_cooldown <= 0:
                    self.sounds.play_walk_sound()
                    self.sound_cooldown = self.cooldown_factor
            elif direction == "right":
                self.rect.x = min(self.rect.x + self.player_speed, self.screen_width - self.rect.width+110)
                self.facing_right = True
                self.animation_state = "running"
                if self.sound_cooldown <= 0:
                    self.sounds.play_walk_sound()
                    self.sound_cooldown = self.cooldown_factor
            elif direction == "down":
                self.rect.y = min(self.rect.y + self.player_speed, self.screen_height - self.rect.height+80)
                self.animation_state = "running"
                if self.sound_cooldown <= 0:
                    self.sounds.play_walk_sound()
                    self.sound_cooldown = self.cooldown_factor
            elif direction == "up":
                self.rect.y = max(self.rect.y - self.player_speed,  -80)
                self.animation_state = "running"
                if self.sound_cooldown <= 0:
                    self.sounds.play_walk_sound()
                    self.sound_cooldown = self.cooldown_factor
            elif direction == "idle":
                self.animation_state = "idle"
        else:
            if direction == "left":
                self.rect.x = max(self.rect.x - self.player_speed, -110)
                self.facing_right = False
                self.animation_state = "running"
                if self.sound_cooldown <= 0:
                    self.sounds.play_walk_sound()
                    self.sound_cooldown = self.cooldown_factor
            elif direction == "right":
                self.rect.x = min(self.rect.x + self.player_speed, self.screen_width - self.rect.width+110)
                self.facing_right = True
                self.animation_state = "running"
                if self.sound_cooldown <= 0:
                    self.sounds.play_walk_sound()
                    self.sound_cooldown = self.cooldown_factor
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

        if self.sound_cooldown > 0:
            self.sound_cooldown -= 1
