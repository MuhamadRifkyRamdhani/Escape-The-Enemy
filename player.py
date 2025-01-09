import pygame

# player.py

class Player:
    def __init__(self, x, y, character):
        # Muat gambar berdasarkan karakter yang dipilih
        try:
            if character == "chara_1":
                self.normal_image = pygame.image.load("assets/chara_1.png")
                self.shield_image = pygame.image.load("assets/chara_1_shield.png")
            elif character == "chara_2":
                self.normal_image = pygame.image.load("assets/chara_2.png")
                self.shield_image = pygame.image.load("assets/chara_2_shield.png")
            elif character == "chara_3":
                self.normal_image = pygame.image.load("assets/chara_3.png")
                self.shield_image = pygame.image.load("assets/chara_3_shield.png")
            else:
                raise ValueError("Character not recognized")
        except pygame.error as e:
            raise FileNotFoundError(f"Error loading character assets: {e}")

        # Atur ukuran gambar
        # Atur ukuran gambar
        self.normal_image = pygame.transform.scale(self.normal_image, (50, 80))  # Sesuaikan ukuran
        self.shield_image = pygame.transform.scale(self.shield_image, (50, 80))

        self.image = self.normal_image
        self.rect = self.image.get_rect(center=(x, y))

        # Atribut player
        self.speed = 5
        self.health = 3
        self.damage_message = None
        self.damage_message_time = 0

    def update(self, speed=None):
        if speed is not None:
            self.speed = speed  # Gunakan kecepatan yang diberikan
        keys = pygame.key.get_pressed()

        # Pergerakan player
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Batas pergerakan
        screen_width = 800
        screen_height = 520
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, screen_width)
        self.rect.top = max(self.rect.top, screen_height // 1.5)
        self.rect.bottom = min(self.rect.bottom, screen_height)

    def draw(self, screen, shield_active):
        # Tentukan gambar berdasarkan status shield
        if shield_active:
            self.image = self.shield_image
        else:
            self.image = self.normal_image
        screen.blit(self.image, self.rect)

    def handle_collision(self, enemy):
        if hasattr(enemy, 'damage') and isinstance(enemy.damage, (int, float)) and enemy.damage > 0:
            self.health -= enemy.damage
            self.damage_message = f"-{enemy.damage}"
            self.damage_message_time = pygame.time.get_ticks()
            self.damage_message_pos = (self.rect.centerx, self.rect.top - 20)  # Atur posisi damage text

    def draw_damage_message(self, screen, font):
        if self.damage_message and pygame.time.get_ticks() - self.damage_message_time < 2000:  # Perpanjang waktu tampilan
            text_surface = font.render(self.damage_message, True, (255, 0, 0))
            screen.blit(text_surface, self.damage_message_pos)  # Gambar teks di posisi yang tepat
