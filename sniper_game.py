import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sniper Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player (sniper) shape (green triangle)
sniper_width = 30
sniper_height = 40
sniper_rect = pygame.Rect(SCREEN_WIDTH // 2 - sniper_width // 2, SCREEN_HEIGHT - sniper_height - 10, sniper_width, sniper_height)

# Enemy shape (red star)
enemy_list = []
ENEMY_SPEED = 2
enemy_size = 20

# Bullet properties
bullet_list = []
BULLET_SPEED = -10

# Player's score
score = 0
font = pygame.font.Font(None, 36)

# Function to spawn a new enemy (red stars)
def spawn_enemy():
    x = random.randint(0, SCREEN_WIDTH - enemy_size)
    y = -enemy_size
    enemy_list.append(pygame.Rect(x, y, enemy_size, enemy_size))

# Function to draw text on the screen
def draw_text(text, x, y):
    render = font.render(text, True, WHITE)
    screen.blit(render, (x, y))

# Function to draw a green triangle (sniper)
def draw_sniper():
    points = [(sniper_rect.centerx, sniper_rect.top), 
              (sniper_rect.left, sniper_rect.bottom), 
              (sniper_rect.right, sniper_rect.bottom)]
    pygame.draw.polygon(screen, GREEN, points)

# Function to draw a red star (enemy)
def draw_enemy(enemy_rect):
    points = [
        (enemy_rect.centerx, enemy_rect.top),
        (enemy_rect.left + 8, enemy_rect.bottom - 5),
        (enemy_rect.left + 20, enemy_rect.bottom - 5),
        (enemy_rect.left + 10, enemy_rect.bottom - 20),
        (enemy_rect.right - 8, enemy_rect.bottom - 5)
    ]
    pygame.draw.polygon(screen, RED, points)

# Show start screen
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

# Show game over screen with options to retry or quit
def show_game_over():
    screen.fill(BLACK)
    draw_text("Game Over!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3)
    draw_text(f"Your score: {score}", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    draw_text("Press R to Retry or Q to Quit", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()

# Reset the game state
def reset_game():
    global score, enemy_list, bullet_list, ENEMY_SPEED
    score = 0
    enemy_list = []
    bullet_list = []
    ENEMY_SPEED = 2  # Reset the enemy speed
    sniper_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - sniper_height - 10)

# Main game loop
clock = pygame.time.Clock()
running = True

# Show start screen
show_start_screen()

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement (sniper)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and sniper_rect.left > 0:
        sniper_rect.x -= 5
    if keys[pygame.K_RIGHT] and sniper_rect.right < SCREEN_WIDTH:
        sniper_rect.x += 5

    # Shoot bullets
    if keys[pygame.K_SPACE]:
        bullet_rect = pygame.Rect(sniper_rect.centerx - 5, sniper_rect.top - 10, 10, 20)
        bullet_list.append(bullet_rect)
    
    # Spawn new enemies
    if random.randint(1, 60) == 1:
        spawn_enemy()

    # Move enemies
    for enemy_rect in enemy_list[:]:
        enemy_rect.y += ENEMY_SPEED
        if enemy_rect.top > SCREEN_HEIGHT:
            enemy_list.remove(enemy_rect)

    # Move bullets
    for bullet_rect in bullet_list[:]:
        bullet_rect.y += BULLET_SPEED
        if bullet_rect.bottom < 0:
            bullet_list.remove(bullet_rect)

    # Check for collisions
    for enemy_rect in enemy_list[:]:
        for bullet_rect in bullet_list[:]:
            if enemy_rect.colliderect(bullet_rect):
                enemy_list.remove(enemy_rect)
                bullet_list.remove(bullet_rect)
                score += 10
                # Increase the enemy speed each time an enemy is destroyed
                ENEMY_SPEED += 0.1

    # Check if sniper hits an enemy
    for enemy_rect in enemy_list[:]:
        if sniper_rect.colliderect(enemy_rect):
            show_game_over()
            running = False
            break

    # Draw enemies (red stars)
    for enemy_rect in enemy_list:
        draw_enemy(enemy_rect)

    # Draw bullets
    for bullet_rect in bullet_list:
        pygame.draw.rect(screen, WHITE, bullet_rect)

    # Draw player (green triangle)
    draw_sniper()

    # Draw score
    draw_text(f"Score: {score}", 10, 10)

    # Update the screen
    pygame.display.flip()
    clock.tick(60)

    # Check if game is over and handle user input for retry/quit
    if not running:
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Retry
                        reset_game()
                        running = True
                        waiting_for_input = False
                    elif event.key == pygame.K_q:  # Quit
                        pygame.quit()
                        sys.exit()

pygame.quit()
sys.exit()
