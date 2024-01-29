import pygame, sys, os
from pygame.locals import *
from src.characters.Ally import Player
from .controller import PlayerController
from .settings import GameSettings

class Level():
    def __init__(self, player_position, level_file):
        self.player_position = player_position
        self.level_file = level_file


    


    