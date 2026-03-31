import pygame
import sys
from classes.settings import *
from classes.utils import draw_grass


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.scroll = 0

        self.running = True
        self.show_settings = False

        # volume
        self.volume = 70
        self.drag = False

        # images
        self.sky = pygame.transform.scale(
            pygame.image.load("Images/sky.png").convert(),
            (W, H - GH)
        )

        self.grass = pygame.transform.scale(
            pygame.image.load("Images/grass.png").convert_alpha(),
            (GW, GH)
        )

        # 🐶 DOGE (fixed aspect ratio, NOT squished)
        img = pygame.image.load("Images/Doge.png").convert_alpha()

        size = 70  # target width
        ratio = img.get_height() / img.get_width()

        self.doge = pygame.transform.scale(img, (size, int(size * ratio)))
        self.doge_pos = (W // 2 + 200, H // 2 - 50)

        # font
        self.font = pygame.font.Font("./gui/fonts/pixel.ttf", 36)

        # buttons
        self.play = self._img("gui/buttons/Play.png", 160)
        self.settings_btn = self._img("gui/buttons/Settings_button.png", 160)

        cx, y = W // 2, H // 2 + 30
        self.play_rect = self.play.get_rect(center=(cx, y))
        self.settings_rect = self.settings_btn.get_rect(center=(cx, y + self.play_rect.height + 8))

        # settings panel
        self.panel = pygame.Surface((400, 300), pygame.SRCALPHA)
        self.panel_rect = self.panel.get_rect(center=(W // 2, H // 2))

        # slider
        self.slider = pygame.Rect(120, 150, 200, 6)
        self.knob_r = 10

    def _img(self, path, w):
        img = pygame.image.load(path).convert_alpha()
        h = int(img.get_height() * w / img.get_width())
        return pygame.transform.scale(img, (w, h))

    # ---------------- BACKGROUND ----------------
    def draw_bg(self):
        self.screen.blit(self.sky, (0, 0))
        draw_grass(self.screen, self.grass, self.scroll)

    # ---------------- DOGE ----------------
    def draw_doge(self):
        rect = self.doge.get_rect(center=self.doge_pos)
        self.screen.blit(self.doge, rect)

    # ---------------- TITLE ----------------
    def draw_title(self):
        t = self.font.render("Flappy Doge", True, (255, 255, 255))
        self.screen.blit(t, (W // 2 - t.get_width() // 2, H // 3))

    # ---------------- SLIDER ----------------
    def draw_slider(self):
        p = self.panel

        pygame.draw.rect(p, (70, 70, 70), self.slider, border_radius=3)

        fill = int(self.volume / 100 * self.slider.width)
        pygame.draw.rect(
            p,
            (0, 200, 255),
            (self.slider.x, self.slider.y, fill, self.slider.height),
            border_radius=3
        )

        x = self.slider.x + fill
        y = self.slider.y + self.slider.height // 2

        pygame.draw.circle(p, (255, 255, 255), (x, y), self.knob_r)
        pygame.draw.circle(p, (0, 200, 255), (x, y), self.knob_r, 2)

        p.blit(
            pygame.font.SysFont("Arial", 22).render("Volume", True, (255, 255, 255)),
            (20, 130)
        )

    # ---------------- SETTINGS ----------------
    def draw_settings(self):
        self.panel.fill((20, 20, 20, 230))

        self.panel.blit(self.font.render("Settings", True, (255, 255, 255)), (20, 20))
        self.panel.blit(
            pygame.font.SysFont("Arial", 18).render("ESC to close", True, (180, 180, 180)),
            (20, 80)
        )

        self.draw_slider()
        self.screen.blit(self.panel, self.panel_rect)

    # ---------------- INPUT ----------------
    def slider_value(self, mx):
        x = mx - self.panel_rect.x
        x = max(self.slider.x, min(x, self.slider.x + self.slider.width))

        self.volume = int((x - self.slider.x) / self.slider.width * 100)

    def handle(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.show_settings = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if self.show_settings:
                    knob_x = self.slider.x + int(self.volume / 100 * self.slider.width)
                    knob_y = self.slider.y + self.slider.height // 2

                    rx, ry = mx - self.panel_rect.x, my - self.panel_rect.y
                    if (rx - knob_x) ** 2 + (ry - knob_y) ** 2 < (self.knob_r + 5) ** 2:
                        self.drag = True
                    return

                if self.play_rect.collidepoint((mx, my)):
                    self.running = False

                if self.settings_rect.collidepoint((mx, my)):
                    self.show_settings = True

            if e.type == pygame.MOUSEBUTTONUP:
                self.drag = False

            if e.type == pygame.MOUSEMOTION and self.drag and self.show_settings:
                self.slider_value(pygame.mouse.get_pos()[0])

    # ---------------- DRAW ----------------
    def draw(self):
        self.draw_bg()
        self.draw_doge()
        self.draw_title()

        self.screen.blit(self.play, self.play_rect)
        self.screen.blit(self.settings_btn, self.settings_rect)

        if self.show_settings:
            dark = pygame.Surface((W, H))
            dark.set_alpha(160)
            self.screen.blit(dark, (0, 0))
            self.draw_settings()

    # ---------------- LOOP ----------------
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.scroll += SPEED

            self.handle()
            self.draw()

            pygame.mixer.music.set_volume(self.volume / 100)
            pygame.display.update()