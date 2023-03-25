import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir las dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de recoger objetos")

# Definir los colores que se usarán en el juego
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Definir la velocidad del personaje
player_speed = 5

# Definir la velocidad de los obstáculos
obstacle_speed = 3

# Definir las dimensiones del personaje y los obstáculos
player_width = 50
player_height = 50
obstacle_width = 50
obstacle_height = 50

# Definir la posición inicial del personaje
player_x = screen_width / 2 - player_width / 2
player_y = screen_height - player_height

# Definir la lista de obstáculos
obstacles = []

# Definir la lista de objetos recolectables
objects = []

# Definir la función para crear un objeto recolectable en una posición aleatoria
def create_object():
    object_x = random.randint(0, screen_width - obstacle_width)
    object_y = random.randint(0, screen_height / 2)
    objects.append(pygame.Rect(object_x, object_y, obstacle_width, obstacle_height))

# Definir la función para crear un obstáculo en una posición aleatoria
def create_obstacle():
    obstacle_x = random.randint(0, screen_width - obstacle_width)
    obstacle_y = 0
    obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))

# Bucle principal del juego
game_over = False
clock = pygame.time.Clock()
score = 0
while not game_over:
    # Manejar eventos del teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Mover el personaje
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Mover los obstáculos y los objetos recolectables
    for obstacle in obstacles:
        obstacle.move_ip(0, obstacle_speed)
    for object in objects:
        object.move_ip(0, obstacle_speed)

    # Eliminar los obstáculos que han salido de la pantalla
    for obstacle in obstacles[:]:
        if obstacle.bottom > screen_height:
            obstacles.remove(obstacle)

    # Eliminar los objetos recolectables que han salido de la pantalla
    for object in objects[:]:
        if object.bottom > screen_height:
            objects.remove(object)

    # Comprobar si el personaje ha tocado un objeto recolectable
    for object in objects[:]:
        if object.colliderect((player_x, player_y, player_width, player_height)):
            objects.remove(object)
            score += 1

    # Comprobar si el personaje ha tocado un obstáculo
    for obstacle in obstacles[:]:
        if obstacle.colliderect((player_x, player_y, player_width, player_height)):
            game_over = True

    # Crear obstáculos y objetos recolectables aleatorios
    if random.randint(0, 100) < 5:
        create_obstacle()
    if random.randint(0, 100) < 5:
        create_object()

    # Pintar la pantalla
    screen.fill(black)

    # Pintar el personaje
    player_rect = pygame.draw.rect(screen, red, (player_x, player_y, player_width, player_height))

    # Pintar los obstáculos
    for obstacle in obstacles:
        pygame.draw.rect(screen, blue, obstacle)

    # Pintar los objetos recolectables
    for object in objects:
        pygame.draw.rect(screen, green, object)

    # Mostrar la puntuación
    font = pygame.font.Font(None, 36)
    text = font.render("Puntuación: " + str(score), True, white)
    screen.blit(text, (10, 10))

    # Actualizar la pantalla
    pygame.display.update()

    # Establecer la velocidad de fotogramas
    clock.tick(60)
