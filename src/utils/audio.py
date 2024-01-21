import pygame
import os

def loadSound(sound_name):
    '''
    sound_name:string
    takes an audio anbd returns the Sound object
    '''
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except (pygame.error, message):
        print("Cannot load sound:", fullname)
        raise SystemExit(message)
    return sound

