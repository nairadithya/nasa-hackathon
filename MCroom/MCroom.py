import pygame

class IntroScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_path = r"MemoryGame\assets\BigBlue_Terminal_v1.0\BigBlue_Terminal_437TT.TTF"
        self.font = pygame.font.Font(self.font_path,30)
        self.text1 = '''Hello, you are an astronaut.'''
        self.text2 = '''You are on a mission to save the world.'''
        self.text3 = '''The spaceship has landed on Mars.'''
        self.text4 = '''You need to manage your resources and '''
        self.text5 = '''complete tasks to return to Earth.'''
        self.text6 = '''Press SPACE to continue...'''

        self.text_surface1 = self.font.render(self.text1, True, (255, 255, 255))
        self.text_surface2 = self.font.render(self.text2, True, (255, 255, 255))
        self.text_surface3 = self.font.render(self.text3, True, (255, 255, 255))
        self.text_surface4 = self.font.render(self.text4, True, (255, 255, 255))
        self.text_surface5 = self.font.render(self.text5, True, (255, 255, 255))
        self.text_surface6 = self.font.render(self.text6, True, (255, 255, 255))

    def show_intro(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        self.screen.blit(self.text_surface1, (50, 100))  # Display text
        self.screen.blit(self.text_surface2, (50, 200))  # Display text
        self.screen.blit(self.text_surface3, (50, 300))  # Display text
        self.screen.blit(self.text_surface4, (50, 400))  # Display text
        self.screen.blit(self.text_surface5, (50, 500))  # Display text
        self.screen.blit(self.text_surface6, (50, 600))  # Display text

        pygame.display.flip()  # Update display

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
        return True

class MCroom:
    def __init__(self):
        self.mc_image = pygame.image.load("MCroom/mc.png")
        self.mc_rect = self.mc_image.get_rect(topleft=(100, 300))  
        self.font_path = r"MemoryGame\assets\BigBlue_Terminal_v1.0\BigBlue_Terminal_437TT.TTF"
        self.font = pygame.font.Font(self.font_path,30)

    def mc_room_logic(self, screen, interesed):
        mc_image = self.mc_image
        mc_rect = self.mc_rect
        approaching_door = None

        door_width = 200
        door_height = 100
        door1_rect = pygame.Rect(150, 50, door_width, door_height)
        door2_rect = pygame.Rect(540, 50, door_width, door_height)
        door3_rect = pygame.Rect(930, 50, door_width, door_height)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if mc_rect.x > 50:
                mc_rect.x -= 1
        if keys[pygame.K_RIGHT]:
            if mc_rect.x < 1170:
                mc_rect.x += 1
        if keys[pygame.K_UP]:
            if mc_rect.y > 50:
                mc_rect.y -= 1
        if keys[pygame.K_DOWN]:
            if mc_rect.y < 580:
                mc_rect.y += 1

        if mc_rect.colliderect(door1_rect):
            if interesed[0] == 0:
                approaching_door = "door1"
        elif mc_rect.colliderect(door2_rect):
            if interesed[1] == 0:
                approaching_door = "door2"
        elif mc_rect.colliderect(door3_rect):
            if interesed[2] == 0:
                approaching_door = "door3"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and approaching_door:
                    if approaching_door == "door1":
                        return "memory_game"
                    if approaching_door == "door2":
                        return "pong_game"
                    print(f"Interacting with {approaching_door}")  # You can replace this with state change

        screen.fill((0, 0, 0))  
        pygame.draw.rect(screen, (255, 255, 255), (50, 50, 1180, 620), 5)  # Room border

        # Draw doors
        pygame.draw.rect(screen, (255, 255, 255), door1_rect)  # Door 1
        pygame.draw.rect(screen, (255, 255, 255), door2_rect)  # Door 2
        pygame.draw.rect(screen, (255, 255, 255), door3_rect)  # Door 3

        #show three stats: sanity, electricity and food
        if interesed[0] == 1:
            text_surface1 = self.font.render("Sanity: 100%", True, (255, 255, 255))
            screen.blit(text_surface1, (150, 10))
        else:
            text_surface1 = self.font.render("Sanity: 0%", True, (255, 255, 255))
            screen.blit(text_surface1, (150, 10))
        if interesed[1] == 1:
            text_surface2 = self.font.render("Electricity: 100%", True, (255, 255, 255))
            screen.blit(text_surface2, (500, 10))
        else:
            text_surface2 = self.font.render("Electricity: 0%", True, (255, 255, 255))
            screen.blit(text_surface2, (500, 10))

        if interesed[2] == 1:
            text_surface3 = self.font.render("Food: 100%", True, (255, 255, 255))
            screen.blit(text_surface3, (950, 10))
        else:
            text_surface3 = self.font.render("Food: 0%", True, (255, 255, 255))
            screen.blit(text_surface3, (950, 10))

        # Draw player character
        screen.blit(mc_image, mc_rect.topleft)

        # Display approaching door text
        if approaching_door:
            text_surface = self.font.render(f"Press SPACE to enter {approaching_door}", True, (255, 255, 255))
            screen.blit(text_surface, (50, 680))

        return True