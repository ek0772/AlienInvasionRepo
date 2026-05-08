import pygame
from pygame import mixer


class Audio:
    def __init__(self):
        """Initialize audio settings."""
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound('Assets/sound/SpamtonTheme.mp3')
        self.shoot_sound = pygame.mixer.Sound('Assets/sound/HeartShot.wav')
        self.spamton_sound = pygame.mixer.Sound('Assets/sound/SpamtonHit.wav')
        self.laugh_sound = pygame.mixer.Sound('Assets/sound/SpamtonLaugh.wav')

        
