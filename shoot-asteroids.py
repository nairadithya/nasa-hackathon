import pygame
import math
import random
import os

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Game states
PLAYING, WIN, LOSE = 0, 1, 2
game_state = PLAYING

# Time delta (for frame-independent movement)
dt = 0

# Screen Settings
game_frame_width, game_frame_height = 700, 550
game_frame = pygame.Surface((game_frame_width, game_frame_height))
game_frame_rect = game_frame.get_rect(center=screen.get_rect().center)

# Load sprite images
def load_image(name):
    path = os.path.join('assets', name)
    try:
        image = pygame.image.load(path).convert_alpha()
        print(f"Successfully loaded {name}")
        return image
    except pygame.error as e:
        print(f"Error loading image {name}: {e}")
        return pygame.Surface((50, 50), pygame.SRCALPHA)  # Fallback surface

turret_base_sprite = load_image('turret_base.png')
turret_gun_sprite = load_image('turret_gun.png')
asteroid_sprite = load_image('asteroid.png')

# Turret settings
TURRET_RADIUS = 40
TURRET_LENGTH = 50

class Turret:
    def __init__(self, pos):
        self.pos = pos
        self.angle = 0
        self.base_sprite = pygame.transform.scale(turret_base_sprite, (TURRET_RADIUS * 2, TURRET_RADIUS * 2))
        self.gun_sprite = pygame.transform.scale(turret_gun_sprite, (TURRET_LENGTH, 20))  # Increased width for visibility

    def rotate(self, angle):
        self.angle += angle

    def draw(self, surface):
        # Draw base
        base_rect = self.base_sprite.get_rect(center=self.pos)
        surface.blit(self.base_sprite, base_rect)
        
        # Draw rotating gun
        rotated_gun = pygame.transform.rotate(self.gun_sprite, -math.degrees(self.angle))
        gun_rect = rotated_gun.get_rect(center=self.pos)
        surface.blit(rotated_gun, gun_rect)

        # Draw a bright outline around the turret for better visibility
        pygame.draw.circle(surface, (255, 255, 255), self.pos, TURRET_RADIUS + 2, 2)

turret = Turret(pygame.Vector2(game_frame_width / 2, game_frame_height - 50))

# Bullet and Asteroid settings
BULLET_SPEED = 400
bullets = []
bullet_cooldown = 0.5
last_shot_time = 0

ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED = 100, 200
asteroids = []
asteroid_hit_count = 0
turret_hit = False

# Timer settings
game_duration = 30
start_time = pygame.time.get_ticks()

font_path = "assets/BigBlue_Terminal_437TT.TTF"
font = pygame.font.Font(font_path, 40)
large_font = pygame.font.Font(font_path, 60)

class Bullet:
    def __init__(self, pos, angle):
        self.pos = pygame.Vector2(pos)
        self.angle = angle

    def update(self, dt):
        self.pos.x += math.cos(self.angle) * BULLET_SPEED * dt
        self.pos.y += math.sin(self.angle) * BULLET_SPEED * dt

    def draw(self, surface):
        pygame.draw.circle(surface, "white", (int(self.pos.x), int(self.pos.y)), 5)

