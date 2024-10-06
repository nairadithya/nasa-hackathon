import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect the Wires")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]  # Red, Green, Blue, Yellow, Orange

# Load custom font
font_path = "BigBlue_Terminal_437TT.ttf"  # Replace with the actual path to your .ttf font file

# Fonts
header_font = pygame.font.Font(font_path, 48)  # Custom font for header
success_font = pygame.font.Font(font_path, 36)  # Custom font for success message

# Fuse box dimensions
FUSE_BOX_WIDTH, FUSE_BOX_HEIGHT = 600, 500
FUSE_BOX_X = (WIDTH - FUSE_BOX_WIDTH) // 2  # Centering the fuse box horizontally
FUSE_BOX_Y = (HEIGHT - FUSE_BOX_HEIGHT) // 2  # Centering the fuse box vertically

# Terminal dimensions and spacing
TERMINAL_WIDTH, TERMINAL_HEIGHT = 40, 40
TERMINAL_SPACING = 80

# Calculate vertical offset to center the terminals within the fuse box
total_terminal_height = (len(COLORS) - 1) * TERMINAL_SPACING + TERMINAL_HEIGHT
vertical_offset = (FUSE_BOX_HEIGHT - total_terminal_height) // 2

# Terminals (rectangles for wires)
left_terminals = []
right_terminals = []
wire_connections = []  # Stores the (start, end) pairs
correct_wires = 0

# Generate terminal positions
for i in range(len(COLORS)):
    left_terminals.append(pygame.Rect(FUSE_BOX_X + 50, FUSE_BOX_Y + vertical_offset + i * TERMINAL_SPACING, TERMINAL_WIDTH, TERMINAL_HEIGHT))
    right_terminals.append(pygame.Rect(FUSE_BOX_X + FUSE_BOX_WIDTH - 90, FUSE_BOX_Y + vertical_offset + i * TERMINAL_SPACING, TERMINAL_WIDTH, TERMINAL_HEIGHT))

# Shuffle right terminals to randomize matching
random.shuffle(right_terminals)

# Game variables
dragging_wire = False
start_terminal = None
wire_color = None
game_completed = False

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Draw header
    header_text = header_font.render("Oxygen Centre Power Room", True, WHITE)
    screen.blit(header_text, (WIDTH // 2 - header_text.get_width() // 2, 20))
    
    # Draw fuse box
    fuse_box = pygame.Rect(FUSE_BOX_X, FUSE_BOX_Y, FUSE_BOX_WIDTH, FUSE_BOX_HEIGHT)
    pygame.draw.rect(screen, GRAY, fuse_box)
    pygame.draw.rect(screen, WHITE, fuse_box, 2)  # White border
    
    # Draw the terminals
    for i, rect in enumerate(left_terminals):
        pygame.draw.rect(screen, COLORS[i], rect)
        
    for i, rect in enumerate(right_terminals):
        pygame.draw.rect(screen, COLORS[i], rect)
        
    # Draw wires
    for wire in wire_connections:
        pygame.draw.line(screen, wire[2], wire[0].center, wire[1].center, 5)

    # Draw dragging wire
    if dragging_wire:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, wire_color, start_terminal.center, mouse_pos, 5)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN and not game_completed:
            # Check if we clicked on a left terminal
            for i, rect in enumerate(left_terminals):
                if rect.collidepoint(event.pos):
                    dragging_wire = True
                    start_terminal = rect
                    wire_color = COLORS[i]
                    break
        
        if event.type == pygame.MOUSEBUTTONUP and not game_completed:
            if dragging_wire:
                # Check if we released over a right terminal
                for i, rect in enumerate(right_terminals):
                    if rect.collidepoint(event.pos) and COLORS[left_terminals.index(start_terminal)] == COLORS[right_terminals.index(rect)]:
                        wire_connections.append((start_terminal, rect, wire_color))
                        correct_wires += 1
                        break
                
                dragging_wire = False

    # Check if all wires are connected correctly
    if correct_wires == len(COLORS) and not game_completed:
        game_completed = True
    
    if game_completed:
        screen.fill(BLACK)
        success_text1 = success_font.render("Task Completed Successfully", True, WHITE)
        success_text2 = success_font.render("Your Oxygen supply has been restored.", True, WHITE)
        screen.blit(success_text1, (WIDTH // 2 - success_text1.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(success_text2, (WIDTH // 2 - success_text2.get_width() // 2, HEIGHT // 2 + 50))
    
    pygame.display.flip()

# Quit pygame
pygame.quit()
