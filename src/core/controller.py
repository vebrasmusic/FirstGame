import pygame
from pygame.locals import *


class PlayerController():
    def __init__(self, player, key_bindings):
        self.player = player
        self.bindings = key_bindings

    # def handle_keys(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[self.bindings.get_key("left")]:
    #         self.player.move("left")
    #     if keys[self.bindings.get_key("right")]:
    #         self.player.move("right")
    #     if keys[self.bindings.get_key("up")]:
    #         self.player.move("up")
    #     if keys[self.bindings.get_key("down")]:
    #         self.player.move("down")
    #     # if keys[self.bindings.get_key("action")]:
    #     #     self.player.action()
    #     if not any([keys[self.bindings.get_key("left")], keys[self.bindings.get_key("right")],
    #                 keys[self.bindings.get_key("up")], keys[self.bindings.get_key("down")]]):
    #         self.player.move("idle")
    def handle_keys(self, events):
        keys = pygame.key.get_pressed()
        if keys[self.bindings.get_key("left")]:
            self.player.move("left")
        elif keys[self.bindings.get_key("right")]:
            self.player.move("right")
        elif keys[self.bindings.get_key("up")]:
            self.player.move("up")
        elif keys[self.bindings.get_key("down")]:
            self.player.move("down")
        else:
            self.player.move("idle")

        # for event in events:
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == self.bindings.get_key("action"):
        #             self.player.action()
        