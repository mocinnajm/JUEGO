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
COLORS = [RED, BLUE, GREEN, YELLOW, PURPLE, CYAN]  # Lista de colores

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego Extensible - Ampliación 1: Puntuación")
clock = pygame.time.Clock()

# Fuente para mostrar la puntuación
font = pygame.font.SysFont("Arial", 24)

# Variable global para la puntuación
score = 0

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
        """Actualiza la posición del jugador según las teclas presionadas."""
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
        # Crear un obstáculo de tamaño aleatorio
        width = random.randint(20, 100)
        height = random.randint(20, 100)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Superficie con transparencia
        self.color = random.choice(COLORS)  # Seleccionar un color aleatorio
        self.shape = random.choice(["rectangle", "circle", "triangle"])  # Seleccionar una forma aleatoria

        # Dibujar la forma en la superficie
        if self.shape == "rectangle":
            pygame.draw.rect(self.image, self.color, (0, 0, width, height))
        elif self.shape == "circle":
            radius = min(width, height) // 2
            pygame.draw.circle(self.image, self.color, (width // 2, height // 2), radius)
        elif self.shape == "triangle":
            points = [(width // 2, 0), (0, height), (width, height)]
            pygame.draw.polygon(self.image, self.color, points)

        self.rect = self.image.get_rect()
        # Ubicación inicial: fuera de la pantalla por la derecha
        self.rect.x = WIDTH + random.randint(10, 100)
        self.rect.y = random.randint(0, HEIGHT - height)
        self.speed = random.randint(3, 7)

    def update(self):
        """Actualiza la posición del obstáculo moviéndolo a la izquierda.
           Si sale de la pantalla, incrementa la puntuación y se elimina."""
        global score
        self.rect.x -= self.speed
        # Si el obstáculo sale completamente de la pantalla
        if self.rect.right < 0:
            score += 1  # Incrementar la puntuación
            self.kill()  # Eliminar el obstáculo

# ========================
# Grupos de sprites
# ========================
all_sprites = pygame.sprite.Group()  # Todos los sprites del juego
obstacles = pygame.sprite.Group()    # Grupo específico para los obstáculos

# Crear el jugador y agregarlo al grupo principal
player = Player()
all_sprites.add(player)

# Definir un evento personalizado para agregar obstáculos de forma periódica
ADD_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_OBSTACLE, 1500)  # Cada 1500 milisegundos se añade un obstáculo

# ========================
# Bucle principal del juego
# ========================
running = True
while running:
    clock.tick(FPS)  # Controlar la velocidad del juego

    # Procesamiento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADD_OBSTACLE:
            # Crear un nuevo obstáculo y añadirlo a los grupos correspondientes
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

    # Actualización de sprites
    all_sprites.update()

    # Comprobar colisiones entre el jugador y los obstáculos
    if pygame.sprite.spritecollideany(player, obstacles):
        print("¡Colisión! Fin del juego.")
        running = False

    # Dibujar en la pantalla
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Renderizar y mostrar la puntuación en la pantalla
    score_text = font.render("Puntuación: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()