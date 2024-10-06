import pygame
from MCroom import MCroom as m
from MemoryGame import MainGame as m1

class GameState:
    MC_ROOM = "mc_room"
    STATION1_SCENE = "station1_scene"
    GAME1 = "game1"
    STATION2_SCENE = "station2_scene"
    GAME2 = "game2"
    STATION3_SCENE = "station3_scene"
    GAME3 = "game3"

# Initialize Pygame
pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PowerPuff")

# Create an instance of MCroom
mc = m.MCroom()
intro = m.IntroScreen(screen)


running = intro.show_intro()

current_screen = "mc_room"
while running:
    if current_screen == "mc_room":
        result = mc.mc_room_logic(screen)
        if result == "memory_game":
            current_screen = "memory_game"
        else:
            running = result
    elif current_screen == "memory_game":
        memory_game_screen = m1.MemoryGameScreen(screen)
        running = memory_game_screen.memory_game_logic()
        #delay 5 seconds
        current_screen = "mc_room"
    pygame.display.flip()

pygame.quit() 