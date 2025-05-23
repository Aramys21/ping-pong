import pygame, sys

pygame.init()
w, h = 800, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Ping Pong Moderne")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (70, 70, 70)
LIGHT_GRAY = (200, 200, 200)
BLUE = (30, 144, 255)
DARK_BLUE = (10, 50, 100)

font_big = pygame.font.SysFont("Segoe UI", 48, bold=True)
font_medium = pygame.font.SysFont("Segoe UI", 32)
font_small = pygame.font.SysFont("Segoe UI", 20)

clock = pygame.time.Clock()

def draw_button(text, rect, mouse_pos):
    # Changer couleur au survol
    if rect.collidepoint(mouse_pos):
        color = BLUE
        txt_color = WHITE
    else:
        color = LIGHT_GRAY
        txt_color = DARK_BLUE
    pygame.draw.rect(screen, color, rect, border_radius=12)
    label = font_medium.render(text, True, txt_color)
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2,
                        rect.y + (rect.height - label.get_height()) // 2))

def main_menu():
    buttons = {
        "2 joueurs": pygame.Rect(300, 180, 200, 60),
        "Contre IA": pygame.Rect(300, 280, 200, 60),
        "Quitter": pygame.Rect(300, 380, 200, 60)
    }

    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        title = font_big.render("PING PONG MODERNE", True, BLUE)
        screen.blit(title, ((w - title.get_width()) // 2, 80))

        for text, rect in buttons.items():
            draw_button(text, rect, mouse_pos)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if buttons["2 joueurs"].collidepoint(mouse_pos):
                    game_loop("2joueurs")
                elif buttons["Contre IA"].collidepoint(mouse_pos):
                    game_loop("ia")
                elif buttons["Quitter"].collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

def draw_paddle(rect):
    # Ombre douce pour raquette
    shadow_rect = rect.move(4, 4)
    pygame.draw.rect(screen, (15, 15, 15), shadow_rect, border_radius=10)
    pygame.draw.rect(screen, BLUE, rect, border_radius=10)

def draw_ball(rect):
    # Cercle lumineux
    pygame.draw.ellipse(screen, BLUE, rect)
    glow = pygame.Surface((rect.width+12, rect.height+12), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (30, 144, 255, 80), glow.get_rect())
    screen.blit(glow, (rect.x-6, rect.y-6), special_flags=pygame.BLEND_RGBA_ADD)

def game_loop(mode):
    pw, ph, bs = 12, 100, 20
    p1 = pygame.Rect(50, h // 2 - ph // 2, pw, ph)
    p2 = pygame.Rect(w - 62, h // 2 - ph // 2, pw, ph)
    ball = pygame.Rect(w // 2, h // 2, bs, bs)
    bx, by = 6, 6
    speed = 8
    p1_score = p2_score = 0

    running = True
    while running:
        clock.tick(60)
        screen.fill(BLACK)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        # Joueur 1 (W/S)
        if keys[pygame.K_w] and p1.top > 0:
            p1.y -= speed
        if keys[pygame.K_s] and p1.bottom < h:
            p1.y += speed

        # Joueur 2
        if mode == "2joueurs":
            if keys[pygame.K_UP] and p2.top > 0:
                p2.y -= speed
            if keys[pygame.K_DOWN] and p2.bottom < h:
                p2.y += speed
        else:  # IA simple
            if p2.centery < ball.centery and p2.bottom < h:
                p2.y += speed
            if p2.centery > ball.centery and p2.top > 0:
                p2.y -= speed

        ball.x += bx
        ball.y += by

        # Rebond haut/bas
        if ball.top <= 0 or ball.bottom >= h:
            by = -by

        # Rebond raquettes
        if ball.colliderect(p1) or ball.colliderect(p2):
            bx = -bx

        # Points
        if ball.left <= 0:
            p2_score += 1
            ball.center = (w // 2, h // 2)
        if ball.right >= w:
            p1_score += 1
            ball.center = (w // 2, h // 2)

        # Fin de jeu
        if p1_score == 7:
            show_winner("Joueur 1")
            running = False
        elif p2_score == 7:
            show_winner("Joueur 2")
            running = False

        # Dessin
        draw_paddle(p1)
        draw_paddle(p2)
        draw_ball(ball)

        # Ligne centrale pointillée moderne
        for y in range(0, h, 30):
            pygame.draw.rect(screen, GRAY, (w // 2 - 5, y, 10, 15), border_radius=5)

        # Score semi-transparent
        score_bg = pygame.Surface((140, 60))
        score_bg.set_alpha(180)
        score_bg.fill(BLACK)
        screen.blit(score_bg, (w // 2 - 70, 10))

        score_text = font_big.render(f"{p1_score} - {p2_score}", True, WHITE)
        screen.blit(score_text, (w // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()

def show_winner(winner):
    while True:
        screen.fill(BLACK)
        text = font_big.render(f"{winner} a gagné!", True, BLUE)
        retry = font_small.render("ESPACE: rejouer | ECHAP: quitter", True, GRAY)
        screen.blit(text, ((w - text.get_width()) // 2, h // 2 - 50))
        screen.blit(retry, ((w - retry.get_width()) // 2, h // 2 + 20))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if e.key == pygame.K_SPACE:
                    main_menu()

main_menu()
