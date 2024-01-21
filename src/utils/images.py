import pygame
import os

def loadImage(image_name):
    '''
    image_name:string
    takes an image and returns the Surface of it for pygame
    '''
    path = os.path.join("assets","sprites",image_name)
    try:
        surf = pygame.image.load(path)
    except Exception as exception:
        print("Cannot Load image")
        raise SystemExit(exception)
    return surf, surf.get_rect()

    



