import pygame
class AsteroidIntroScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.font_path = "BigBlue_Terminal_437TT.TTF"  # Replace with the actual path to your .ttf font file
        self.font = pygame.font.Font(self.font_path, 40)
        self.small_font = pygame.font.Font(self.font_path, 25)

    def show_intro(self):
        while self.running:
            self.screen.fill((0, 0, 0))  # Fill the screen with black

            # Render the introductory message
            intro_text1 = self.small_font.render("UH OH, your ship is barreling into an asteroid belt!!", True, (255, 255, 255))
            intro_text2 = self.small_font.render("Get into the artillery room and shoot down all the asteroids in your way,", True, (255, 255, 255))
            intro_text3 = self.small_font.render("survive for 30 seconds and you might be able to survive.", True, (255, 255, 255))
            intro_text4 = self.small_font.render("Use the left, right and space key, all the best !!", True, (255, 255, 255))
            self.screen.blit(intro_text1, (self.screen.get_width() // 2 - intro_text1.get_width() // 2, self.screen.get_height() // 2 - 100))
            self.screen.blit(intro_text2, (self.screen.get_width() // 2 - intro_text2.get_width() // 2, self.screen.get_height() // 2 - 50))
            self.screen.blit(intro_text3, (self.screen.get_width() // 2 - intro_text3.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(intro_text4, (self.screen.get_width() // 2 - intro_text4.get_width() // 2, self.screen.get_height() // 2 + 50))

            # Render the start instruction

            pygame.display.flip()

            pygame.time.delay(5000)
            return "start_asteroid_game"
