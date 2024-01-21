import pygame
from utils import images, audio
import Entity
from graphics.animation import Animation

class Player(Entity.Entity):
    def __init__(self, x, y):
        super(Player, self).__init__(x, y) #probably put default player image here
        self.idle_animation = Animation("assets/player_idle")
        self.walk_animation = Animation("assets/player_walk")
        self.run_animation = Animation("assets/player_run")
        self.animation_state = "idle"
        self.image = self.idle_animation.update()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, direction):
        if direction == "left":
            self.rect.x -= 5
            self.animation_state = "walking"
        elif direction == "right":
            self.rect.x += 5
            self.animation_state = "walking"
        # Add more directions (up, down) as needed
        elif direction == "up":
            self.rect.y += 5
            self.animation_state = "walking"
        # Add more directions (up, down) as needed
        elif direction == "down":
            self.rect.x -= 5
            self.animation_state = "walking"
        elif direction == "idle":
            self.animation_state = "walking"
        # Add more directions (up, down) as needed

    def update(self):
        # Select and update the current animation based on the player's state
        if self.animation_state == "idle":
            self.image = self.idle_animation.update()
        elif self.animation_state == "walking":
            self.image = self.walking_animation.update()
        elif self.animation_state == "running":
            self.image = self.running_animation.update()


    



