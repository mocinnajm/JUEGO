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
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego Extensible - Ampliación 2: Dificultad Incremental")
clock = pygame.time.Clock()

# Fuente para mostrar la puntuación y la dificultad
font = pygame.font.SysFont("Arial", 24)

# Variables globales para la puntuación y la dificultad
score = 0
difficulty_level = 1
last_difficulty_update_time = pygame.time.get_ticks()  # Tiempo inicial para la dificultad

# Definir intervalo inicial para la aparición de obstáculos (en milisegundos)
spawn_interval = 1500
ADD_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_OBSTACLE, spawn_interval)

# ========================
# Clases del juego
# ========================

class Player(pygame.sprite.Sprite):
    """Clase para el jugador."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.speed = 5

    def update(self):
        """Actualiza la posición del jugador según las teclas pulsadas."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Evitar que el jugador se salga de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Obstacle(pygame.sprite.Sprite):
    """Clase para los obstáculos."""
    def __init__(self):
        super().__init__()
        # Crear un obstáculo con dimensiones aleatorias
        width = random.randint(20, 100)
        height = random.randint(20, 100)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Posición inicial: fuera de la pantalla por la derecha
        self.rect.x = WIDTH + random.randint(10, 100)
        self.rect.y = random.randint(0, HEIGHT - height)
        # La velocidad se incrementa con la dificultad:
        # Se añade la dificultad al rango base de velocidad (entre 3 y 7)
        self.speed = random.randint(3 + difficulty_level, 7 + difficulty_level)

    def update(self):
        """Actualiza la posición del obstáculo desplazándolo a la izquierda.
           Si sale de la pantalla, se incrementa la puntuación y se elimina."""
        global score
        self.rect.x -= self.speed
        if self.rect.right < 0:
            score += 1  # Incrementar la puntuación
            self.kill()  # Eliminar el obstáculo

# ========================
# Grupos de sprites
# ========================
all_sprites = pygame.sprite.Group()  # Grupo con todos los sprites
obstacles = pygame.sprite.Group()    # Grupo específico para los obstáculos

# Crear el jugador y añadirlo al grupo principal
player = Player()
all_sprites.add(player)

# ========================
# Bucle principal del juego
# ========================
running = True
while running:
    clock.tick(FPS)  # Controlar la velocidad de fotogramas

    # Comprobar si ha pasado suficiente tiempo para incrementar la dificultad
    # (en este ejemplo, se aumenta la dificultad cada 15 segundos)
    current_time = pygame.time.get_ticks()
    if current_time - last_difficulty_update_time >= 15000:
        difficulty_level += 1
        last_difficulty_update_time = current_time
        # Reducir el intervalo de aparición de obstáculos, sin bajar de 500 ms
        spawn_interval = max(500, 1500 - difficulty_level * 100)
        pygame.time.set_timer(ADD_OBSTACLE, spawn_interval)
        print("Dificultad incrementada a:", difficulty_level)

    # Procesamiento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADD_OBSTACLE:
            # Crear un nuevo obstáculo y añadirlo a los grupos
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

    # Actualizar todos los sprites
    all_sprites.update()

    # Comprobar colisiones entre el jugador y los obstáculos
    if pygame.sprite.spritecollideany(player, obstacles):
        print("¡Colisión! Fin del juego.")
        running = False

    # Dibujar la escena
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Renderizar y mostrar la puntuación y la dificultad en pantalla
    score_text = font.render("Puntuación: " + str(score), True, BLACK)
    difficulty_text = font.render("Dificultad: " + str(difficulty_level), True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(difficulty_text, (10, 40))

    pygame.display.flip()

# Finalizar el juego
pygame.quit()
sys.exit()
