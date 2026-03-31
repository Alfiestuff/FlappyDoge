import pygame
import sys
import random
import math
from classes.settings import *
from classes.utils import draw_grass


class Particle:
    def __init__(self):
        self.x = random.randint(0, W)
        self.y = random.randint(0, H)
        self.speed = random.uniform(0.2, 0.6)
        self.size = random.randint(2, 4)

    def update(self):
        self.y -= self.speed
        if self.y < -10:
            self.y = H
            self.x = random.randint(0, W)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size)


class Button:
    def __init__(self, image, x, y):
        self.base_image = image
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.scale = 1.0

    def update(self, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        target = 1.08 if hovered else 1.0
        self.scale += (target - self.scale) * 0.15

        center = self.rect.center
        w = int(self.base_image.get_width() * self.scale)
        h = int(self.base_image.get_height() * self.scale)

        self.image = pygame.transform.scale(self.base_image, (w, h))
        self.rect = self.image.get_rect(center=center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.scroll = 0

        self.running = True
        self.show_settings = False

        self.particles = [Particle() for _ in range(40)]

        self.sky_img = pygame.transform.scale(
            pygame.image.load("Images/sky.png").convert(),
            (W, H - GH)
        )

        self.grass_img = pygame.transform.scale(
            pygame.image.load("Images/grass.png").convert_alpha(),
            (GW, GH)
        )

        try:
            self.font = pygame.font.Font("./gui/fonts/pixel.ttf", 40)
        except:
            self.font = pygame.font.SysFont("Courier", 40)

        self._load_buttons()

    def _load_buttons(self):
        def scale(img):
            w = 150
            r = img.get_height() / img.get_width()
            return pygame.transform.scale(img, (w, int(w * r)))

        play_img = scale(pygame.image.load("gui/buttons/Play.png").convert_alpha())
        settings_img = scale(pygame.image.load("gui/buttons/Settings_button.png").convert_alpha())

        cx = W // 2

        self.play_button = Button(play_img, cx, H // 2 + 60)
        self.settings_button = Button(settings_img, cx, H // 2 + 120)

    def draw_settings(self):
        panel = pygame.Surface((420, 280))
        panel.fill((35, 35, 35))

        title = self.font.render("Settings", True, (255, 255, 255))
        panel.blit(title, (20, 20))

        text = pygame.font.SysFont("Arial", 20).render(
            "Press ESC to close", True, (180, 180, 180)
        )
        panel.blit(text, (20, 90))

        rect = panel.get_rect(center=(W // 2, H // 2))
        self.screen.blit(panel, rect)

    def draw_background(self):
        self.screen.blit(self.sky_img, (0, 0))
        draw_grass(self.screen, self.grass_img, self.scroll)

    def draw_title(self):
        offset = math.sin(pygame.time.get_ticks() * 0.002) * 5
        text = self.font.render("Flappy Doge", True, (255, 255, 255))
        self.screen.blit(text, (W // 2 - text.get_width() // 2, H // 3 + offset))

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.show_settings = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.show_settings:
                    continue

                if self.play_button.rect.collidepoint(e.pos):
                    self.running = False

                if self.settings_button.rect.collidepoint(e.pos):
                    self.show_settings = True

    def update(self):
        for p in self.particles:
            p.update()

        mouse = pygame.mouse.get_pos()
        self.play_button.update(mouse)
        self.settings_button.update(mouse)

    def draw(self):
        self.draw_background()

        for p in self.particles:
            p.draw(self.screen)

        self.draw_title()

        self.play_button.draw(self.screen)
        self.settings_button.draw(self.screen)

        if self.show_settings:
            dark = pygame.Surface((W, H))
            dark.set_alpha(160)
            dark.fill((0, 0, 0))
            self.screen.blit(dark, (0, 0))
            self.draw_settings()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.scroll += SPEED

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()