"""
file: alien_invasion.py
Author: Elijah K
Date: 4-14-2026
Purpose: A game where the player shoots aliens and controls a ship.
Starter code: Comes from lecture demonstration and Python Crash Course, 3rd edition.
"""



import pygame
import sys
import random

from random import randint
from pygame import event
import settings
from pathlib import Path
from ship import Ship
from bullet import Bullet
from alien import Alien

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
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()


        """Movement flag; start with a ship that's not moving."""
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right==True:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1
        if self.moving_up:
            self.rect.y -= 1
        if self.moving_down:
            self.rect.y += 1



    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()   
            self.clock.tick(self.settings.frame_rate)
            """Make the most recently drawn screen visible."""

    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien= Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (400):
            while current_x < (self.settings.screen_width + 280):
                random_x = randint(0, self.settings.screen_width+280)
                self._create_alien(random_x, current_y)
                current_x += 2 * alien_width
                
            


            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self,x_position,y_position):
        """Create an aliens and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


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
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        

        """Get rid of bullets that have disappeared."""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)





        if not self.aliens:
            """Destroy existing bullets and create new fleet."""
            self.bullets.empty()
            """Win message implemented HERE"""

            """Start again with a new fleet."""
            self._create_fleet()

    def _update_aliens(self):
        """Update the position of aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.settings.background, (0,0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
