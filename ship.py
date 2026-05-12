import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        """Create the player area."""
        self.player_area = pygame.Rect(400, self.settings.screen_width - 400, self.settings.screen_height-800, 400)
        


        """Load the ship image and get its rect."""
        self.image = pygame.image.load('Assets/images/YellowHeart.png')
        self.rect = self.image.get_rect()

        """Start each new ship at the bottom center of the player area."""
        self.rect.midbottom = self.player_area.midbottom
        """Store a decimal value for the ship's horizontal position."""
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.player_area.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.player_area.left:
            self.x -= self.settings.ship_speed

        """"Vertical update."""
        if self.moving_up and self.rect.top > self.player_area.top:
            self.rect.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.player_area.bottom:
            self.rect.y += self.settings.ship_speed


        """Update rect object from self.x."""
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)