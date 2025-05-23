import pygame
import sys

# Initialiser Pygame
pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.Font(None, 50)

# Paramètres du jeu
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 30
player_speed = 7
ball_speed_x = 5
ball_speed_y = 5

# Clock
clock = pygame.time.Clock()


def menu():
    while True:
        screen.fill(BLACK)
        title = font.render("PING PONG", True, WHITE)
        option1 = font.render("1 - Joueur contre Joueur", True, WHITE)
        option2 = font.render("2 - Joueur contre IA", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        screen.blit(option1, (WIDTH // 2 - option1.get_width() // 2, 250))
        screen.blit(option2, (WIDTH // 2 - option2.get_width() // 2, 320))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return False  # pas d'IA
                elif event.key == pygame.K_2:
                    return True  # IA activée


def jouer(contre_ia=False):
    global ball_speed_x, ball_speed_y

    # Création des objets
    player1 = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    player2 = pygame.Rect(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

    score1 = 0
    score2 = 0

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Contrôle joueur 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= player_speed
        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += player_speed

        # Joueur 2 ou IA
        if contre_ia:
            if ball.centery > player2.centery and player2.bottom < HEIGHT:
                player2.y += player_speed - 2
            if ball.centery < player2.centery and player2.top > 0:
                player2.y -= player_speed - 2
        else:
            if keys[pygame.K_UP] and player2.top > 0:
                player2.y -= player_speed
            if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
                player2.y += player_speed

        # Mouvement de la balle
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Collision haut/bas
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Collision raquettes
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1

        # Score
        if ball.left <= 0:
            score2 += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= -1
        if ball.right >= WIDTH:
            score1 += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= -1

        # Dessin
        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, WHITE, player2)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
        score_text = font.render(f"{score1} - {score2}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)


# Lancement
contre_ia = menu()
jouer(contre_ia)
