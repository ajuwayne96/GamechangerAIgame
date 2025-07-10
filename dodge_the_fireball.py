import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔥 Dodge the Fireball!")

# Colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)

# Load background image
background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load music and sound
pygame.mixer.music.load("assets/bg_music.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

move_sound = pygame.mixer.Sound("assets/move.wav")
move_sound.set_volume(0.4)

# Load assets
player_size = 40
boss_size = 80
fireball_radius = 10

player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (player_size, player_size))

boss_img = pygame.image.load("assets/boss.png")
boss_img = pygame.transform.scale(boss_img, (boss_size, boss_size))

fireball_img = pygame.image.load("assets/fireball.png")
fireball_img = pygame.transform.scale(fireball_img, (fireball_radius*2, fireball_radius*2))

# Menu UI assets
title_img = pygame.image.load("assets/title.png")
title_img = pygame.transform.scale(title_img, (300, 100))
title_rect = title_img.get_rect(center=(WIDTH // 2, 180))

start_img = pygame.image.load("assets/start.png")
start_img = pygame.transform.scale(start_img, (180, 60))
start_rect = start_img.get_rect(center=(WIDTH // 2, 300))

quit_img = pygame.image.load("assets/quit.png")
quit_img = pygame.transform.scale(quit_img, (180, 60))
quit_rect = quit_img.get_rect(center=(WIDTH // 2, 380))

# Retry screen UI
retry_img = pygame.image.load("assets/retry.png")
retry_img = pygame.transform.scale(retry_img, (150, 50))
retry_rect = retry_img.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))

retry_quit_img = pygame.image.load("assets/quit.png")
retry_quit_img = pygame.transform.scale(retry_quit_img, (150, 50))
retry_quit_rect = retry_quit_img.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

def game_over_screen():
    while True:
        win.blit(background, (0, 0))
        win.blit(retry_img, retry_rect)
        win.blit(retry_quit_img, retry_quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    run_game()
                elif retry_quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def run_game():
    player_x = WIDTH // 2
    player_y = HEIGHT - player_size - 10
    player_speed = 5

    boss_x = WIDTH // 2 - boss_size // 2
    boss_y = 30

    fireballs = []
    fireball_speed = 4
    score = 0
    moving = False
    running = True

    while running:
        clock.tick(60)
        win.blit(background, (0, 0))
        moving = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            moving = True
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
            moving = True
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
            moving = True
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
            player_y += player_speed
            moving = True

        if moving:
            if not pygame.mixer.Channel(1).get_busy():
                pygame.mixer.Channel(1).play(move_sound)
        else:
            pygame.mixer.Channel(1).stop()

        # Fireballs from boss
        if random.randint(1, 30) == 1:
            target_x = player_x + random.randint(-30, 30)
            angle = math.atan2(player_y - boss_y, target_x - boss_x)
            dx = fireball_speed * math.cos(angle)
            dy = fireball_speed * math.sin(angle)
            fireballs.append([boss_x + boss_size//2, boss_y + boss_size, dx, dy])

        for fb in fireballs[:]:
            fb[0] += fb[2]
            fb[1] += fb[3]
            if fb[1] > HEIGHT or fb[0] < 0 or fb[0] > WIDTH:
                fireballs.remove(fb)
                score += 1

            dist = math.hypot(fb[0] - (player_x + player_size // 2), fb[1] - (player_y + player_size // 2))
            if dist < player_size // 2 + fireball_radius:
                game_over_screen()

        # Draw sprites
        win.blit(player_img, (player_x, player_y))
        win.blit(boss_img, (boss_x, boss_y))
        for fb in fireballs:
            win.blit(fireball_img, (int(fb[0] - fireball_radius), int(fb[1] - fireball_radius)))

        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))

        pygame.display.flip()

def show_menu():
    while True:
        win.blit(background, (0, 0))
        win.blit(title_img, title_rect)
        win.blit(start_img, start_rect)
        win.blit(quit_img, quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    run_game()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Start with menu
show_menu()
