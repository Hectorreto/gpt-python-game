import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

while True:
    # Establecer las dimensiones de la pantalla
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Establecer el título de la ventana
    pygame.display.set_caption("Mi juego en Pygame")

    # Establecer los colores
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    yellow = (255, 255, 0)

    # Establecer las propiedades del jugador
    player_x = 400
    player_y = 500
    player_width = 40
    player_height = 40
    player_speed = 5

    # Establecer las propiedades de los objetos
    object_width = 20
    object_height = 20
    object_speed = 1

    # Establecer las propiedades de los obstáculos
    obstacle_width = 40
    obstacle_height = 40
    obstacle_speed = 2

    # Establecer las propiedades de los objetos recolectables
    object_points = 1

    # Establecer las propiedades del objeto de aumento de velocidad
    speed_boost_duration = 5
    speed_boost_amount = 10

    # Crear el reloj
    clock = pygame.time.Clock()

    # Crear las listas de objetos, obstáculos y velocidad de aumento
    objects = []
    obstacles = []
    speed_boosts = []
    clearers = []

    # Establecer la puntuación
    score = 0

    # Establecer el estado del juego
    game_over = False

    # Establecer el tiempo restante del aumento de velocidad
    speed_boost_time = 0

    # Función para crear obstáculos
    def create_obstacle():
        obstacle_x = random.randint(0, screen_width - obstacle_width)
        obstacle_y = -obstacle_height
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
        obstacles.append(obstacle_rect)

    # Función para crear objetos recolectables
    def create_object():
        object_x = random.randint(0, screen_width - object_width)
        object_y = -object_height
        object_rect = pygame.Rect(object_x, object_y, object_width, object_height)
        objects.append(object_rect)

    def create_clearer():
        object_x = random.randint(0, screen_width - object_width)
        object_y = -object_height
        object_rect = pygame.Rect(object_x, object_y, object_width, object_height)
        clearers.append(object_rect)

    # Función para crear el objeto de aumento de velocidad
    def create_speed_boost():
        speed_boost_x = random.randint(0, screen_width - object_width)
        speed_boost_y = -object_height
        speed_boost_rect = pygame.Rect(speed_boost_x, speed_boost_y, object_width, object_height)
        speed_boosts.append(speed_boost_rect)

    # Función para mover el jugador
    def move_player(keys_pressed):
        global player_x, player_y, speed_boost_time
        if keys_pressed[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed + (speed_boost_amount if speed_boost_time > 0 else 0)
        if keys_pressed[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed + (speed_boost_amount if speed_boost_time > 0 else 0)
        if keys_pressed[pygame.K_UP] and player_y > 0:
            player_y -= player_speed + (speed_boost_amount if speed_boost_time > 0 else 0)
        if keys_pressed[pygame.K_DOWN] and player_y < screen_height - player_height:
            player_y += player_speed + (speed_boost_amount if speed_boost_time > 0 else 0)

        if keys_pressed[pygame.K_ESCAPE]:
            # Salir de Pygame y del programa
            pygame.quit()
            sys.exit()

        # Restar el tiempo restante del aumento de velocidad si es mayor que cero
        if speed_boost_time > 0:
            speed_boost_time -= 1 / 60

    # Función para mover los objetos
    def move_objects():
        global score, game_over, speed_boost_time, obstacles
        for object_rect in objects:
            object_rect.y += object_speed
            if object_rect.colliderect(player_rect):
                score += object_points
                objects.remove(object_rect)
        for obstacle_rect in obstacles:
            obstacle_rect.y += obstacle_speed
            if obstacle_rect.colliderect(player_rect):
                if not speed_boost_time > 0:
                    game_over = True
        for speed_boost_rect in speed_boosts:
            speed_boost_rect.y += 1
            if speed_boost_rect.colliderect(player_rect):
                score += 1
                speed_boost_time = speed_boost_duration
                speed_boosts.remove(speed_boost_rect)
        for clearer_rect in clearers:
            clearer_rect.y += 1
            if clearer_rect.colliderect(player_rect):
                score += len(obstacles)
                obstacles = []
                clearers.remove(clearer_rect)

        # Eliminar los obstáculos que han salido de la pantalla
        for obstacle in obstacles[:]:
            if obstacle.top > screen_height:
                obstacles.remove(obstacle)

        # Eliminar los objetos recolectables que han salido de la pantalla
        for object in objects[:]:
            if object.top > screen_height:
                objects.remove(object)
                game_over = True

        # Eliminar los objetos de aumento de velocidad que han salido de la pantalla
        for speed_boost in speed_boosts[:]:
            if speed_boost.top > screen_height:
                speed_boosts.remove(speed_boost)

        for clearer in clearers[:]:
            if clearer.top > screen_height:
                clearers.remove(clearer)

    # Función para dibujar los objetos
    def draw_objects():
        for obstacle_rect in obstacles:
            pygame.draw.rect(screen, green if speed_boost_time > 0 else red, obstacle_rect)
        for object_rect in objects:
            pygame.draw.rect(screen, blue, object_rect)
        for speed_boost_rect in speed_boosts:
            pygame.draw.rect(screen, green, speed_boost_rect)
        for clearer_rect in clearers:
            pygame.draw.rect(screen, yellow, clearer_rect)

    # Función para dibujar la pantalla de juego
    def draw_game():
        screen.fill(black)
        pygame.draw.rect(screen, white, player_rect)
        draw_objects()
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Puntuación: {str(score)}", True, white)
        screen.blit(score_text, (10, 10))
        pygame.display.update()

    # Crear el rectángulo del jugador
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Bucle principal del juego
    while not game_over:
        # Manejar los eventos de Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Mover el jugador
        keys_pressed = pygame.key.get_pressed()
        move_player(keys_pressed)
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # Crear objetos y obstáculos aleatorios
        if random.randint(0, 50) == 0:
            create_object()
        if random.randint(0, 30) == 0:
            create_obstacle()
        if random.randint(0, 1000) == 0:
            create_speed_boost()
        if random.randint(0, 1000) == 0:
            create_clearer()

        # Mover los objetos
        move_objects()

        # Dibujar la pantalla del juego
        draw_game()

        # Verificar si se ha perdido el juego
        if score < 0:
            game_over = True

        # Establecer el título de la ventana con la puntuación
        pygame.display.set_caption("Juego de objetos - Puntuación: " + str(score))

        # Esperar un corto período de tiempo
        clock.tick(60)

    # Si se ha perdido el juego, mostrar un mensaje de "Game Over"
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("Game Over", True, red)
    screen.blit(game_over_text, (screen_width/2 - game_over_text.get_width()/2, screen_height/2 - game_over_text.get_height()/2))
    pygame.display.update()

    # Esperar tres segundos antes de reiniciar
    pygame.time.wait(3000)
