import pygame
from MCroom import MCroom as m
from MemoryGame import MainGame as m1
import pong as p
import electrical as e
import shootasteroids as s
import FinalScreen as fs
import AsteroidScreen as a


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
interested = [1,1,1,1]
current_screen = "mc_room"
while running:
    if current_screen == "mc_room":
        result = mc.mc_room_logic(screen, interested)
        if result == "memory_game":
            current_screen = "memory_game"
        elif result == "pong_game":
            current_screen = "pong_game"
        elif result == "connect_wires_games":
            current_screen = "connect_wires_games"
        else:
            running = result
    elif current_screen == "memory_game":
        memory_game_screen = m1.MemoryGameScreen(screen)
        running = memory_game_screen.memory_game_logic()
        current_screen = "mc_room"
        interested[0] = 1
    elif current_screen == "pong_game":
        electrical = e.ConnectTheWiresGame(screen)
        result = electrical.run_game()
        interested[1] = 1
        if result == "mc_room":
            current_screen = "mc_room"
    elif current_screen == "connect_wires_games":
        pong_game = p.Pong(screen)
        result = pong_game.pong_game_logic()
        interested[2] = 1
        if result == "mc_room":
            current_screen = "mc_room"

    elif current_screen == "asteroid_intro":
        asteroid_intro = a.AsteroidIntroScreen(screen)
        
        result = asteroid_intro.show_intro()
        print(result)
        if result == "start_asteroid_game":
            print("yo wsg")
            current_screen = "start_asteroid_game"

    if current_screen == "start_asteroid_game":
        print("hi")
        result = s.shoot_asteroids_game(screen)
        if result == "final":
            final_screen = fs.FinalScreen(screen)
            result = final_screen.show()

    if interested[0] == 1 and interested[1] == 1 and interested[2] == 1:
        current_screen = "asteroid_intro"
    pygame.display.flip()

# Initialize Pygam
pygame.quit()