import random
import pygame
class Pong:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.player_score = 0
        self.computer_score = 0
        self.font_path = "BigBlue_Terminal_437TT.ttf"  # Adjust this path as needed
        self.font = pygame.font.Font(self.font_path, 40)  # Change the size from 74 to 40
        self.setup_game()

    def setup_game(self):
        # Screen dimensions (1280x720 resolution)
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720

        # Colors (RGB)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Paddle settings
        self.PADDLE_WIDTH = 80  # Paddle width
        self.PADDLE_HEIGHT = 15  # Increased paddle height for thickness
        self.PADDLE_SPEED = 6  # Player paddle speed
        self.AI_PADDLE_SPEED = 3  # Slower AI paddle speed for "dumb" AI

        # Ball settings (Smaller ball)
        self.BALL_SIZE = 15  # Smaller ball size
        self.BALL_SPEED_X = 4  # Slower horizontal speed
        self.BALL_SPEED_Y = 4  # Slower vertical speed

        # Clock for controlling the frame rate
        self.clock = pygame.time.Clock()

        # Paddles (position them closer together)
        self.player_paddle = pygame.Rect(self.SCREEN_WIDTH // 2 - 70, self.SCREEN_HEIGHT - 120, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.computer_paddle = pygame.Rect(self.SCREEN_WIDTH // 2 - 70, 120, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)

        # Ball
        self.ball = pygame.Rect(self.SCREEN_WIDTH // 2 - self.BALL_SIZE // 2, self.SCREEN_HEIGHT // 2 - self.BALL_SIZE // 2, self.BALL_SIZE, self.BALL_SIZE)
        self.ball_dx = self.BALL_SPEED_X * random.choice((1, -1))
        self.ball_dy = self.BALL_SPEED_Y * random.choice((1, -1))

        # Create static stars for the background limited to the playable area
        self.stars = []
        for _ in range(200):  # Increased the number of stars
            star_x = random.randint((self.SCREEN_WIDTH - 800) // 2, (self.SCREEN_WIDTH + 800) // 2)  # Stars only in playable width
            star_y = random.randint(130, self.SCREEN_HEIGHT - 100)  # Ensure stars start below the computer paddle (y = 130)
            self.stars.append((star_x, star_y))

    def reset_ball(self):
        self.ball.x = self.SCREEN_WIDTH // 2 - self.BALL_SIZE // 2
        self.ball.y = self.SCREEN_HEIGHT // 2 - self.BALL_SIZE // 2
        self.ball_dx *= random.choice((1, -1))
        self.ball_dy *= random.choice((1, -1))

    def display_win_message(self):
        win_message = "YOU WIN YAY !!! but alien is sad :((("
        win_text = self.font.render(win_message, True, self.WHITE)
        self.screen.fill(self.BLACK)  # Clear the screen
        self.screen.blit(win_text, (self.SCREEN_WIDTH // 8, self.SCREEN_HEIGHT // 2 - 40))  # Center message
        pygame.display.flip()  # Update the screen
        pygame.time.delay(5000)  # Display for 5 seconds

    def pong_game_logic(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Get keys pressed
            keys = pygame.key.get_pressed()

            # Player movement (Left/Right arrow keys)
            if keys[pygame.K_LEFT] and self.player_paddle.left > (self.SCREEN_WIDTH - 800) // 2:
                self.player_paddle.x -= self.PADDLE_SPEED
            if keys[pygame.K_RIGHT] and self.player_paddle.right < (self.SCREEN_WIDTH + 800) // 2:
                self.player_paddle.x += self.PADDLE_SPEED

            # AI Paddle Movement: Make the AI "dumb"
            if self.ball.centerx < self.computer_paddle.centerx:
                self.computer_paddle.x -= self.AI_PADDLE_SPEED  # Move left if ball is to the left
            elif self.ball.centerx > self.computer_paddle.centerx:
                self.computer_paddle.x += self.AI_PADDLE_SPEED  # Move right if ball is to the right

            # Adding a bit of a delay in reaction by only moving toward the ball sometimes
            if random.random() < 0.2:  # 20% of the time, the AI won't react
                if self.ball.centerx < self.computer_paddle.centerx:
                    self.computer_paddle.x -= self.AI_PADDLE_SPEED  # Move left
                elif self.ball.centerx > self.computer_paddle.centerx:
                    self.computer_paddle.x += self.AI_PADDLE_SPEED  # Move right

            # Ensure the computer paddle doesn't go out of bounds
            if self.computer_paddle.left <= (self.SCREEN_WIDTH - 800) // 2:
                self.computer_paddle.left = (self.SCREEN_WIDTH - 800) // 2
            if self.computer_paddle.right >= (self.SCREEN_WIDTH + 800) // 2:
                self.computer_paddle.right = (self.SCREEN_WIDTH + 800) // 2

            # Ball movement
            self.ball.x += self.ball_dx
            self.ball.y += self.ball_dy

            # Ball collision with left/right walls
            if self.ball.left <= (self.SCREEN_WIDTH - 800) // 2 or self.ball.right >= (self.SCREEN_WIDTH + 800) // 2:
                self.ball_dx = -self.ball_dx

            # Ball collision with paddles
            if self.ball.colliderect(self.player_paddle) or self.ball.colliderect(self.computer_paddle):
                self.ball_dy = -self.ball_dy

            # Ball goes out of bounds (score)
            if self.ball.top <= 0:  # AI missed, player scores
                self.player_score += 1
                self.reset_ball()

            if self.ball.bottom >= self.SCREEN_HEIGHT - 100:  # Player missed, AI scores
                self.computer_score += 1
                self.reset_ball()

            # Check if the player is winning by 2 points
            if self.player_score - self.computer_score >= 2:
                self.display_win_message()
                return "mc_room"

            # Drawing everything
            self.screen.fill(self.BLACK)  # Clear the screen with black
            
            # Draw static stars covering the playable area
            for star in self.stars:
                pygame.draw.circle(self.screen, self.WHITE, star, 2)

            # Define the border rectangle
            border_rect = pygame.Rect((self.SCREEN_WIDTH - 800) // 2, 120, 800, self.SCREEN_HEIGHT - 220)  # Adjust height to fit paddles

            # Draw the border rectangle
            pygame.draw.rect(self.screen, self.WHITE, border_rect, 5)  # 5 is the width of the border

            pygame.draw.rect(self.screen, self.WHITE, self.player_paddle)  # Player paddle
            pygame.draw.rect(self.screen, self.WHITE, self.computer_paddle)  # Computer paddle
            if self.ball.x >= 0 and self.ball.x <= self.SCREEN_WIDTH:  # Draw the ball only if it's on screen
                pygame.draw.ellipse(self.screen, self.WHITE, self.ball)  # Ball

            # Draw the limited middle line
            pygame.draw.aaline(self.screen, self.WHITE, 
                            ((self.SCREEN_WIDTH - 800) // 2, self.SCREEN_HEIGHT // 2), 
                            ((self.SCREEN_WIDTH + 800) // 2, self.SCREEN_HEIGHT // 2))  # Middle line

            # Draw the scores with custom labels
            player_text = self.font.render("YOUR SCORE", True, self.WHITE)
            self.screen.blit(player_text, (self.SCREEN_WIDTH // 4 - 100, 20))

            player_score_text = self.font.render(str(self.player_score), True, self.WHITE)
            self.screen.blit(player_score_text, (self.SCREEN_WIDTH // 4, 60))  # Adjust y-position

            computer_text = self.font.render("ALIEN SCORE", True, self.WHITE)
            self.screen.blit(computer_text, (self.SCREEN_WIDTH * 3 // 4 - 100, 20))

            computer_score_text = self.font.render(str(self.computer_score), True, self.WHITE)
            self.screen.blit(computer_score_text, (self.SCREEN_WIDTH * 3 // 4, 60))  # Adjust y-position

            # Update the screen
            pygame.display.flip()

            # Frame rate
            self.clock.tick(60)

        pygame.quit()
        return "mc_room"
