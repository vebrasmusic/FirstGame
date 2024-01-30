import pygame
from pygame.locals import *


class Camera():
    def __init__(self, level_width, level_height, viewport_width, viewport_height):
        self.level_rect = pygame.Rect(0, 0, level_width, level_height)
        self.viewport = pygame.Rect(0, 0, viewport_width, viewport_height)
        self.zoom_level = 1.0

    def update(self, target):
        # Center the camera on the target (e.g., the player)
        self.viewport.center = target.rect.center

        # Adjust for zoom
        self.viewport.width = int(self.viewport.width / self.zoom_level)
        self.viewport.height = int(self.viewport.height / self.zoom_level)

        # Prevent the camera from going out of bounds
        self.viewport.clamp_ip(self.level_rect)

    def apply(self, entity):
        # Apply the camera's offset to an entity's position
        return entity.rect.move(-self.viewport.topleft)

    def change_zoom(self, zoom_change):
        # Change the zoom level
        self.zoom_level = max(0.5, min(2.0, self.zoom_level + zoom_change))

    def convert_to_screen_coordinates(self, world_coordinates):
        # Convert world coordinates to screen coordinates
        screen_x = world_coordinates[0] - self.viewport.x
        screen_y = world_coordinates[1] - self.viewport.y
        return screen_x, screen_y

    # Additional methods as needed...