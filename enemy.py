import pygame
import random

class Enemy:
    def __init__(self, enemy_type, width=62, height=62):
        self.x = random.randint(0, 800 - width)
        self.y = random.randint(-150, -50)
        self.speed = random.randint(2, 5)
        self.direction = random.choice([-1, 1])  # Gerakan horizontal (kiri/kanan)
        self.type = enemy_type

        self.width = width
        self.height = height

        self.images = {
            "bomb": "assets/bomb.png",
            "fire": "assets/fire.png",
            "rock": "assets/rock.png",
        }

        self.damage = {"bomb": -1, "fire": -1, "rock": -1}

        self.image = pygame.image.load(self.images.get(self.type, "assets/rock.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        """Update posisi musuh dengan gerakan acak."""
        self.y += self.speed
        self.x += self.direction * random.randint(1, 3)  # Gerakan horizontal acak

        # Reset posisi jika keluar layar
        if self.y > 600 or self.x < 0 or self.x > 800:
            self.y = random.randint(-150, -50)
            self.x = random.randint(0, 800 - self.width)
            self.speed = random.randint(2, 5)
            self.direction = random.choice([-1, 1])  # Arah horizontal baru

        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        """Gambar musuh ke layar."""
        screen.blit(self.image, self.rect)

def spawn_enemies(enemies, enemy_types, max_enemies, level):
    """Fungsi untuk spawn musuh baru secara acak."""
    if len(enemies) < max_enemies:
        new_enemy = Enemy(random.choice(enemy_types))
        enemies.append(new_enemy)

    # Tambahkan lebih banyak musuh dengan meningkatnya level
    if level > 1 and random.random() < 0.1 * level:  # Semakin tinggi level, semakin sering spawn
        new_enemy = Enemy(random.choice(enemy_types))
        enemies.append(new_enemy)

def update_level(level, spawn_rate, timer):
    """Tingkatkan level berdasarkan waktu."""
    current_time = pygame.time.get_ticks()
    if current_time - timer > 10000:  # Naik level setiap 10 detik
        level += 1
        spawn_rate = max(500, spawn_rate - 50)  # Spawn rate makin cepat
        timer = current_time
    return level, spawn_rate, timer
