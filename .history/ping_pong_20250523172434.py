import pygame, sys
pygame.init()

w, h = 800, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Ping Pong")
font = pygame.font.SysFont("Arial", 36)

def draw_btn(t,x,y,w_,h_):
    pygame.draw.rect(screen, (128,128,128), (x,y,w_,h_))
    l = font.render(t,1,(0,0,0))
    screen.blit(l, (x+(w_-l.get_width())//2, y+(h_-l.get_height())//2))

def show_winner(w):
    while True:
        screen.fill((0,0,0))
        txt = font.render(f"{w} a gagné!",1,(255,255,255))
        retry = font.render("ESPACE: rejouer | ECHAP: quitter",1,(128,128,128))
        screen.blit(txt, ((w//2)-txt.get_width()//2, h//2-50))
        screen.blit(retry, ((w//2)-retry.get_width()//2, h//2+20))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if e.key==pygame.K_SPACE: return

def game_loop():
    pw, ph, bs = 10, 100, 20
    p1 = pygame.Rect(50, h//2 - ph//2, pw, ph)
    p2 = pygame.Rect(w-60, h//2 - ph//2, pw, ph)
    ball = pygame.Rect(w//2, h//2, bs, bs)
    bx, by = 5, 5
    speed = 7
    p1_score = p2_score = 0
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.fill((0,0,0))
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and p1.top > 0: p1.y -= speed
        if keys[pygame.K_s] and p1.bottom < h: p1.y += speed

        # IA simple
        if p2.centery < ball.centery and p2.bottom < h: p2.y += speed
        if p2.centery > ball.centery and p2.top > 0: p2.y -= speed

        ball.x += bx
        ball.y += by

        if ball.top <= 0 or ball.bottom >= h: by = -by
        if ball.colliderect(p1) or ball.colliderect(p2): bx = -bx

        if ball.left <= 0:
            p2_score += 1
            ball.center = (w//2, h//2)
        if ball.right >= w:
            p1_score += 1
            ball.center = (w//2, h//2)

        if p1_score == 7:
            show_winner("Joueur 1")
            break
        if p2_score == 7:
            show_winner("Joueur 2")
            break

        pygame.draw.rect(screen, (255,255,255), p1)
        pygame.draw.rect(screen, (255,255,255), p2)
        pygame.draw.ellipse(screen, (255,255,255), ball)
        pygame.draw.aaline(screen, (255,255,255), (w//2,0), (w//2,h))

        score = font.render(f"{p1_score} - {p2_score}", 1, (255,255,255))
        screen.blit(score, (w//2 - score.get_width()//2, 20))
        pygame.display.flip()

def main_menu():
    while True:
        screen.fill((255,255,255))
        draw_btn("Jouer à deux", 300, 200, 200, 60)
        draw_btn("Jouer contre IA", 300, 300, 200, 60)
        draw_btn("Quitter", 300, 400, 200, 60)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                x,y = e.pos
                if 300 <= x <= 500:
                    if 200 <= y <= 260: game_loop()
                    elif 300 <= y <= 360: game_loop()
                    elif 400 <= y <= 460: pygame.quit(); sys.exit()

main_menu()
