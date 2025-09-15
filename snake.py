# Snake Game using pygame
import pygame
import sys
import random
import json
import os
import time

# Initialize pygame
pygame.init()

class Config:
    # Game settings
    WIDTH = 1200
    HEIGHT = 800
    BLOCK_SIZE = 40
    INITIAL_SPEED = 15
    
    # Nokia 3310 retro colors
    NOKIA_GREEN = (155, 188, 15)  # Light green background like Nokia screen
    NOKIA_BLACK = (0, 0, 0)      # Black for sprites
    NOKIA_DARK_GREEN = (48, 98, 48)  # Darker green for contrast
    
    # Colors
    BLACK = NOKIA_BLACK
    WHITE = NOKIA_BLACK  # Use black instead of white for text
    GREEN = NOKIA_BLACK  # Snake will be black
    RED = NOKIA_BLACK    # Food will be black
    BLUE = NOKIA_BLACK   # Power-ups will be black
    BACKGROUND = NOKIA_GREEN
    
    # Controls
    CONTROLS = {
        'up': [pygame.K_UP, pygame.K_w],
        'down': [pygame.K_DOWN, pygame.K_s],
        'left': [pygame.K_LEFT, pygame.K_a],
        'right': [pygame.K_RIGHT, pygame.K_d],
        'pause': pygame.K_p,
        'quit': pygame.K_q
    }

# Game settings
WIDTH, HEIGHT = Config.WIDTH, Config.HEIGHT
BLOCK_SIZE = Config.BLOCK_SIZE
SPEED = Config.INITIAL_SPEED

# Set up display
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Set up clock
CLOCK = pygame.time.Clock()

class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    PAUSED = 3

class Difficulty:
    EASY = {"speed": 10, "name": "Easy"}
    MEDIUM = {"speed": 15, "name": "Medium"}
    HARD = {"speed": 20, "name": "Hard"}

class PowerUp:
    def __init__(self, pos, type_):
        self.pos = pos
        self.type = type_  # "speed", "slow", "score_boost"
        self.spawn_time = time.time()
        self.duration = 10  # seconds

class GameStats:
    def __init__(self):
        self.games_played = 0
        self.total_score = 0
        self.best_score = 0
        self.average_score = 0
    
    def update_stats(self, score):
        self.games_played += 1
        self.total_score += score
        self.best_score = max(self.best_score, score)
        self.average_score = self.total_score / self.games_played

def random_food_position():
    x = random.randrange(0, WIDTH, BLOCK_SIZE)
    y = random.randrange(0, HEIGHT, BLOCK_SIZE)
    return (x, y)

def draw_snake(snake_list):
    for i, pos in enumerate(snake_list):
        # Draw solid black rectangles for retro look
        pygame.draw.rect(WINDOW, Config.NOKIA_BLACK, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        # Add a small border for definition
        pygame.draw.rect(WINDOW, Config.NOKIA_DARK_GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE), 2)

