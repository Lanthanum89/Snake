# Snake Game using pygame
import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
SPEED = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up display
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Set up clock
CLOCK = pygame.time.Clock()

def random_food_position():
    x = random.randrange(0, WIDTH, BLOCK_SIZE)
    y = random.randrange(0, HEIGHT, BLOCK_SIZE)
    return (x, y)

def draw_snake(snake_list):
    for pos in snake_list:
        pygame.draw.rect(WINDOW, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

def show_score(score):
    font = pygame.font.SysFont(None, 35)
    value = font.render(f"Score: {score}", True, WHITE)
    WINDOW.blit(value, [0, 0])

def game_over_screen(score):
    font = pygame.font.SysFont(None, 50)
    msg = font.render('Game Over! Press Q-Quit or C-Play Again', True, RED)
    WINDOW.fill(BLACK)
    WINDOW.blit(msg, [WIDTH // 10, HEIGHT // 3])
    show_score(score)
    pygame.display.update()

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

    while running:
        while game_over:
            game_over_screen(snake_length - 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_c:
                        main()
                        return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -BLOCK_SIZE
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = BLOCK_SIZE
                    dx = 0

        if dx != 0 or dy != 0:
            x += dx
            y += dy

        # Check boundaries
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_over = True

        head = (x, y)
        snake_list.append(head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check self collision
        for segment in snake_list[:-1]:
            if segment == head:
                game_over = True

        WINDOW.fill(BLACK)
        draw_snake(snake_list)
        pygame.draw.rect(WINDOW, RED, (food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        show_score(snake_length - 1)
        pygame.display.update()

        # Check food collision
        if head == food_pos:
            snake_length += 1
            while True:
                food_pos = random_food_position()
                if food_pos not in snake_list:
                    break

        CLOCK.tick(SPEED)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
