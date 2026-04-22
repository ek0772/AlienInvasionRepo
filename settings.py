"""settings.py"""
import pygame

class settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 1200
        self.frame_rate = 60
        self.background = pygame.image.load('AlienInvasionRepo/Assets/images/background.png')

        """Ship settings."""
        self.ship_speed = 6
        self.ship_limit = 3

        """Bullet settings."""
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        """Alien settings."""
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1