import pygame
import random

# MemoryGame.py

# Rest of your code
class MemoryGame:
    def __init__(self, screen, rows=3, cols=4):
        self.screen = screen
        self.rows = rows
        self.cols = cols
        self.cards = []
        self.flipped_cards = []
        self.matched_cards = []
        self.card_width = 100
        self.card_height = 100

        # Add cursor to track the currently selected card
        self.cursor_row = 0
        self.cursor_col = 0

        self.margin_x = 20  # Horizontal space between cards
        self.margin_y = 20

        self.setup_game()
        

    def setup_game(self):
        # Calculate the total width and height of the card grid including the margins
        total_width = self.cols * (self.card_width + self.margin_x) - self.margin_x
        total_height = self.rows * (self.card_height + self.margin_y) - self.margin_y

        # Calculate the top-left position to start drawing cards to center them
        screen_width, screen_height = self.screen.get_size()
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2

        # Initialize cards (pairs of images or numbers)
        card_values = list(range(self.rows * self.cols // 2)) * 2
        random.shuffle(card_values)

        # Create card objects and arrange them in a grid with spacing
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                card_value = card_values.pop()
                card_x = start_x + j * (self.card_width + self.margin_x)  # Add margin to the x position
                card_y = start_y + i * (self.card_height + self.margin_y)  # Add margin to the y position
                row.append(Card(card_value, card_x, card_y, self.card_width, self.card_height))  # Pass the calculated position
            self.cards.append(row)  

    def draw(self):
        # Calculate the bounding box of the card grid
        total_width = self.cols * (self.card_width + self.margin_x) - self.margin_x
        total_height = self.rows * (self.card_height + self.margin_y) - self.margin_y

        # Calculate the top-left position of the grid
        screen_width, screen_height = self.screen.get_size()
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2

        # Draw the white box (border) around the grid with padding
        padding = 50  # Padding between the cards and the box
        box_rect = pygame.Rect(start_x - padding, start_y - padding, total_width + 2 * padding, total_height + 2 * padding)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, 5)  # White thick border with a thickness of 10

        # Draw the cards inside the grid
        for row in self.cards:
            for card in row:
                card.draw(self.screen)

        # Highlight the selected card with a border
        selected_card = self.cards[self.cursor_row][self.cursor_col]
        pygame.draw.rect(self.screen, (255, 255, 255), selected_card.rect, 5)  # White border for the selected card


    def move_cursor(self, direction):
        # Move the cursor based on the arrow keys
        if direction == 'UP' and self.cursor_row > 0:
            self.cursor_row -= 1
        elif direction == 'DOWN' and self.cursor_row < self.rows - 1:
            self.cursor_row += 1
        elif direction == 'LEFT' and self.cursor_col > 0:
            self.cursor_col -= 1
        elif direction == 'RIGHT' and self.cursor_col < self.cols - 1:
            self.cursor_col += 1

    def handle_key_press(self, key):
        # Handle key presses for navigation and flipping
        if key == pygame.K_UP:
            self.move_cursor('UP')
        elif key == pygame.K_DOWN:
            self.move_cursor('DOWN')
        elif key == pygame.K_LEFT:
            self.move_cursor('LEFT')
        elif key == pygame.K_RIGHT:
            self.move_cursor('RIGHT')
        elif key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.flip_selected_card()

    def flip_selected_card(self):
        # Flip the currently selected card
        selected_card = self.cards[self.cursor_row][self.cursor_col]
        if not selected_card.matched and not selected_card.flipped:
            selected_card.flip()
            self.flipped_cards.append(selected_card)

        # After flipping two cards, check for a match
        if len(self.flipped_cards) == 2:
            self.check_match()

    def check_match(self):
        card1, card2 = self.flipped_cards
        if card1.value == card2.value:
            card1.matched = True
            card2.matched = True
            self.matched_cards.extend([card1, card2])
        else:
            # Flip back if not a match
            pygame.time.delay(0)  # Optional delay
            card1.flip()
            card2.flip()

        self.flipped_cards = []

    def is_game_over(self):
        return len(self.matched_cards) == self.rows * self.cols
import pygame

class Card:
    def __init__(self, value, x, y, width, height):
        self.value = value
        self.flipped = False
        self.matched = False
        
        # Load the corresponding image based on the card value
        # Ensure the image extension matches the actual image type (webp or jpg)
        self.image = pygame.image.load(r'MemoryGame/assets/{}.jpg'.format(value+1))  # Using .jpg format
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale to card size
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        if self.flipped or self.matched:
            # Draw the card face (the image)
            screen.blit(self.image, self.rect.topleft)  # Draw the image
        else:
            # Draw the card back
            pygame.draw.rect(screen, (29, 27, 64), self.rect)  # Draw a blue rectangle for the back

    def is_clicked(self, pos):
        # Check if the card's rectangle was clicked
        return self.rect.collidepoint(pos)

    def flip(self):
        self.flipped = not self.flipped


class MemoryGameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.memory_game = MemoryGame(screen)
        self.font_path = r"MemoryGame/assets/BigBlue_Terminal_v1.0/BigBlue_Terminal_437TT.TTF"
        self.font = pygame.font.Font(self.font_path, 40)
        self.text1 = self.font.render("Congratulations !!", True, (255, 255, 255))
        self.text2 = self.font.render("You are now sane :)", True, (255, 255, 255))
        self.text3 = self.font.render("Your mental health is now optimum !!", True, (255, 255, 255))
        self.game_over = False

    def memory_game_logic(self):
        while True:
            screen_width, screen_height = 1280, 720
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN and not self.game_over:
                    self.memory_game.handle_key_press(event.key)

            self.screen.fill((0, 0, 0))

            if not self.memory_game.is_game_over():
                self.memory_game.draw()
            else:
                text_rect = self.text1.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
                self.screen.blit(self.text1, text_rect)
                text_rect = self.text2.get_rect(center=(screen_width // 2, screen_height // 2))
                self.screen.blit(self.text2, text_rect)
                text_rect = self.text3.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
                self.screen.blit(self.text3, text_rect)
                pygame.display.flip()  # Update the display to show the "You Win!" message
                pygame.time.delay(2000)  # Delay 2 seconds
                return "mc_room"

            pygame.display.flip()
'''
# Initialize Pygame
pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory Game")

# Create an instance of MemoryGameScreen
memory_game_screen = MemoryGameScreen(screen)

# Main game loop
running = True
while running:
    running = memory_game_screen.memory_game_logic()

pygame.quit()'''
