import pygame, sys, os
from pygame.locals import *
from .settings import GameSettings
from src.objects.levelObjects import *
from src.graphics.animation import *
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
        self.door_fragments = {}
        self.doors = []
        self.spawn_point = None
        self.tileset_image = pygame.image.load("assets/levels/tileset.png")
        self.load_objects()

        self.door_text_coords = (0,0)

        self.door_interact_text = AnimatedText(self.door_text_coords, "assets/text/door_interact.png","assets/text/door_interact.json", 300, 0.3, "door_interact")

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

        for frag in self.door_fragments:
            #frag is the key ie the destination
            new_door = Door(self.door_fragments[frag], frag)
            print(new_door)
            self.doors.append(new_door)

    def check_collisions(self, player_rect):
        for door in self.doors:
            collision, overlap = door.is_collision(player_rect)
            if collision:
                print(f"Player collided with door to {door.destination_level} at {overlap}")
                self.door_interact_text.set_coords((250, 0))
                self.door_interact_text.visible = True
            else:
                self.door_interact_text.visible = False
            
            
    def load_spawn_point(self, layer):
        if layer['objects']:
            # Assuming there's only one spawn point object
            spawn = layer['objects'][0]
            self.spawn_point = (spawn['x'], spawn['y'] - 40)

    def update(self):
        self.door_interact_text.update()

    def render(self, screen):
        self.door_interact_text.render(screen)
        



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

    def check_collisions(self, player_rect):
        self.objects.check_collisions(player_rect)

    
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
        self.objects.render(screen)

        # Then render the terrain and objects
        self.terrain.render(screen)


    def update(self, player_rect):
        self.check_collisions(player_rect)
        self.objects.door_interact_text.update()

    

