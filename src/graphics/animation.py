import pygame
import os
import json

class Spritesheet:
    def __init__(self, filename):
        # Using convert_alpha() to maintain the transparency of spritesheet
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, x, y, width, height, scale=3):
        """
        (x, y) is the top left coordinate of the sprite on the sheet,
        width and height are the size of the sprite
        """
        # Create a new blank image with support for alpha transparency
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        if scale != 1:
            sprite = pygame.transform.scale(sprite, (int(width * scale), int(height * scale)))
        return sprite
        


class Animation:
    def __init__(self, frame_specs, filename, animation_speed):
        """
        frame_specs: List of tuples, each tuple containing (x, y, width, height) of a frame on the spritesheet
        filename: Path to the spritesheet file
        animation_speed: Time in milliseconds to show each frame
        """
        self.spritesheet = Spritesheet(filename)
        self.frames = self.load_frames(frame_specs)
        self.current_frame = 0
        self.last_updated = pygame.time.get_ticks()
        self.animation_speed = animation_speed

    def load_frames(self, frame_specs):
        images = []
        for spec in frame_specs:
            try:
                x, y, width, height = spec
                images.append(self.spritesheet.get_sprite(x, y, width, height))
            except Exception as e:
                # Handle the exception as appropriate for your use case
                print(f"Error loading sprite: {e}")
        return images

    def update(self, flip_x=False):
        now = pygame.time.get_ticks()
        if now - self.last_updated > self.animation_speed and len(self.frames) > 0:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        frame = self.frames[self.current_frame] if self.frames else self.spritesheet.get_sprite(0, 0, 32, 32)
        
        if flip_x:
            frame = pygame.transform.flip(frame, True, False)

        return frame