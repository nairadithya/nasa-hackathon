import pygame
from MCroom import MCroom as m
from MemoryGame import MainGame as m1
import pong as p
import random

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
font_path = r"MemoryGame\assets\BigBlue_Terminal_v1.0\BigBlue_Terminal_437TT.TTF"
font = pygame.font.Font(font_path,30)

running = intro.show_intro()
interested = [0,0,0,0]
current_screen = "mc_room"
while running:
    if current_screen == "mc_room":
        result = mc.mc_room_logic(screen, interested)
        if result == "memory_game":
            current_screen = "memory_game"
        elif result == "pong_game":
            current_screen = "pong_game"
        else:
            running = result
    elif current_screen == "memory_game":
        memory_game_screen = m1.MemoryGameScreen(screen)
        running = memory_game_screen.memory_game_logic()
        current_screen = "mc_room"
        interested[0] = 1
    elif current_screen == "pong_game":
        pong_game = p.Pong(screen)
        result = pong_game.pong_game_logic()
        interested[1] = 1
        if result == "mc_room":
            current_screen = "mc_room"
        
    pygame.display.flip()

pygame.quit()