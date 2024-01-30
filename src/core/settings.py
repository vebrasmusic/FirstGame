import pygame
from pygame.locals import *

class KeyBindings():
    def __init__(self):
        self.bindings = {}
        self.bindings["up"] = K_w
        self.bindings["down"] = K_s
        self.bindings["right"] = K_d
        self.bindings["left"] = K_a
        self.bindings["action"] = K_c
    
    def changeBindings(self, key, new_binding):
        if self.check_conflicting(new_binding):
            if key in self.bindings:
                self.bindings[key] = new_binding
                return True  # Successfully changed the binding
            # Optionally handle the case where 'key' is not in 'bindings'
        return False  # Conflict found or key not found

    def check_conflicting(self, new_binding):
        for binding in self.bindings.values():
            if binding == new_binding:
                return False  # Conflict found
        return True  # No conflict

    def getAllBindings(self):
        return self.bindings

    def get_key(self, action):
        return self.bindings.get(action, None)

class GameSettings():
    def __init__(self):
        self.key_bindings = KeyBindings()

        self.base_resolution = (640, 480)
        self.scale_factor = 2
        self.scaled_resolution = (self.base_resolution[0] * self.scale_factor,
                                  self.base_resolution[1] * self.scale_factor)


                                  # Aspect ratio check
        base_aspect_ratio = self.base_resolution[0] / self.base_resolution[1]
        scaled_aspect_ratio = self.scaled_resolution[0] / self.scaled_resolution[1]
        print("Base Aspect Ratio:", base_aspect_ratio, "Scaled Aspect Ratio:", scaled_aspect_ratio)

        

