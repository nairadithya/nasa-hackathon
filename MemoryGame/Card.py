import pygame

class Card:
    def __init__(self, value, x, y, width, height):
        self.value = value
        self.flipped = False
        self.matched = False
        
        # Load the corresponding image based on the card value
        # Ensure the image extension matches the actual image type (webp or jpg)
        self.image = pygame.image.load(r'MemoryGame\assets\{}.jpg'.format(value+1))  # Using .jpg format
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
