import pygame
import random

class ConnectTheWiresGame:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.game_completed = False
        self.dragging_wire = False
        self.start_terminal = None
        self.wire_color = None
        self.correct_wires = 0
        self.wire_connections = []

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 1280, 720

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (100, 100, 100)
        self.COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]  # Red, Green, Blue, Yellow, Orange

        # Load custom font
        self.font_path = "BigBlue_Terminal_437TT.ttf"  # Replace with the actual path to your .ttf font file

        # Fonts
        self.header_font = pygame.font.Font(self.font_path, 48)  # Custom font for header
        self.success_font = pygame.font.Font(self.font_path, 36)  # Custom font for success message

        # Fuse box dimensions
        self.FUSE_BOX_WIDTH, self.FUSE_BOX_HEIGHT = 600, 500
        self.FUSE_BOX_X = (self.WIDTH - self.FUSE_BOX_WIDTH) // 2  # Centering the fuse box horizontally
        self.FUSE_BOX_Y = (self.HEIGHT - self.FUSE_BOX_HEIGHT) // 2  # Centering the fuse box vertically

        # Terminal dimensions and spacing
        self.TERMINAL_WIDTH, self.TERMINAL_HEIGHT = 40, 40
        self.TERMINAL_SPACING = 80

        # Calculate vertical offset to center the terminals within the fuse box
        total_terminal_height = (len(self.COLORS) - 1) * self.TERMINAL_SPACING + self.TERMINAL_HEIGHT
        self.vertical_offset = (self.FUSE_BOX_HEIGHT - total_terminal_height) // 2

        # Terminals (rectangles for wires)
        self.left_terminals = []
        self.right_terminals = []

        # Generate terminal positions
        for i in range(len(self.COLORS)):
            self.left_terminals.append(pygame.Rect(self.FUSE_BOX_X + 50, self.FUSE_BOX_Y + self.vertical_offset + i * self.TERMINAL_SPACING, self.TERMINAL_WIDTH, self.TERMINAL_HEIGHT))
            self.right_terminals.append(pygame.Rect(self.FUSE_BOX_X + self.FUSE_BOX_WIDTH - 90, self.FUSE_BOX_Y + self.vertical_offset + i * self.TERMINAL_SPACING, self.TERMINAL_WIDTH, self.TERMINAL_HEIGHT))

        # Shuffle right terminals to randomize matching
        random.shuffle(self.right_terminals)

    def run_game(self):
        while self.running:
            self.screen.fill(self.BLACK)
            
            # Draw header
            header_text = self.header_font.render("Power Room", True, self.WHITE)
            self.screen.blit(header_text, (self.WIDTH // 2 - header_text.get_width() // 2, 20))
            
            # Draw fuse box
            fuse_box = pygame.Rect(self.FUSE_BOX_X, self.FUSE_BOX_Y, self.FUSE_BOX_WIDTH, self.FUSE_BOX_HEIGHT)
            pygame.draw.rect(self.screen, self.GRAY, fuse_box)
            pygame.draw.rect(self.screen, self.WHITE, fuse_box, 2)  # White border
            
            # Draw the terminals
            for i, rect in enumerate(self.left_terminals):
                pygame.draw.rect(self.screen, self.COLORS[i], rect)
                
            for i, rect in enumerate(self.right_terminals):
                pygame.draw.rect(self.screen, self.COLORS[i], rect)
                
            # Draw wires
            for wire in self.wire_connections:
                pygame.draw.line(self.screen, wire[2], wire[0].center, wire[1].center, 5)

            # Draw dragging wire
            if self.dragging_wire:
                mouse_pos = pygame.mouse.get_pos()
                pygame.draw.line(self.screen, self.wire_color, self.start_terminal.center, mouse_pos, 5)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                
                # Handle mouse events
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_completed:
                    # Check if we clicked on a left terminal
                    for i, rect in enumerate(self.left_terminals):
                        if rect.collidepoint(event.pos):
                            self.dragging_wire = True
                            self.start_terminal = rect
                            self.wire_color = self.COLORS[i]
                            break
                
                if event.type == pygame.MOUSEBUTTONUP and not self.game_completed:
                    if self.dragging_wire:
                        # Check if we released over a right terminal
                        for i, rect in enumerate(self.right_terminals):
                            if rect.collidepoint(event.pos) and self.COLORS[self.left_terminals.index(self.start_terminal)] == self.COLORS[self.right_terminals.index(rect)]:
                                self.wire_connections.append((self.start_terminal, rect, self.wire_color))
                                self.correct_wires += 1
                                break
                        
                        self.dragging_wire = False

            # Check if all wires are connected correctly
            if self.correct_wires == len(self.COLORS) and not self.game_completed:
                self.game_completed = True
                break  
            pygame.display.flip()

        self.screen.fill(self.BLACK)
        success_text1 = self.success_font.render("Task Completed Successfully", True, self.WHITE)
        success_text2 = self.success_font.render("Your electricity supply has been restored.", True, self.WHITE)
        self.screen.blit(success_text1, (self.WIDTH // 2 - success_text1.get_width() // 2, self.HEIGHT // 2 - 50))
        self.screen.blit(success_text2, (self.WIDTH // 2 - success_text2.get_width() // 2, self.HEIGHT // 2 + 50))
        pygame.display.flip()
        pygame.time.delay(2000)
        return "mc_room"