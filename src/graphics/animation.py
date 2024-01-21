import pygame
import os

class Animation():

    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.frames = self.load_frames(image_folder)
        self.current_frame = 0
        self.last_updated = pygame.time.get_ticks()
        self.animation_speed = 100 #ms

    def load_frames(self, folder):
        images = []
        for file_name in sorted(os.listdir(folder)):
            if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                image_path = os.path.join(folder, file_name)
                images.append(pygame.image.load(image_path))
        return images
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > self.animation_speed:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
        return self.frames[self.current_frame] if self.frames else None
    

