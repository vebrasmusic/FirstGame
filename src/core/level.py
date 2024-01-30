import pygame, sys, os
from pygame.locals import *
from .settings import GameSettings
import json

class LevelTerrain:
    def __init__(self, level_data):
        self.level_data = level_data
        self.tileset_image = pygame.image.load("assets/levels/tileset.png")

    def render(self, screen):
        for layer in self.level_data['layers']:
            if layer['type'] == 'tilelayer' and layer['visible']:
                self.render_tile_layer(screen, layer)

    def render_tile_layer(self, screen, layer):
        # Assuming each tile is 16x16 pixels
        tile_width = 16
        tile_height = 16

        for y in range(layer['height']):
            for x in range(layer['width']):
                tile_id = layer['data'][x + y * layer['width']]
                if tile_id > 0:
                    # Tiles in Tiled are 1-indexed, so subtract 1 to get the correct tile
                    tile_id -= 1
                    tile_x = (tile_id % 20) * tile_width  # Assuming 20 tiles per row in the tileset
                    tile_y = (tile_id // 20) * tile_height
                    tile_rect = pygame.Rect(tile_x, tile_y, tile_width, tile_height)
                    screen.blit(self.tileset_image, (x * tile_width, y * tile_height), tile_rect)


class LevelObjects:
    def __init__(self, level_data):
        self.level_data = level_data
        self.doors = []
        self.spawn_point = None
        self.load_objects()

    def load_objects(self):
        for layer in self.level_data['layers']:
            if layer['type'] == 'objectgroup':
                if layer['name'] == 'Doors':
                    self.load_doors(layer)
                elif layer['name'] == 'SPAWN':
                    self.load_spawn_point(layer)

    def load_doors(self, layer):
        for obj in layer['objects']:
            # Create door objects and add them to self.doors
            # You will need to define what a 'door' is in your game
            pass

    def load_spawn_point(self, layer):
        if layer['objects']:
            # Assuming there's only one spawn point object
            spawn = layer['objects'][0]
            self.spawn_point = (spawn['x'], spawn['y'] - 30)

    def render(self, screen):
        # Render interactive objects like doors
        pass


class Level():
    def __init__(self, level):
        self.level_file = "assets/levels/" + level + "/" + level + ".tmj"
        self.bg_image = pygame.image.load("assets/levels/backgrounds/" + level + ".png")

        with open(self.level_file, 'r') as file:
            self.level_data = json.load(file)
        self.terrain = LevelTerrain(self.level_data)
        self.objects = LevelObjects(self.level_data)
        self.player_spawn = self.objects.spawn_point

        self.start_music()

        
    def start_music(self):
        pygame.mixer.music.load("assets/audio/ambience/level1.wav")
        pygame.mixer.music.play(-1)

    
    def render_background(self, screen):
        if self.bg_image:
            # Calculate the y-coordinate to start from the bottom-left corner
            bg_y = self.bg_image.get_height() - 500  # 512 - 480

            # Define the area of the background image to be displayed
            bg_rect = pygame.Rect(1000, bg_y, 640, 480)

            # Blit the specific area of the background to the screen
            screen.blit(self.bg_image, (0, 0), bg_rect)
        else:
            print("Background image not loaded")

    def render(self, screen):
        # Render the static background first
        self.render_background(screen)

        # Then render the terrain and objects
        self.terrain.render(screen)
        # self.objects.render(screen)  # Uncomment if objects have a render method

    

