'''
This module is responsible for loading and rendering the level,
including the terrain and objects.

Also, it is responsible for loading the level data from a file and
creating the level objects based on that data.
'''

import json
import pygame
from pygame.locals import *
from src.objects.levelObjects import Door
#from src.graphics.animation import *


class LevelTerrain:
    '''
    this class is responsible for loading and rendering the terrain in the level
    how: it takes the level data and renders the tile layers
    '''
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


class LevelObjects():
    '''
    this class is responsible for loading and rendering the objects in the level
    '''
    def __init__(self, level_data):
        self.level_data = level_data
        self.door_fragments = {}
        self.doors = []
        self.spawn_point = None
        self.tileset_image = pygame.image.load("assets/levels/tileset.png")
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
            x = obj['x']
            y = obj['y']
            destination_level = obj['name']
            if not destination_level in self.door_fragments:
                self.door_fragments[destination_level] = [(x, y)]
            else:
                self.door_fragments[destination_level].append((x, y))

        for frag, locations in self.door_fragments.items():
            #frag is the key ie the destination
            new_door = Door(locations, frag)
            self.doors.append(new_door)

    def load_spawn_point(self, layer):
        if layer['objects']:
            # Assuming there's only one spawn point objects4
            spawn = layer['objects'][0]
            self.spawn_point = (spawn['x'], spawn['y'] - 40)

    def update(self, player_rect):
        for interactable in self.doors: #eventually should be a list of Interactables, not just doors
            interactable.check_collision(player_rect)

    def render(self, screen):
        pass



class Level():
    ''' 
    holds the level data and objects, and loads the level from a file etc
    '''
    def __init__(self, level):
        self.level_file = "assets/levels/" + level + "/" + level + ".tmj"
        self.bg_image = pygame.image.load("assets/levels/backgrounds/" + level + ".png")

        with open(self.level_file, 'r', encoding='utf-8') as file:
            self.level_data = json.load(file)
        self.terrain = LevelTerrain(self.level_data)
        self.objects = LevelObjects(self.level_data)
        self.player_spawn = self.objects.spawn_point

        self.start_music()

    def start_music(self):
        ''' loads whatever the bg music should be for the level '''
        pygame.mixer.music.load("assets/audio/ambience/level1.wav")
        pygame.mixer.music.play(-1)

    def render_background(self, screen: pygame.Surface):
        ''' renders the background image for the level'''
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
        ''' renders the level to the screen'''
        # Render the static background first
        self.render_background(screen)
        self.objects.render(screen)

        # Then render the terrain and objects
        self.terrain.render(screen)


    def update(self, player_rect):
        ''' updates the level objects'''
        self.objects.update(player_rect)


class LevelHandler():
    ''' 
    this class is responsible for handling the levels in the game,
    including transitions between, etc.
    '''
    def __init__(self):
        self.current_level = None

    def load_level(self, level_name):
        ''' loads the level from a file'''
        self.current_level = Level(level_name)

    # def update(self, player_rect):
    #     ''' updates the current level'''
    #     self.current_level.update(player_rect)

    # def render(self, screen):
    #     ''' renders the current level'''
    #     self.current_level.render(screen)
