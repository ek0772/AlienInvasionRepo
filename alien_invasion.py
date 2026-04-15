"""
file: alien_invasion.py
Author: Elijah K
Date: 4-14-2026
Purpose: A game where the player shoots aliens and controls a ship.
Starter code: Comes from lecture demonstration and Python Crash Course, 3rd edition.
"""



import pygame
import sys

from pygame import event
import settings
from pathlib import Path
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.settings = settings.settings()
        self.screen = pygame.display.set_mode((self.settings.screen_height, self.settings.screen_width))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Alien Invasion")
        self.ship= Ship(self)


        "Runs the game loop."
    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()   
            self.clock.tick(self.settings.frame_rate)
            """Make the most recently drawn screen visible."""
            pygame.display.flip()
            

    def _check_events(self):
        """Responds to keypresses and mouse events."""    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False



    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
