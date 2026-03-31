import pygame
import sys
from classes.bird import Bird
from classes.pipe import Pipe
from classes.utils import draw_grass
from classes.settings import *
from classes.menu import Menu

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Doge")
clock = pygame.time.Clock()

font = pygame.font.Font("./gui/fonts/pixel.ttf", 32)

bird_img = pygame.transform.scale(
    pygame.image.load("Images/Doge.png").convert_alpha(),
    (76.5, 40)
)

grass_img = pygame.transform.scale(
    pygame.image.load("Images/grass.png").convert_alpha(),
    (GW, GH)
)

pipe_img = pygame.image.load("Images/pipe.png").convert_alpha()

sky_img = pygame.transform.scale(
    pygame.image.load("Images/sky.png").convert(),
    (W, H - GH)
)


def loop():
    bird = Bird()
    pipes = [Pipe(W + i * SPACING) for i in range(3)]
    pause = Pause()

    score, scroll = 0, 0
    over, can_flap = False, True
    show_hitboxes = False

    again_rect = pygame.Rect(0, 0, 200, 55)
    menu_rect = pygame.Rect(0, 0, 200, 55)

    again_rect.center = (W // 2, H // 2 - 40)
    menu_rect.center = (W // 2, H // 2 + 40)

    while True:
        clock.tick(FPS)
        screen.blit(sky_img, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and can_flap and not pause.active:
                    if not over:
                        bird.flap()
                    can_flap = False

                elif e.key == pygame.K_EQUALS:
                    show_hitboxes = not show_hitboxes

                elif e.key == pygame.K_MINUS:
                    pause.toggle()

            if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
                can_flap = True

            if pause.active:
                pause.handle_event(e)

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = pygame.mouse.get_pos()

                if over:
                    if again_rect.collidepoint((mx, my)):
                        return "restart"

                    if menu_rect.collidepoint((mx, my)):
                        return "menu"
                else:
                    bird.flap()

        if not over and not pause.active:
            bird.update()
            scroll += SPEED

        if bird.y + 25 >= H - GH or bird.y - 25 <= 0:
            bird.y = min(max(bird.y, 25), H - GH - 25)
            bird.dead = True
            over = True

        r = bird.rect()

        for p in pipes:
            if not over and not pause.active:
                p.update()

            p.draw(screen, pipe_img, show_hitboxes)

            if not p.passed and p.x + PW < bird.x and not over:
                p.passed = True
                score += 1

            if r.colliderect(p.rects()[0]) or r.colliderect(p.rects()[1]):
                bird.dead = True
                over = True

        if pipes[0].x + PW < 0:
            pipes.pop(0)
            pipes.append(Pipe(pipes[-1].x + SPACING))

        draw_grass(screen, grass_img, scroll)
        bird.draw(screen, bird_img)

        score_txt = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_txt, (W // 2 - score_txt.get_width() // 2, 20))

        if pause.active:
            pause.draw(screen)

        if over:
            overlay = pygame.Surface((W, H))
            overlay.set_alpha(160)
            overlay.fill((120, 120, 120))
            screen.blit(overlay, (0, 0))

            mx, my = pygame.mouse.get_pos()

            def draw_button(rect, color, text):
                hover = rect.collidepoint((mx, my))
                c = tuple(min(255, x + 30) for x in color) if hover else color

                pygame.draw.rect(screen, c, rect, border_radius=12)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=12)

                txt = font.render(text, True, (255, 255, 255))
                screen.blit(
                    txt,
                    (rect.centerx - txt.get_width() // 2,
                     rect.centery - txt.get_height() // 2)
                )

            draw_button(again_rect, (220, 60, 60), "PLAY AGAIN!")
            draw_button(menu_rect, (100, 100, 100), "MENU")

        pygame.display.update()


# ---------------- MAIN GAME FLOW ----------------

while True:
    menu = Menu(screen)
    menu.run()

    while True:
        result = loop()

        if result == "menu":
            break  # go back to menu

        if result == "restart":
            continue  # restart game instantly (NO MENU)