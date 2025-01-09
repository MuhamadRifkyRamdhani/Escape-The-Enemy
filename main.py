import pygame
import sys
from player import Player
from enemy import Enemy
from powerup import PowerUp
import random

pygame.init()

# Dimensi layar
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Escape The Enemy")

# Warna
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

selected_character = None

# Pengaturan waktu dan font
clock = pygame.time.Clock()
font = pygame.font.Font("assets/ARCADECLASSIC.ttf", 36)

# Suara dan musik
hit_sound = pygame.mixer.Sound("assets/hit.wav")
game_over_sound = pygame.mixer.Sound("assets/failed.mp3")
pygame.mixer.music.load("assets/backsound.mp3")
pygame.mixer.music.set_volume(0.5)

# Variabel global untuk skor
start_ticks = 0  # Diatur ulang setiap kali game dimulai

class DamageText:
    def __init__(self, x, y, text, color=(255, 0, 0), lifetime=1000):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.start_time = pygame.time.get_ticks()

    def draw(self, screen, font):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed < self.lifetime:
            text_surface = font.render(self.text, True, self.color)
            screen.blit(text_surface, (self.x, self.y))
            self.y -= 1  # Teks naik perlahan
        return elapsed < self.lifetime

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def load_health_images(width, height):
    """Load gambar untuk health bar berdasarkan jumlah nyawa, dengan ukuran yang dapat diatur."""
    try:
        return {
            3: pygame.transform.scale(pygame.image.load("assets/health_full.png"), (140, 50)),
            2: pygame.transform.scale(pygame.image.load("assets/health_2.png"), (140, 50)),
            1: pygame.transform.scale(pygame.image.load("assets/health_1.png"), (140, 50)),
            0: pygame.transform.scale(pygame.image.load("assets/health_empty.png"), (140, 50)),
        }
    except pygame.error as e:
        print(f"Error loading health bar images: {e}")
        sys.exit()  # Berhenti jika terjadi error saat memuat gambar




def draw_health_bar(screen, health, health_images):
    """Gambar health bar berdasarkan jumlah nyawa."""
    health_image = health_images.get(health, health_images[0])  # Default ke gambar kosong jika nyawa tidak valid
    health_rect = health_image.get_rect(topleft=(0, 100))  # Posisi health bar
    screen.blit(health_image, health_rect)

class Button:
    """Kelas untuk membuat tombol dengan gambar yang dapat diatur ukurannya."""
    def __init__(self, image_path, position, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))  # Atur ukuran gambar tombol
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Coin:
    def __init__(self):
        self.image = pygame.image.load("assets/coin.png")
        self.image = pygame.transform.scale(self.image, (50, 50))  # Sesuaikan ukuran
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = -50  # Mulai di luar layar
        self.speed = 2

    def update(self):
        self.rect.y += self.speed  # Gerakan jatuh

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def main_menu():
    """Tampilan menu utama."""
    global selected_character
    pygame.init()
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((800, 530))
    pygame.display.set_caption("Escape The Enemy")
    # Muat gambar background
    background = pygame.image.load("assets/main_menu.png")  # Gambar menu Anda
    background = pygame.transform.scale(background, (screen_width, screen_height))  # Sesuaikan ukuran dengan layar

    # Tombol dengan gambar dan ukuran yang dapat diatur
    start_button = Button("assets/start_button.png", (400, 260), 200, 80)
    hero_button = Button("assets/hero_button.png", (400, 360), 200, 80)  # Tombol Hero
    quit_button = Button("assets/quit_button.png", (400, 460), 200, 80)

    running = True
    while running:
        # Tampilkan gambar background
        screen.blit(background, (0, 0))

        # Gambar teks dan tombol
        screen.blit(background, (0, 0))
        start_button.draw(screen)
        hero_button.draw(screen)
        quit_button.draw(screen)
        
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.is_clicked(event):
                    if not selected_character:
                        draw_text("Choose your hero first!", font, RED, screen, 400, 500)
                        pygame.display.flip()
                        pygame.time.delay(2000)  # Tampilkan peringatan selama 2 detik
                    else:
                        main()  # Mulai game
                        running = False

            if hero_button.is_clicked(event):
                character_selection()  # Ke layar pemilihan karakter
                
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

# Tambahkan efek teks
class DamageText:
    def __init__(self, x, y, text, color=(255, 0, 0), lifetime=1000):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.start_time = pygame.time.get_ticks()

    def draw(self, screen, font):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed < self.lifetime:
            text_surface = font.render(self.text, True, self.color)
            screen.blit(text_surface, (self.x, self.y))
            self.y -= 1  # Teks naik perlahan
        return elapsed < self.lifetime  # Hapus teks jika waktunya habis

