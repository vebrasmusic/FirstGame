import pygame
from pygame.locals import *
import os
import random



class EntitySounds():
    def __init__(self, walk_sound_folder, attack_sound = None):
        self.walk_sounds = []
        self.load_walk_sounds(walk_sound_folder)
        self.attack_sound = pygame.mixer.Sound(attack_sound) if attack_sound else None

    def load_walk_sounds(self, walk_sound_folder):
        for sound in os.listdir(walk_sound_folder):
            if sound.endswith('.wav'):
                full_path = os.path.join(walk_sound_folder, sound)
                self.walk_sounds.append(pygame.mixer.Sound(full_path))

    def play_walk_sound(self):
        random_walk_sound = random.choice(self.walk_sounds)
        pygame.mixer.Sound.play(random_walk_sound)

    def play_attack_sound(self):
        pygame.mixer.Sound.play(self.attack_sound)



class PlayerSounds(EntitySounds):
    def __init__(self, walk_sound_folder):
        super(PlayerSounds, self).__init__(walk_sound_folder)

    def load_walk_sounds(self, walk_sound_folder):
        for sound in os.listdir(walk_sound_folder):
            if sound.endswith('.wav'):
                full_path = os.path.join(walk_sound_folder, sound)
                new_sound = pygame.mixer.Sound(full_path)
                new_sound.set_volume(0.2)
                self.walk_sounds.append(new_sound)

    
    #     self.grab_sound = pygame.mixer.Sound(grab_sound)

    # def play_grab_sound(self):
    #     pygame.mixer.Sound.play(self.grab_sound)
    #     pygame.mixer.music.stop()