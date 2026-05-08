"""
file: alien_invasion.py
Author: Elijah K
Date: 4-14-2026
Purpose: A game where the player shoots aliens and controls a ship.
Starter code: Comes from lecture demonstration and Python Crash Course, 3rd edition.
"""



import pygame
import sys
from time import sleep
import random

"""Experimental gif import"""
"""NEEEDS "pip install gif-pygame" TO WORK """
import gif_pygame


from random import randint
from pygame import event
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from audio import Audio
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
        """Call audio class to load sound effects."""
        self.audio = Audio()
        
        """Load Background Music"""
        pygame.mixer.music.load('Assets/sound/SpamtonTheme.mp3')
        

        #Start Alien Invasion in an inactive state,
        self.game_active = False
        
        self.settings = settings.settings()

        self.screen = pygame.display.set_mode((self.settings.screen_height, self.settings.screen_width))
        
        self.play_button = Button(self, "Play")

        
       
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics, and create a scoreboard.


        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

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
            
            if self.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Play background music.
            pygame.mixer.music.play(-1)


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
            self.audio.shoot_sound.play()


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

        if collisions:
            for aliens in collisions.values():
                self.audio.spamton_sound.play()
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens:
            """Destroy existing bullets and create new fleet."""
            self.bullets.empty()
            """Win message implemented HERE"""

            """Start again with a new fleet."""
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 3
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.audio.laugh_sound.play()
            self.sb.prep_ships()

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()
            self.game_active = False

    def _update_aliens(self):
        """Update the position of aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        self._check_aliens_bottom()


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.settings.background, (0,0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        #draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
