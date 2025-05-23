import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong Game")

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

font = pygame.font.SysFont("Arial", 36)

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, gray, (x, y, w, h))
    label = font.render(text, True, black)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))

def show_winner(winner):
    while True:
        screen.fill(black)
        text = font.render(f"{winner} a gagné!", True, white)
        retry = font.render("ESPACE: rejouer | ECHAP: quitter", True, gray)

        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 50))
        screen.blit(retry, (width // 2 - retry.get_width() // 2, height // 2 + 20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    main_menu()

def game_loop():
    paddle_width, paddle_height = 10, 100
    ball_size = 20

    player1 = pygame.Rect(50, height // 2 - paddle_height // 2, paddle_width, paddle_height)
    player2 = pygame.Rect(width - 60, height // 2 - paddle_height // 2, paddle_width, paddle_height)
    ball = pygame.Rect(width // 2, height // 2, ball_size, ball_size)

    ball_speed_x, ball_speed_y = 5, 5
    paddle_speed = 7

    p1_score, p2_score = 0, 0

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Joueur 1 (W/S)
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= paddle_speed
        if keys[pygame.K_s] and player1.bottom < height:
            player1.y += paddle_speed

        # Joueur 2 (IA simple)
        if player2.centery < ball.centery and player2.bottom < height:
            player2.y += paddle_speed
        elif player2.centery > ball.centery and player2.top > 0:
            player2.y -= paddle_speed

        # Déplacer balle
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Rebonds haut/bas
        if ball.top <= 0 or ball.bottom >= height:
            ball_speed_y *= -1

        # Rebonds sur raquettes
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1

        # Gérer les points
        if ball.left <= 0:
            p2_score += 1
            ball.center = (width // 2, height // 2)
        if ball.right >= width:
            p1_score += 1
            ball.center = (width // 2, height // 2)

        # Fin de partie
        if p1_score == 7:
            show_winner("Joueur 1")
            running = False
        elif p2_score == 7:
            show_winner("Joueur 2")
            running = False

        # Dessiner raquettes, balle et score
        pygame.draw.rect(screen, white, player1)
        pygame.draw.rect(screen, white, player2)
        pygame.draw.ellipse(screen, white, ball)
        pygame.draw.aaline(screen, white, (width // 2, 0), (width // 2, height))

        score_text = font.render(f"{p1_score} - {p2_score}", True, white)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()

def main_menu():
    while True:
        screen.fill(white)
        draw_button("Jouer à deux", 300, 200, 200, 60)
        draw_button("Jouer contre IA", 300, 300, 200, 60)
        draw_button("Quitter", 300, 400, 200, 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 300 <= x <= 500:
                    if 200 <= y <= 260:
                        game_loop()  # tu peux modifier plus tard pour 2 joueurs
                    elif 300 <= y <= 360:
                        game_loop()  # même chose, à adapter pour IA
                    elif 400 <= y <= 460:
                        pygame.quit()
                        sys.exit()

main_menu()