def get_enemies_for_level(level):
    """Menghasilkan musuh dengan properti acak berdasarkan level."""
    enemies = []
    max_enemies = min(level + 2, 10)  # Batasi jumlah musuh berdasarkan level
    for _ in range(max_enemies):
        enemy_type = random.choice(["rock", "fire", "bomb"])
        new_enemy = Enemy(enemy_type)
        new_enemy.speed = random.randint(2 + level, 5 + level)  # Kecepatan musuh bertambah
        new_enemy.movement_pattern = random.choice(["zigzag", "linear", "random"])
        enemies.append(new_enemy)
    return enemies


def character_selection():
    global selected_character  # Variabel global untuk menyimpan pilihan karakter
    pygame.init()
    screen = pygame.display.set_mode((800, 530))
    # Muat gambar latar belakang
    background = pygame.image.load("assets/bg_hero.png")
    background = pygame.transform.scale(background, (800, 530))

    # Gambar karakter
    chara_1_image = pygame.image.load("assets/chara_1.png")
    chara_2_image = pygame.image.load("assets/chara_2.png")
    chara_3_image = pygame.image.load("assets/chara_3.png")

    # Ubah ukuran gambar karakter
    chara_1_image = pygame.transform.scale(chara_1_image, (100, 150))
    chara_2_image = pygame.transform.scale(chara_2_image, (100, 150))
    chara_3_image = pygame.transform.scale(chara_3_image, (100, 150))

    chara_1_rect = chara_1_image.get_rect(center=(200, 265))
    chara_2_rect = chara_2_image.get_rect(center=(400, 265))
    chara_3_rect = chara_3_image.get_rect(center=(600, 265))

    confirm_button = Button("assets/confirm_button.png", (400, 450), 200, 80)
    temp_selected_character = None  # Pilihan sementara sebelum konfirmasi

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Gambar karakter
        screen.blit(chara_1_image, chara_1_rect)
        screen.blit(chara_2_image, chara_2_rect)
        screen.blit(chara_3_image, chara_3_rect)

        # Gambar border di sekitar karakter yang dipilih sementara
        if temp_selected_character == "chara_1":
            pygame.draw.rect(screen, (255, 255, 255), chara_1_rect.inflate(10, 10), 3)
        elif temp_selected_character == "chara_2":
            pygame.draw.rect(screen, (255, 255, 255), chara_2_rect.inflate(10, 10), 3)
        elif temp_selected_character == "chara_3":
            pygame.draw.rect(screen, (255, 255, 255), chara_3_rect.inflate(10, 10), 3)

        confirm_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if chara_1_rect.collidepoint(event.pos):
                    temp_selected_character = "chara_1"
                elif chara_2_rect.collidepoint(event.pos):
                    temp_selected_character = "chara_2"
                elif chara_3_rect.collidepoint(event.pos):
                    temp_selected_character = "chara_3"

                if confirm_button.is_clicked(event) and temp_selected_character:
                    selected_character = temp_selected_character
                    running = False  # Keluar dari loop untuk kembali ke menu utama