class Asteroid:
    def __init__(self):
        self.radius = random.randint(20, 40)
        self.sprite = pygame.transform.scale(asteroid_sprite, (self.radius * 2, self.radius * 2))
        self.speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        self.pos, self.angle = self.spawn_from_edge()
        self.rotate_speed = random.uniform(-1, 1)
        self.alpha = 255  # Full opacity
        self.fade_speed = random.uniform(2, 5)  # Speed of fading in/out
        self.fading_in = True

    def spawn_from_edge(self):
        edge = random.choice(['top', 'left', 'right'])
        if edge == 'top':
            x = random.randint(0, game_frame_width)
            y = -self.radius * 2  # Spawn further away from the top edge
            angle = random.uniform(math.pi / 4, 3 * math.pi / 4)
        elif edge == 'left':
            x = -self.radius * 2  # Spawn further away from the left edge
            y = random.randint(0, game_frame_height)
            angle = random.uniform(-math.pi / 4, math.pi / 4)
        else:  # Right edge
            x = game_frame_width + self.radius * 2  # Spawn further away from the right edge
            y = random.randint(0, game_frame_height)
            angle = random.uniform(3 * math.pi / 4, 5 * math.pi / 4)
        return pygame.Vector2(x, y), angle

    def update(self, dt):
        self.pos.x += math.cos(self.angle) * self.speed * dt
        self.pos.y += math.sin(self.angle) * self.speed * dt
        self.sprite = pygame.transform.rotate(self.sprite, self.rotate_speed)

        # Update opacity
        if self.fading_in:
            self.alpha = min(255, self.alpha + self.fade_speed)
            if self.alpha == 255:
                self.fading_in = False
        else:
            self.alpha = max(0, self.alpha - self.fade_speed)
            if self.alpha == 0:
                self.fading_in = True

    def draw(self, surface):
        sprite_copy = self.sprite.copy()
        sprite_copy.set_alpha(self.alpha)
        rect = sprite_copy.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        surface.blit(sprite_copy, rect)

    def collides_with(self, other):
        return self.pos.distance_to(other.pos) < (self.radius + other.radius)

def check_collision(bullet, asteroid):
    return bullet.pos.distance_to(asteroid.pos) < asteroid.radius

def check_turret_collision(asteroid):
    return turret.pos.distance_to(asteroid.pos) < (asteroid.radius + TURRET_RADIUS)

def handle_asteroid_collisions():
    for i, asteroid1 in enumerate(asteroids):
        for asteroid2 in asteroids[i+1:]:
            if asteroid1.collides_with(asteroid2):
                asteroid1.angle, asteroid2.angle = asteroid2.angle, asteroid1.angle
                overlap = asteroid1.radius + asteroid2.radius - asteroid1.pos.distance_to(asteroid2.pos)
                direction = (asteroid1.pos - asteroid2.pos).normalize()
                asteroid1.pos += direction * overlap / 2
                asteroid2.pos -= direction * overlap / 2

def draw_timer_and_hits(remaining_time, hit_count):
    timer_text = font.render(f"Time: {int(remaining_time)}s", True, (255, 255, 255))
    screen.blit(timer_text, (1000, 20))
    hit_text = font.render(f"Asteroid Hits: {hit_count}/10", True, (255, 0, 0))
    screen.blit(hit_text, (10, 20))

def draw_win_screen():
    win_text = large_font.render("You Win!!!", True, (0, 255, 0))
    screen.blit(win_text, win_text.get_rect(center=(640, 360)))

def draw_lose_screen():
    lose_text = large_font.render("Oh no you lose", True, (255, 0, 0))
    screen.blit(lose_text, lose_text.get_rect(center=(640, 300)))
    
    button_width, button_height = 200, 50
    button_rect = pygame.Rect((1280 - button_width) // 2, 400, button_width, button_height)
    pygame.draw.rect(screen, (0, 255, 0), button_rect)
    
    button_font = pygame.font.Font(font_path, 30)
    button_text = button_font.render("Try Again", True, (0, 0, 0))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    
    return button_rect

def reset_game():
    global game_state, asteroid_hit_count, turret_hit, start_time, bullets, asteroids
    game_state = PLAYING
    asteroid_hit_count = 0
    turret_hit = False
    start_time = pygame.time.get_ticks()
    bullets = []
    asteroids = []
    turret.angle = 0

stars = [(random.randint((game_frame_width - 800) // 2, (game_frame_width + 800) // 2),
          random.randint(0, game_frame_height)) for _ in range(200)]

while running:
    screen.fill("black")
    game_frame.fill("black")
    for star in stars:
        pygame.draw.circle(game_frame, "white", star, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == LOSE:
            if try_again_button.collidepoint(event.pos):
                reset_game()

    if game_state == PLAYING
