import pygame
import random
import sys

# ========================
# Configuración inicial
# ========================
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
DeepSkyBlue = (0, 191, 255)
COLORS = [RED, BLUE, GREEN, YELLOW, PURPLE, CYAN, DeepSkyBlue]

# Inicializar Pygame y la ventana
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joc Extensible - Ampliació 4: Menú i Reinici")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Stencil", 24)

# Cargar la música
try:
    pygame.mixer.music.load("9090.mp3")  # Cambia por la ruta correcta
    pygame.mixer.music.set_volume(0.5)
except pygame.error:
    print("No se pudo cargar la música.")

# ========================
# Variables Globales del Juego
# ========================
score = 0
difficulty_level = 1
lives = 3
spawn_interval = 1500
ADD_OBSTACLE = pygame.USEREVENT + 1

# Grupos de sprites
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# ========================
# Funciones Auxiliares
# ========================

def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# ========================
# Clases del Juego
# ========================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("123.png")
            self.image = pygame.transform.scale(self.image, (50, 50))
        except FileNotFoundError:
            self.image = pygame.Surface((50, 50))
            self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.midleft = (x, y)
        self.speed = 8

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = random.choice(COLORS)
        width, height = random.randint(20, 100), random.randint(20, 100)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, width, height))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(10, 100)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(3 + difficulty_level, 7 + difficulty_level)

    def update(self):
        global score
        self.rect.x -= self.speed
        if self.rect.right < 0:
            score += 1
            self.kill()

# ========================
# Función para reiniciar el juego
# ========================

def new_game():
    global score, difficulty_level, lives, player
    score = 0
    difficulty_level = 1
    lives = 3
    all_sprites.empty()
    obstacles.empty()
    bullets.empty()
    player = Player()
    all_sprites.add(player)
    pygame.time.set_timer(ADD_OBSTACLE, spawn_interval)

# ========================
# Bucle principal del juego
# ========================

def game_loop():
    new_game()
    pygame.mixer.music.play(-1)
    running, paused = True, False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == ADD_OBSTACLE and not paused:
                obstacle = Obstacle()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_SPACE:
                    player.shoot()

        if not paused:
            all_sprites.update()
            for bullet in bullets:
                if pygame.sprite.spritecollide(bullet, obstacles, True):
                    bullet.kill()
            
            if pygame.sprite.spritecollideany(player, obstacles):
                global lives
                lives -= 1
                if lives > 0:
                    player.rect.center = (100, HEIGHT // 2)
                    obstacles.empty()
                else:
                    running = False

        screen.fill(DeepSkyBlue)
        all_sprites.draw(screen)
        draw_text(screen, f"Puntuació: {score}", font, BLACK, 10, 10)
        draw_text(screen, f"Vides: {lives}", font, BLACK, 10, 40)
        if paused:
            draw_text(screen, "PAUSA", font, RED, WIDTH // 2 - 50, HEIGHT // 2)
        pygame.display.flip()
    return score

# ========================
# Bucle principal
# ========================
while True:
    game_loop()