def main():
    pygame.mixer.music.play(-1)

    global start_ticks, coin  # Tambahkan ini agar dapat mengubah variabel global
    start_ticks = pygame.time.get_ticks()  # Reset skor

    coin = None

    if not selected_character:
        character_selection()

    # Pastikan karakter sudah dipilih sebelum memulai permainan
    if not selected_character:
        print("No character selected! Exiting...")
        pygame.quit()
        sys.exit()

    # Buat objek player menggunakan karakter yang dipilih
    player = Player(screen_width // 2, screen_height - 50, selected_character)

    level = 1
    level_increase_timer = pygame.time.get_ticks()
    power_ups = []
    enemies = []

    backgrounds = [
        pygame.image.load("assets/bg_level_1.png"),
        pygame.image.load("assets/bg_level_2.png"),
        pygame.image.load("assets/bg_level_3.png"),
        pygame.image.load("assets/bg_level_4.png"),
    ]
    backgrounds = [pygame.transform.scale(bg, (screen_width, screen_height)) for bg in backgrounds]
    current_background_index = 0
    current_background_y = 0  # Posisi awal background (untuk efek bergerak)

    health_images = load_health_images(220, 180)
    player_speed = 5  # Kecepatan default pemain
    shield_active = False
    shield_timer = 0
    slow_active = False
    slow_timer = 0
    next_enemy_time = pygame.time.get_ticks() + random.randint(1000, 3000)
    next_powerup_time = pygame.time.get_ticks() + random.randint(3000, 8000)

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Tingkatkan level setiap 10 detik
        if current_time - level_increase_timer > 10000:
            level += 1
            level_increase_timer = current_time

            if level % 3 == 0 and current_background_index < len(backgrounds) - 1:
                current_background_index += 1

        if level == 9 and 80000 <= current_time - start_ticks <= 100000 and not coin:
            coin = Coin()

        if coin is not None:
            coin.update()
            if player.rect.colliderect(coin.rect):
                pygame.mixer.music.stop()
                you_win()
                return

        # Spawn musuh secara acak berdasarkan waktu
        if current_time >= next_enemy_time:
            enemy_type = random.choice(["rock", "fire", "bomb"])
            new_enemy = Enemy(enemy_type)
            new_enemy.speed = random.randint(2 + level, 5 + level)
            new_enemy.movement_pattern = random.choice(["zigzag", "linear", "random"])
            enemies.append(new_enemy)

            next_enemy_time = current_time + random.randint(max(500, 3000 - level * 200), max(1000, 5000 - level * 300))

        # Spawn power-up secara acak berdasarkan waktu
        if current_time >= next_powerup_time:
            power_up_type = random.choice(["health", "slow", "shield"])
            power_ups.append(PowerUp(effect=power_up_type))
            next_powerup_time = current_time + random.randint(3000, 8000)

        # Efek shield
        if shield_active and current_time - shield_timer > 3000:
            shield_active = False

        # Efek slow
        if slow_active and current_time - slow_timer > 3000:
            slow_active = False
            player_speed = 5

        # Perbarui pemain dan objek lain
        player.update(speed=player_speed if not shield_active else 5)
        for enemy in enemies[:]:
            enemy.update()
            if player.rect.colliderect(enemy.rect):
                if not shield_active:
                    hit_sound.play()
                    player.handle_collision(enemy)
                    player.health -= 1
                enemies.remove(enemy)
                if player.health <= 0:
                    pygame.mixer.music.stop()
                    game_over_sound.play()
                    game_over()
                    return

        for power_up in power_ups[:]:
            power_up.update()
            if player.rect.colliderect(power_up.rect):
                if power_up.effect == "health":
                    player.health = min(player.health + 1, 3)
                elif power_up.effect == "shield":
                    shield_active = True
                    shield_timer = current_time
                elif power_up.effect == "slow":
                    slow_active = True
                    slow_timer = current_time
                    player_speed = max(player_speed // 2, 1)
                power_ups.remove(power_up)

        
        player.draw_damage_message(screen, font)
        # Gambar elemen ke layar
        screen.fill(WHITE)
        screen.blit(backgrounds[current_background_index], (0, current_background_y))
        screen.blit(backgrounds[current_background_index], (0, current_background_y - screen_height))

        player.draw(screen, shield_active)
        for enemy in enemies:
            enemy.draw(screen)
        for power_up in power_ups:
            power_up.draw(screen)
        if coin:
            coin.draw(screen)


        score = (pygame.time.get_ticks() - start_ticks) // 1000
        score_text = font.render(f"Score    {score}", True, WHITE)
        level_text = font.render(f"Level    {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        draw_health_bar(screen, player.health, health_images)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()



def you_win():
    running = True
    while running:
        screen.fill(WHITE)

        # Muat gambar background
        background = pygame.image.load("assets/you_win_bg.png")  # Ganti dengan nama file gambar background yang diinginkan
        background = pygame.transform.scale(background, (screen_width, screen_height))
        screen.blit(background, (0, 0))

        # Tampilkan gambar mahkota
        crown_image = pygame.image.load("assets/crown.png")
        crown_image = pygame.transform.scale(crown_image, (200, 150))
        crown_rect = crown_image.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        screen.blit(crown_image, crown_rect)

        # Tombol kembali ke menu utama
        main_menu_button = Button("assets/main_menu_button.png", (screen_width // 2, screen_height // 2 + 150), 200, 80)
        main_menu_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.is_clicked(event):
                    main_menu()  # Kembali ke menu utama
                    return

        pygame.display.flip()
        clock.tick(60)

        pygame.display.flip()
        clock.tick(60)


def game_over():
    global start_ticks  # Agar bisa akses skor terakhir
    final_score = (pygame.time.get_ticks() - start_ticks) // 1000 # Hitung skor akhir

    pygame.mixer.music.load("assets/game_over_bg.mp3")
    pygame.mixer.music.play(-1)

    # Muat gambar background untuk game over
    background = pygame.image.load("assets/bggameover.png")
    background = pygame.transform.scale(background, (screen_width, screen_height))

    retry_button = Button("assets/retry_button.png", (screen_width // 2, 300), 200, 80)
    menu_button = Button("assets/menu_button.png", (screen_width // 2, 430), 200, 80)

    while True:
        screen.blit(background, (0, 0))  # Gambar background

        draw_text("Game Over!", font, WHITE, screen, screen_width // 2, 200)
        draw_text(f"Your Score is  {final_score}", font, WHITE, screen, screen_width // 2, 150)  # Tampilkan skor terakhir

        retry_button.draw(screen)
        menu_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if retry_button.is_clicked(event):
                pygame.mixer.music.stop()
                pygame.mixer.music.load("assets/backsound.mp3")  # Muat ulang backsound awal
                pygame.mixer.music.set_volume(0.5)
                main()  # Mulai ulang game
                return
            if menu_button.is_clicked(event):
                pygame.mixer.music.stop()
                main_menu()
                return



def draw_text(text, font, color, surface, x, y):
    """Gambar teks di posisi tertentu."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


if __name__ == "__main__":
    main_menu()
