import pygame
import random

class PowerUp:
    def __init__(self, width=50, height=50, effect=None):
        self.x = random.randint(0, 800)
        self.y = random.randint(-100, 0)
        self.speed = 2
        
        # Jika efek diberikan, gunakan efek tersebut; jika tidak, pilih secara acak
        self.effect = effect if effect else random.choice(["health", "slow", "shield"])
        
        # Gambar untuk setiap jenis efek
        self.images = {
            "health": "assets/health.png",
            "slow": "assets/slow.png",
            "shield": "assets/shield.png",
        }
        
        self.image = pygame.image.load(self.images[self.effect])
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.y += self.speed
        if self.y > 600:
            self.y = random.randint(-100, 0)
            self.x = random.randint(0, 800)
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)