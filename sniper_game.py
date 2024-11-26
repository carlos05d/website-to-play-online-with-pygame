import pygame
import random
import sys

# Initialize the game
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sniper Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Sniper (player) setup
sniper_rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 60, 50, 50)

# Enemy setup
enemy_list = []
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 40
ENEMY_SPEED = 2

# Bullet setup
bullet_list = []
BULLET_WIDTH, BULLET_HEIGHT = 10, 20
BULLET_SPEED = -10

# Player score
score = 0
font = pygame.font.Font(None, 36)

# Function to spawn enemies
def spawn_enemy():
    x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
    y = -ENEMY_HEIGHT
    enemy_list.append(pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT))

# Function to draw text
def draw_text(text, x, y):
    render = font.render(text, True, WHITE)
    screen.blit(render, (x, y))

# Start screen function
def show_start_screen():
    screen.fill(BLACK)
    draw_text("Press any key to start", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Main game loop
clock = pygame.time.Clock()
show_start_screen()
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and sniper_rect.left > 0:
        sniper_rect.x -= 5
    if keys[pygame.K_RIGHT] and sniper_rect.right < SCREEN_WIDTH:
        sniper_rect.x += 5

    # Shooting bullets
    if keys[pygame.K_SPACE]:
        bullet_rect = pygame.Rect(sniper_rect.centerx - BULLET_WIDTH // 2, sniper_rect.top - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
        bullet_list.append(bullet_rect)

    # Update enemies
    if random.randint(1, 60) == 1:
        
        spawn_enemy()

    for enemy_rect in enemy_list[:]:
        enemy_rect.y += ENEMY_SPEED
        if enemy_rect.top > SCREEN_HEIGHT:
            enemy_list.remove(enemy_rect)

    # Update bullets
    for bullet_rect in bullet_list[:]:
        bullet_rect.y += BULLET_SPEED
        if bullet_rect.bottom < 0:
            bullet_list.remove(bullet_rect)

    # Check collisions
    for enemy_rect in enemy_list[:]:
        for bullet_rect in bullet_list[:]:
            if enemy_rect.colliderect(bullet_rect):
                enemy_list.remove(enemy_rect)
                bullet_list.remove(bullet_rect)
                score += 10

    # Draw enemies
    for enemy_rect in enemy_list:
        pygame.draw.rect(screen, RED, enemy_rect)

    # Draw bullets
    for bullet_rect in bullet_list:
        pygame.draw.rect(screen, YELLOW, bullet_rect)

    # Draw player
    pygame.draw.rect(screen, BLUE, sniper_rect)

    # Display score
    draw_text(f"Score: {score}", 10, 10)

    # Update screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
           