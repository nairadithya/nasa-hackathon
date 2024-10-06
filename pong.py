import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions (1280x720 resolution)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH = 80  # Paddle width
PADDLE_HEIGHT = 15  # Increased paddle height for thickness
PADDLE_SPEED = 6  # Player paddle speed
AI_PADDLE_SPEED = 3  # Slower AI paddle speed for "dumb" AI

# Ball settings (Smaller ball)
BALL_SIZE = 15  # Smaller ball size
BALL_SPEED_X = 4  # Slower horizontal speed
BALL_SPEED_Y = 4  # Slower vertical speed

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong Game - Single Player (Dumb AI)')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Paddles (position them closer together)
player_paddle = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT - 120, PADDLE_WIDTH, PADDLE_HEIGHT)
computer_paddle = pygame.Rect(SCREEN_WIDTH // 2 - 70, 120, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_dx = BALL_SPEED_X * random.choice((1, -1))
ball_dy = BALL_SPEED_Y * random.choice((1, -1))

# Score
player_score = 0
computer_score = 0

# Load the custom font with a smaller size
font_path = "BigBlue_Terminal_437TT.ttf"  # Adjust this path as needed
font = pygame.font.Font(font_path, 40)  # Change the size from 74 to 40

# Function to reset the ball after scoring
def reset_ball():
    global ball_dx, ball_dy
    ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
    ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
    ball_dx *= random.choice((1, -1))
    ball_dy *= random.choice((1, -1))

# Function to display the win message
def display_win_message():
    win_message = "YOU WIN YAY !!! but alien is sad :((("
    win_text = font.render(win_message, True, WHITE)
    screen.fill(BLACK)  # Clear the screen
    screen.blit(win_text, (SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2 - 40))  # Center message
    pygame.display.flip()  # Update the screen
    pygame.time.delay(5000)  # Display for 5 seconds
    pygame.quit()
    quit()

# Create static stars for the background limited to the playable area
stars = []
for _ in range(200):  # Increased the number of stars
    star_x = random.randint((SCREEN_WIDTH - 800) // 2, (SCREEN_WIDTH + 800) // 2)  # Stars only in playable width
    star_y = random.randint(130, SCREEN_HEIGHT - 100)  # Ensure stars start below the computer paddle (y = 130)
    stars.append((star_x, star_y))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Player movement (Left/Right arrow keys)
    if keys[pygame.K_LEFT] and player_paddle.left > (SCREEN_WIDTH - 800) // 2:
        player_paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and player_paddle.right < (SCREEN_WIDTH + 800) // 2:
        player_paddle.x += PADDLE_SPEED

    # AI Paddle Movement: Make the AI "dumb"
    if ball.centerx < computer_paddle.centerx:
        computer_paddle.x -= AI_PADDLE_SPEED  # Move left if ball is to the left
    elif ball.centerx > computer_paddle.centerx:
        computer_paddle.x += AI_PADDLE_SPEED  # Move right if ball is to the right

    # Adding a bit of a delay in reaction by only moving toward the ball sometimes
    if random.random() < 0.2:  # 20% of the time, the AI won't react
        if ball.centerx < computer_paddle.centerx:
            computer_paddle.x -= AI_PADDLE_SPEED  # Move left
        elif ball.centerx > computer_paddle.centerx:
            computer_paddle.x += AI_PADDLE_SPEED  # Move right

    # Ensure the computer paddle doesn't go out of bounds
    if computer_paddle.left <= (SCREEN_WIDTH - 800) // 2:
        computer_paddle.left = (SCREEN_WIDTH - 800) // 2
    if computer_paddle.right >= (SCREEN_WIDTH + 800) // 2:
        computer_paddle.right = (SCREEN_WIDTH + 800) // 2

    # Ball movement
    ball.x += ball_dx
    ball.y += ball_dy

    # Ball collision with left/right walls
    if ball.left <= (SCREEN_WIDTH - 800) // 2 or ball.right >= (SCREEN_WIDTH + 800) // 2:
        ball_dx = -ball_dx

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(computer_paddle):
        ball_dy = -ball_dy

    # Ball goes out of bounds (score)
    if ball.top <= 0:  # AI missed, player scores
        player_score += 1
        reset_ball()

    if ball.bottom >= SCREEN_HEIGHT - 100:  # Player missed, AI scores
        computer_score += 1
        reset_ball()

    # Check if the player is winning by 2 points
    if player_score - computer_score >= 2:
        display_win_message()
        break

    # Drawing everything
    screen.fill(BLACK)  # Clear the screen with black
    
    # Draw static stars covering the playable area
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 2)

    # Define the border rectangle
    border_rect = pygame.Rect((SCREEN_WIDTH - 800) // 2, 120, 800, SCREEN_HEIGHT - 220)  # Adjust height to fit paddles

    # Draw the border rectangle
    pygame.draw.rect(screen, WHITE, border_rect, 5)  # 5 is the width of the border

    pygame.draw.rect(screen, WHITE, player_paddle)  # Player paddle
    pygame.draw.rect(screen, WHITE, computer_paddle)  # Computer paddle
    if ball.x >= 0 and ball.x <= SCREEN_WIDTH:  # Draw the ball only if it's on screen
        pygame.draw.ellipse(screen, WHITE, ball)  # Ball

    # Draw the limited middle line
    pygame.draw.aaline(screen, WHITE, 
                       ((SCREEN_WIDTH - 800) // 2, SCREEN_HEIGHT // 2), 
                       ((SCREEN_WIDTH + 800) // 2, SCREEN_HEIGHT // 2))  # Middle line

    # Draw the scores with custom labels
    player_text = font.render("YOUR SCORE", True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH // 4 - 100, 20))

    player_score_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_score_text, (SCREEN_WIDTH // 4, 60))  # Adjust y-position

    computer_text = font.render("ALIEN SCORE", True, WHITE)
    screen.blit(computer_text, (SCREEN_WIDTH * 3 // 4 - 100, 20))

    computer_score_text = font.render(str(computer_score), True, WHITE)
    screen.blit(computer_score_text, (SCREEN_WIDTH * 3 // 4, 60))  # Adjust y-position

    # Update the screen
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
