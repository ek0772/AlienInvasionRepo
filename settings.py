"""settings.py"""
import pygame

class settings:
    def __init__(self):
        """Screen settings."""
        self.screen_width = 800
        self.screen_height = 1200
        self.frame_rate = 60
        self.background = pygame.image.load('Assets/images/SpamtonBackground.png')

        """Ship settings."""
        self.ship_speed = 8
        self.ship_limit = 2

        """Bullet settings."""
        self.bullet_speed = 10.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 20

        """Alien settings."""
        self.fleet_drop_speed = 5

        # "How quickly the game speeds up."
        self.speedup_scale = 1.5

        # "How quickly the alien point values increase."
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self): 
        """Initialize settings that change throughout the game."""
        self.ship_speed = 5.5
        self.bullet_speed = 5.5
        self.alien_speed = 1.5

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def font_settings(self):
        """Font settings for scoring information."""
        self.text_color = (255, 255, 0)
        self.font = pygame.font.Font('Assets/Fonts/VT323/VT323-Regular.ttf', 48)


    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)