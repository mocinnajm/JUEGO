import pygame
import random
import sys

# ========================
# Configuració inicial
# ========================
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Inicialitzar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joc Extensible - Ampliació 3: Vides")
clock = pygame.time.Clock()

# Font per mostrar textos (puntuació, dificultat, vides)
font = pygame.font.SysFont("Arial", 24)

# Variables globals: puntuació, dificultat i vides
score = 0
difficulty_level = 1
lives = 3

# Control del temps per incrementar la dificultat (cada 15 segons)
last_difficulty_update_time = pygame.time.get_ticks()

# Interval inicial per generar obstacles (en mil·lisegons)
spawn_interval = 1500
ADD_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_OBSTACLE, spawn_interval)

# ========================
# Classes del joc
# ========================

class Player(pygame.sprite.Sprite):
    """Classe per al jugador."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.speed = 5

    def update(self):
        """Actualitza la posició del jugador segons les tecles premudes."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Evitar que el jugador surti de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Obstacle(pygame.sprite.Sprite):
    """Classe per als obstacles."""
    def __init__(self):
        super().__init__()
        # Crear un obstacle amb dimensions aleatòries
        width = random.randint(20, 100)
        height = random.randint(20, 100)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Posició inicial: fora de la pantalla per la dreta
        self.rect.x = WIDTH + random.randint(10, 100)
        self.rect.y = random.randint(0, HEIGHT - height)
        # La velocitat s'incrementa amb la dificultat:
        self.speed = random.randint(3 + difficulty_level, 7 + difficulty_level)

    def update(self):
        """Actualitza la posició de l'obstacle movent-lo cap a l'esquerra.
           Quan surt de la pantalla, incrementa la puntuació i s'elimina."""
        global score
        self.rect.x -= self.speed
        if self.rect.right < 0:
            score += 1  # Incrementar la puntuació
            self.kill()  # Eliminar l'obstacle

# ========================
# Grups de sprites
# ========================
all_sprites = pygame.sprite.Group()   # Conté tots els sprites
obstacles = pygame.sprite.Group()     # Grup específic per als obstacles

# Crear el jugador i afegir-lo al grup principal
player = Player()
all_sprites.add(player)

# ========================
# Bucle principal del joc
# ========================
running = True
while running:
    clock.tick(FPS)  # Controlar la velocitat de fotogrames

    # Comprovar si ha passat el temps per incrementar la dificultat (cada 15 segons)
    current_time = pygame.time.get_ticks()
    if current_time - last_difficulty_update_time >= 15000:
        difficulty_level += 1
        last_difficulty_update_time = current_time
        # Reduir l'interval d'aparició dels obstacles, amb un mínim de 500 ms
        spawn_interval = max(500, 1500 - difficulty_level * 100)
        pygame.time.set_timer(ADD_OBSTACLE, spawn_interval)
        print("Dificultat incrementada a:", difficulty_level)

    # Processament d'esdeveniments
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADD_OBSTACLE:
            # Crear un nou obstacle i afegir-lo als grups
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

    # Actualitzar tots els sprites
    all_sprites.update()

    # Comprovar col·lisions entre el jugador i els obstacles
    if pygame.sprite.spritecollideany(player, obstacles):
        # Quan es produeix una col·lisió, es resta una vida
        lives -= 1
        if lives > 0:
            # Si encara té vides, reinicialitzar la posició del jugador i esborra els obstacles
            player.rect.center = (100, HEIGHT // 2)
            for obs in obstacles:
                obs.kill()
            print("Has perdut una vida! Vides restants:", lives)
        else:
            # Si no hi ha més vides, acaba el joc
            print("Game Over! Puntuació final:", score)
            running = False

    # Dibuixar la escena
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Renderitzar i mostrar la puntuació, la dificultat i les vides en pantalla
    score_text = font.render("Puntuació: " + str(score), True, BLACK)
    difficulty_text = font.render("Dificultat: " + str(difficulty_level), True, BLACK)
    lives_text = font.render("Vides: " + str(lives), True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(difficulty_text, (10, 40))
    screen.blit(lives_text, (10, 70))

    pygame.display.flip()

# Finalitzar el joc
pygame.quit()
sys.exit()
