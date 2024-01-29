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
    def __init__(self, graphic_filepath, json_filepath,  animation_speed):
        """
        frame_specs: List of tuples, each tuple containing (x, y, width, height) of a frame on the spritesheet
        filename: Path to the spritesheet file
        animation_speed: Time in milliseconds to show each frame
        """
        self.filename = graphic_filepath
        self.json_filepath = json_filepath
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


class ShootingAnimation(Animation):
    def __init__(self, graphic_filepath, json_filepath, animation_speed):
        super().__init__(graphic_filepath, json_filepath, animation_speed)
        self.playing = False

    def start(self):
        # Always restart the animation when this method is called
        self.playing = True
        self.current_frame = 0
    
    def is_finished(self):
        return self.current_frame == len(self.frames) - 1

    def update(self, flip_x=False):
        if not self.playing:
            return self.frames[0]  # Return the first frame when not playing

        now = pygame.time.get_ticks()
        if now - self.last_updated > self.animation_speed:
            self.last_updated = now
            if self.current_frame < len(self.frames) - 1:
                self.current_frame += 1
            else:
                self.playing = False  # Reset playing state when animation finishes

        frame = self.frames[self.current_frame]
        if flip_x:
            frame = pygame.transform.flip(frame, True, False)

        return frame

