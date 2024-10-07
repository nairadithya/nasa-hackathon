import pygame

class FinalScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.font_path = "BigBlue_Terminal_437TT.TTF"  # Replace with the actual path to your .ttf font file
        self.font = pygame.font.Font(self.font_path, 60)
        self.small_font = pygame.font.Font(self.font_path, 30)

    def show(self):
        while self.running:
            self.screen.fill((0, 0, 0))  # Fill the screen with black

            # Render the congratulations message
            congrats_text = self.font.render("Congratulations!", True, (255, 255, 255))
            self.screen.blit(congrats_text, (self.screen.get_width() // 2 - congrats_text.get_width() // 2, self.screen.get_height() // 2 - 100))

            # Render the additional message
            additional_text = self.small_font.render("You have successfully completed the game.", True, (255, 255, 255))
            self.screen.blit(additional_text, (self.screen.get_width() // 2 - additional_text.get_width() // 2, self.screen.get_height() // 2))

            # Render the exit instruction
            exit_text = self.small_font.render("Press any key to exit.", True, (255, 255, 255))
            self.screen.blit(exit_text, (self.screen.get_width() // 2 - exit_text.get_width() // 2, self.screen.get_height() // 2 + 100))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.running = False

        pygame.quit()
        return "final"
