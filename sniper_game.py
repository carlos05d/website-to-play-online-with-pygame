from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Game state
player_position = {"x": 375, "y": 550}
score = 0
bullets = []
enemies = []
game_over = False

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
player_speed = 5
bullet_speed = 10
enemy_speed = 2
enemy_spawn_rate = 0.02  # Rate of enemy spawning

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('move_player')
def handle_move(data):
    global player_position, game_over
    if game_over:
        return
    if data['direction'] == 'left' and player_position['x'] > 0:
        player_position['x'] -= player_speed
    elif data['direction'] == 'right' and player_position['x'] < SCREEN_WIDTH - 50:
        player_position['x'] += player_speed
    emit('update_game', {
        'player_position': player_position, 
        'bullets': bullets, 
        'enemies': enemies, 
        'score': score, 
        'game_over': game_over
    }, broadcast=True)

@socketio.on('shoot')
def handle_shoot(data):
    if game_over:
        return
    bullets.append({'x': player_position['x'] + 22.5, 'y': player_position['y']})
    emit('update_game', {
        'player_position': player_position, 
        'bullets': bullets, 
        'enemies': enemies, 
        'score': score, 
        'game_over': game_over
    }, broadcast=True)

def spawn_enemy():
    x = random.randint(0, SCREEN_WIDTH - 50)
    enemies.append({'x': x, 'y': -50})

def move_bullets():
    global score
    for bullet in bullets[:]:
        bullet['y'] -= bullet_speed
        if bullet['y'] < 0:
            bullets.remove(bullet)
        # Collision detection
        for enemy in enemies[:]:
            if (bullet['x'] > enemy['x'] and bullet['x'] < enemy['x'] + 50) and \
               (bullet['y'] > enemy['y'] and bullet['y'] < enemy['y'] + 50):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10

def move_enemies():
    global score, game_over
    for enemy in enemies[:]:
        enemy['y'] += enemy_speed
        if enemy['y'] > SCREEN_HEIGHT:
            enemies.remove(enemy)
            score -= 10
        # Collision with player
        if (enemy['x'] < player_position['x'] + 50 and enemy['x'] + 50 > player_position['x'] and
            enemy['y'] < player_position['y'] + 50 and enemy['y'] + 50 > player_position['y']):
            game_over = True
            emit('game_over', broadcast=True)

def game_logic():
    if not game_over:
        if random.random() < enemy_spawn_rate:
            spawn_enemy()
        move_bullets()
        move_enemies()

# Periodically update the game state
@socketio.on('start_game')
def start_game(data):
    global score, bullets, enemies, game_over
    bullets = []
    enemies = []
    score = 0
    game_over = False
    player_position['x'] = SCREEN_WIDTH // 2 - 25
    player_position['y'] = SCREEN_HEIGHT - 60
    while not game_over:
        game_logic()
        emit('update_game', {
            'player_position': player_position, 
            'bullets': bullets, 
            'enemies': enemies, 
            'score': score, 
            'game_over': game_over
        }, broadcast=True)
        socketio.sleep(0.1)

@socketio.on('restart_game')
def restart_game(data):
    global score, bullets, enemies, game_over
    bullets = []
    enemies = []
    score = 0
    game_over = False
    player_position['x'] = SCREEN_WIDTH // 2 - 25
    player_position['y'] = SCREEN_HEIGHT - 60
    emit('update_game', {
        'player_position': player_position, 
        'bullets': bullets, 
        'enemies': enemies, 
        'score': score, 
        'game_over': game_over
    }, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
