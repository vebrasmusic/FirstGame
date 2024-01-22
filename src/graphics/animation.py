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
    def __init__(self, filename, animation_speed):
        """
        frame_specs: List of tuples, each tuple containing (x, y, width, height) of a frame on the spritesheet
        filename: Path to the spritesheet file
        animation_speed: Time in milliseconds to show each frame
        """
        self.filename = filename + '.png'
        self.json_filepath = filename + '.json'
        self.spritesheet = Spritesheet(self.filename)
        self.frames = self.load_frames_from_json()
        self.current_frame = 0
        self.last_updated = pygame.time.get_ticks()
        self.animation_speed = animation_speed

    def load_frames_from_json(self):
        images = []
        try:
            with open(self.json_filepath, 'r') as file:
                data = json.load(file)
                frame_specs = data.get('frame_specs', [])

            for spec in frame_specs:
                if len(spec) == 4:  # Ensure spec has 4 elements: x, y, width, height
                    images.append(self.spritesheet.get_sprite(*spec))
                else:
                    print(f"Invalid frame specification: {spec}")

        except Exception as e:
            print(f"Error loading frames from JSON: {e}")

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