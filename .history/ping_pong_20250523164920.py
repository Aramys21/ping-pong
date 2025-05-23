import pygame 
import sys 

pygame.init() 

width, height = 800, 600 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong Game")

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)

font = pygame.font.SysFont("Arial", 36)

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, gray, (x, y, w, h))
    label = font.render(text, True, black)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))

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
                        print("Mode 2 joueurs choisi")
                    elif 300 <= y <= 360:
                        print("Mode contre IA choisi")
                    elif 400 <= y <= 460:
                        pygame.quit()
                        sys.exit()

main_menu()
