''' 
this module holds the main game class
'''
from dataclasses import dataclass
import pygame
from pygame.locals import *
from src.characters.Ally import Player
from .controller import PlayerController
from .menu import MainMenu
from .settings import GameSettings
from .level import Level, LevelHandler

@dataclass
class EventHandler():
    '''
    class for handling events in the game loop
    '''
    controller: PlayerController
    is_running: bool = False

    def handle_events(self):
        '''
        handle events in the game loop
        '''
        # Event handling loop
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False

        # Handle continuous key presses
        self.controller.handle_keys(events)


class GameAttributes():
    '''
    class for holding game attributes
    '''
    def __init__(self):
        self.settings = GameSettings()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(self.settings.scaled_resolution)
        pygame.display.set_caption("Dingy")

    def get_settings(self):
        '''
        returns the game settings
        '''
        return self.settings

    def get_clock(self):
        '''
        returns the game clock
        '''
        return self.clock


class Game():
    '''
    the main game core class, which contains
    the game loop and the main game objects,
    such as the player and the level
    '''
    def __init__(self):
        pygame.init()

        self.attributes = GameAttributes()

        self.base_surface = pygame.Surface(self.attributes.settings.base_resolution)  # Surface for base resolution

        #self.menu = MainMenu()

        self.level_handler = LevelHandler()

        # TODO: this is where we need to implement the level loading, ie like the LevelHandler() etc
        self.level1 = Level("level1")
        self.player_spawn = self.level1.player_spawn

        # TODO: get this player related / entity related stuff into its own class
        self.player = Player(self.player_spawn[0], self.player_spawn[1], self.attributes.settings.base_resolution)
        self.group = pygame.sprite.Group(self.player)

        self.controller = PlayerController(self.player, self.attributes.settings.key_bindings)
        self.event_handler = EventHandler(PlayerController(self.player, self.attributes.settings.key_bindings))

    def run(self):
        ''' 
        sets the game running in its loop
        this is what we call in main.py
        '''
        self.event_handler.is_running = True
        self.loop()

    def loop(self):
        '''
        the main game loop, which basiclaly serves as the first "update" function
        '''
        while self.event_handler.is_running:
            self.event_handler.handle_events() # Handle events in loop, ie controls, etc. from user

            self.update_all()  # Update all children

            self.render_all()  # Render the whole game

    def update_all(self):
        ''' updates all children '''
        # TODO: This is where we need to implement the update function for the game objects
        self.level1.update(self.player.rect) # this updates level stuff, need to implement better

        self.group.update()  # Update all sprites

    def render_all(self):
        ''' 
        renders all of the game objects to the screen, 
        calls cascading render functions of all children
        '''

        self.base_surface.fill((0, 0, 0))  # Fill the base surface

        # if self.menu.menu.is_enabled():
        #     print("menu")
        #     self.menu.render(self.base_surface)
        # else:
        self.level1.render(self.base_surface)  # Render terrain to base surface
        self.group.draw(self.base_surface)  # Draw sprites to base surface

        # Scale the base surface
        scaled_surface = pygame.transform.scale(self.base_surface, self.attributes.settings.scaled_resolution)

        # Draw the scaled surface onto the window
        self.attributes.window.blit(scaled_surface, (0, 0))

        pygame.display.flip()  # Update the full display
        self.attributes.clock.tick(60)  # Maintain 60 FPS
