import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants for game screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 15
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))

# Frame rate
FPS = 60

# Score
score_left = 0
score_right = 0
font = pygame.font.Font(None, 74)

# Initialize the paddles
left_paddle = pygame.Rect(10, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 10 - PADDLE_WIDTH, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Initialize the ball
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Function to reset the ball to the center
def reset_ball(winner):
    global ball_speed_x, ball_speed_y, score_left, score_right
    time.sleep(1)  # Wait for 1 second before resetting
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))
    if winner == 'left':
        score_right = 0
        score_left = 0
    elif winner == 'right':
        score_right = 0
        score_left = 0

# Function to display victory message
def display_victory_message(winner):
    screen.fill(BLACK)
    if winner == 'left':
        text = font.render('Left Player Wins!', True, WHITE)
    else:
        text = font.render('Right Player Wins!', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(3)  # Display the message for 3 seconds

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse movement
    mouse_y = pygame.mouse.get_pos()[1]
    left_paddle.y = mouse_y - (PADDLE_HEIGHT // 2)
    if left_paddle.y < 0:
        left_paddle.y = 0
    if left_paddle.y > SCREEN_HEIGHT - PADDLE_HEIGHT:
        left_paddle.y = SCREEN_HEIGHT - PADDLE_HEIGHT

    # AI for the right paddle
    if right_paddle.centery < ball.centery:
        right_paddle.y += min(PADDLE_SPEED, ball.centery - right_paddle.centery)
    elif right_paddle.centery > ball.centery:
        right_paddle.y -= min(PADDLE_SPEED, right_paddle.centery - ball.centery)
    if right_paddle.y < 0:
        right_paddle.y = 0
    if right_paddle.y > SCREEN_HEIGHT - PADDLE_HEIGHT:
        right_paddle.y = SCREEN_HEIGHT - PADDLE_HEIGHT

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top/bottom
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1

    # Ball goes off screen, score points
    if ball.left <= 0:
        score_right += 1
        if score_right == 5:
            display_victory_message('right')
            reset_ball('right')
        else:
            reset_ball(None)
    elif ball.right >= SCREEN_WIDTH:
        score_left += 1
        if score_left == 5:
            display_victory_message('left')
            reset_ball('left')
        else:
            reset_ball(None)

    # Fill the screen
    screen.fill(BLACK)

    # Draw the score
    text = font.render(str(score_left), True, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(score_right), True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - 250, 10))

    # Draw everything else
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Updating the window
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