def draw_food(food_pos):
    # Draw love heart for food (retro style)
    center_x = food_pos[0] + BLOCK_SIZE // 2
    center_y = food_pos[1] + BLOCK_SIZE // 2
    
    # Draw heart shape using circles and a triangle
    heart_size = BLOCK_SIZE // 3
    
    # Left circle of heart
    pygame.draw.circle(WINDOW, Config.NOKIA_BLACK, 
                      (center_x - heart_size//2, center_y - heart_size//4), 
                      heart_size//2)
    
    # Right circle of heart
    pygame.draw.circle(WINDOW, Config.NOKIA_BLACK, 
                      (center_x + heart_size//2, center_y - heart_size//4), 
                      heart_size//2)
    
    # Bottom triangle/diamond part of heart
    heart_points = [
        (center_x - heart_size, center_y),
        (center_x + heart_size, center_y),
        (center_x, center_y + heart_size)
    ]
    pygame.draw.polygon(WINDOW, Config.NOKIA_BLACK, heart_points)
    
    # Add border for retro definition
    pygame.draw.circle(WINDOW, Config.NOKIA_DARK_GREEN, 
                      (center_x - heart_size//2, center_y - heart_size//4), 
                      heart_size//2, 2)
    pygame.draw.circle(WINDOW, Config.NOKIA_DARK_GREEN, 
                      (center_x + heart_size//2, center_y - heart_size//4), 
                      heart_size//2, 2)
    pygame.draw.polygon(WINDOW, Config.NOKIA_DARK_GREEN, heart_points, 2)
    
def load_high_score():
    if os.path.exists("high_score.json"):
        with open("high_score.json", "r") as f:
            return json.load(f).get("high_score", 0)
    return 0

def save_high_score(score):
    with open("high_score.json", "w") as f:
        json.dump({"high_score": score}, f)

def show_score(score, high_score):
    # Use a monospace font for retro feel
    font = pygame.font.Font(None, 25)  # Default font is monospace-like
    score_text = font.render(f"SCORE: {score:04d}", True, Config.NOKIA_BLACK)  # Zero-padded score
    high_score_text = font.render(f"HIGH: {high_score:04d}", True, Config.NOKIA_BLACK)
    WINDOW.blit(score_text, [10, 10])
    WINDOW.blit(high_score_text, [10, 40])

def game_over_screen(score):
    font = pygame.font.Font(None, 40)
    msg = font.render('GAME OVER', True, Config.NOKIA_BLACK)
    restart_msg = font.render('PRESS C TO PLAY AGAIN', True, Config.NOKIA_BLACK)
    quit_msg = font.render('PRESS Q TO QUIT', True, Config.NOKIA_BLACK)
    
    WINDOW.fill(Config.NOKIA_GREEN)
    
    # Center all messages
    WINDOW.blit(msg, [WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 60])
    WINDOW.blit(restart_msg, [WIDTH // 2 - restart_msg.get_width() // 2, HEIGHT // 2])
    WINDOW.blit(quit_msg, [WIDTH // 2 - quit_msg.get_width() // 2, HEIGHT // 2 + 40])
    
    show_score(score, load_high_score())
    pygame.display.update()

def show_menu():
    WINDOW.fill(Config.NOKIA_GREEN)
    
    # Use simple, retro-style text
    title_font = pygame.font.Font(None, 60)
    text_font = pygame.font.Font(None, 30)
    
    title = title_font.render('SNAKE', True, Config.NOKIA_BLACK)
    start_text = text_font.render('PRESS SPACE TO START', True, Config.NOKIA_BLACK)
    quit_text = text_font.render('PRESS Q TO QUIT', True, Config.NOKIA_BLACK)
    
    WINDOW.blit(title, [WIDTH//2 - title.get_width()//2, HEIGHT//3])
    WINDOW.blit(start_text, [WIDTH//2 - start_text.get_width()//2, HEIGHT//2])
    WINDOW.blit(quit_text, [WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 50])
    pygame.display.update()

def show_pause_screen():
    # Draw a simple pause overlay
    font = pygame.font.Font(None, 40)
    pause_text = font.render('PAUSED', True, Config.NOKIA_BLACK)
    resume_text = font.render('PRESS P TO RESUME', True, Config.NOKIA_BLACK)
    
    # Create a semi-transparent overlay effect by drawing a patterned rectangle
    for x in range(0, WIDTH, 20):
        for y in range(0, HEIGHT, 20):
            if (x + y) % 40 == 0:
                pygame.draw.rect(WINDOW, Config.NOKIA_DARK_GREEN, (x, y, 10, 10))
    
    WINDOW.blit(pause_text, [WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 50])
    WINDOW.blit(resume_text, [WIDTH//2 - resume_text.get_width()//2, HEIGHT//2])
    pygame.display.update()

def adjust_speed(score):
    # Increase speed as score increases
    base_speed = 10
    return min(base_speed + score // 5, 25)

def spawn_powerup():
    if random.randint(1, 100) <= 5:  # 5% chance
        pos = random_food_position()
        power_type = random.choice(["speed", "slow", "score_boost"])
        return PowerUp(pos, power_type)
    return None

def handle_input(event, dx, dy):
    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_LEFT, pygame.K_a] and dx == 0:
            return -BLOCK_SIZE, 0
        elif event.key in [pygame.K_RIGHT, pygame.K_d] and dx == 0:
            return BLOCK_SIZE, 0
        elif event.key in [pygame.K_UP, pygame.K_w] and dy == 0:
            return 0, -BLOCK_SIZE
        elif event.key in [pygame.K_DOWN, pygame.K_s] and dy == 0:
            return 0, BLOCK_SIZE
    return dx, dy

def main():
    x = WIDTH // 2
    y = HEIGHT // 2
    dx = 0
    dy = 0
    snake_list = []
    snake_length = 1
    food_pos = random_food_position()
    running = True
    game_over = False
    paused = False
    high_score = load_high_score()
    game_state = GameState.MENU
    powerup = None
    stats = GameStats()
    current_speed = SPEED

    while running:
        if game_state == GameState.MENU:
            show_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_SPACE:
                        game_state = GameState.PLAYING

        elif game_state == GameState.PLAYING:
            if game_over:
                game_over_screen(snake_length - 1)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False
                        if event.key == pygame.K_c:
                            x = WIDTH // 2
                            y = HEIGHT // 2
                            dx = 0
                            dy = 0
                            snake_list = []
                            snake_length = 1
                            food_pos = random_food_position()
                            game_over = False
                            current_speed = SPEED
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    if not paused and not game_over:
                        dx, dy = handle_input(event, dx, dy)

            if not paused and not game_over:
                if dx != 0 or dy != 0:
                    x += dx
                    y += dy

                if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                    game_over = True
                    continue

                head = (x, y)
                snake_list.append(head)
                if len(snake_list) > snake_length:
                    del snake_list[0]

                for segment in snake_list[:-1]:
                    if segment == head:
                        game_over = True
                        continue

                if head == food_pos:
                    snake_length += 1
                    while True:
                        food_pos = random_food_position()
                        if food_pos not in snake_list:
                            break

                if powerup is None or time.time() - powerup.spawn_time > powerup.duration:
                    powerup = spawn_powerup()

                if powerup:
                    if head == powerup.pos:
                        if powerup.type == "speed":
                            current_speed += 5
                        elif powerup.type == "slow":
                            current_speed = max(5, current_speed - 5)
                        elif powerup.type == "score_boost":
                            snake_length += 5
                        powerup = None

                if snake_length - 1 > high_score:
                    high_score = snake_length - 1
                    save_high_score(high_score)

                # Draw everything with Nokia green background
                WINDOW.fill(Config.NOKIA_GREEN)
                draw_snake(snake_list)
                draw_food(food_pos)
                if powerup:
                    # Draw power-up as a different pattern
                    pygame.draw.rect(WINDOW, Config.NOKIA_BLACK, (powerup.pos[0], powerup.pos[1], BLOCK_SIZE, BLOCK_SIZE))
                    # Add cross pattern to distinguish from food
                    pygame.draw.line(WINDOW, Config.NOKIA_GREEN, 
                                   (powerup.pos[0], powerup.pos[1] + BLOCK_SIZE//2), 
                                   (powerup.pos[0] + BLOCK_SIZE, powerup.pos[1] + BLOCK_SIZE//2), 3)
                    pygame.draw.line(WINDOW, Config.NOKIA_GREEN, 
                                   (powerup.pos[0] + BLOCK_SIZE//2, powerup.pos[1]), 
                                   (powerup.pos[0] + BLOCK_SIZE//2, powerup.pos[1] + BLOCK_SIZE), 3)
                show_score(snake_length - 1, high_score)
                pygame.display.update()

            elif paused and not game_over:
                show_pause_screen()

        CLOCK.tick(adjust_speed(snake_length - 1))

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
