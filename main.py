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
pygame.display.set_caption("Juego de Ejemplo Extensible")
clock = pygame.time.Clock()

# Grupo de balas
bullets = pygame.sprite.Group()

# ========================
# Clases del juego
# ========================

class Player(pygame.sprite.Sprite):
    """Clase para el jugador."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.speed = 5

    def update(self):
        """Mover el jugador."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Evitar que el jugador salga de la pantalla
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        """Disparar una bala."""
        bullet = Bullet(self.rect.right, self.rect.centery)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    """Clase para las balas."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 8

    def update(self):
        """Mover la bala hacia la derecha."""
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()  # Eliminar la bala si sale de la pantalla

class Obstacle(pygame.sprite.Sprite):
    """Clase para los obstáculos."""
    def __init__(self):
        super().__init__()
        width = random.randint(20, 100)
        height = random.randint(20, 100)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(10, 100)
        self.rect.y = random.randint(0, HEIGHT - height)
        self.speed = random.randint(3, 7)

    def update(self):
        """Mover el obstáculo hacia la izquierda."""
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# ========================
# Grupos de sprites
# ========================
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Crear el jugador y agregarlo al grupo principal
player = Player()
all_sprites.add(player)

# Definir un evento personalizado para agregar obstáculos
ADD_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_OBSTACLE, 1500)

# ========================
# Bucle principal del juego
# ========================
running = True
while running:
    clock.tick(FPS)

    # Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADD_OBSTACLE:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Disparar con ESPACIO
                player.shoot()

    # Actualizar sprites
    all_sprites.update()
    bullets.update()

    # Comprobar colisiones de balas con obstáculos
    for bullet in bullets:
        hit = pygame.sprite.spritecollideany(bullet, obstacles)
        if hit:
            bullet.kill()
            hit.kill()

    # Comprobar colisiones del jugador con los obstáculos
    if pygame.sprite.spritecollideany(player, obstacles):
        print("¡Colisión! Fin del juego.")
        running = False

    # Dibujar en la pantalla
    screen.fill(WHITE)
    all_sprites.draw(screen)
    bullets.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
