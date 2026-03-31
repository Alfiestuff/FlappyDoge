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
        self.volume = 70
        self.drag = False

        self.language_index = 0
        self.languages = ["English", "Spanish", "French"]

        self.text = {
            "English": {
                "play": "PLAY",
                "settings": "SETTINGS",
                "quit": "QUIT",
                "title": "Flappy Doge"
            },
            "Spanish": {
                "play": "JUGAR",
                "settings": "AJUSTES",
                "quit": "SALIR",
                "title": "Flappy Doge"
            },
            "French": {
                "play": "JOUER",
                "settings": "PARAMÈTRES",
                "quit": "QUITTER",
                "title": "Flappy Doge"
            }
        }

        self.W, self.H = self.screen.get_size()

        self.sky = pygame.transform.scale(
            pygame.image.load("Images/sky.png").convert(),
            (self.W, self.H - GH)
        )

        self.grass = pygame.transform.scale(
            pygame.image.load("Images/grass.png").convert_alpha(),
            (GW, GH)
        )

        img = pygame.image.load("Images/Doge.png").convert_alpha()
        size = 70
        ratio = img.get_height() / img.get_width()
        self.doge = pygame.transform.scale(img, (size, int(size * ratio)))
        self.doge_pos = (self.W // 2 + 200, self.H // 2 - 50)

        self.font = pygame.font.Font("./gui/fonts/pixel.ttf", 28)
        self.small_font = pygame.font.SysFont("Arial", 18)

        cx, y = self.W // 2, self.H // 2 + 30

        self.play_rect = pygame.Rect(0, 0, 150, 40)
        self.play_rect.center = (cx, y)

        self.settings_rect = pygame.Rect(0, 0, 150, 40)
        self.settings_rect.center = (cx, y + 55)

        self.quit_rect = pygame.Rect(0, 0, 150, 40)
        self.quit_rect.center = (cx, y + 110)

        self.panel = pygame.Surface((420, 320), pygame.SRCALPHA)
        self.panel_rect = self.panel.get_rect(center=(self.W // 2, self.H // 2))

        self.slider = pygame.Rect(120, 170, 220, 6)
        self.knob_r = 10

        self.lang_rect = pygame.Rect(20, 105, 260, 30)

    def draw_bg(self):
        self.screen.blit(self.sky, (0, 0))
        draw_grass(self.screen, self.grass, self.scroll)

    def draw_doge(self):
        rect = self.doge.get_rect(center=self.doge_pos)
        self.screen.blit(self.doge, rect)

    def draw_button(self, rect, color, text):
        mx, my = pygame.mouse.get_pos()
        hover = rect.collidepoint((mx, my))
        c = tuple(min(255, i + 30) for i in color) if hover else color

        pygame.draw.rect(self.screen, c, rect, border_radius=12)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2, border_radius=12)

        txt = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(
            txt,
            (rect.centerx - txt.get_width() // 2,
             rect.centery - txt.get_height() // 2)
        )

    def draw_buttons(self):
        lang = self.languages[self.language_index]

        self.draw_button(self.play_rect, (200, 50, 50), self.text[lang]["play"])
        self.draw_button(self.settings_rect, (120, 120, 120), self.text[lang]["settings"])
        self.draw_button(self.quit_rect, (0, 120, 255), self.text[lang]["quit"])

    def draw_settings(self):
        self.panel.fill((25, 25, 25, 240))

        lang = self.languages[self.language_index]

        title = self.font.render(self.text[lang]["settings"], True, (255, 255, 255))
        self.panel.blit(title, (20, 20))

        vol_txt = self.small_font.render(f"Volume: {self.volume}%", True, (255, 255, 255))
        self.panel.blit(vol_txt, (20, 80))

        lang_txt = self.small_font.render(
            f"Language: {lang}",
            True,
            (255, 255, 255)
        )
        self.panel.blit(lang_txt, (self.lang_rect.x, self.lang_rect.y))
        pygame.draw.rect(self.panel, (80, 80, 80), self.lang_rect, 1, border_radius=6)

        hint = self.small_font.render("ESC to close", True, (150, 150, 150))
        self.panel.blit(hint, (20, 140))

        pygame.draw.rect(self.panel, (60, 60, 60), self.slider, border_radius=4)

        fill = int(self.volume / 100 * self.slider.width)
        pygame.draw.rect(
            self.panel,
            (0, 200, 255),
            (self.slider.x, self.slider.y, fill, self.slider.height),
            border_radius=4
        )

        x = self.slider.x + fill
        y = self.slider.y + self.slider.height // 2
        pygame.draw.circle(self.panel, (255, 255, 255), (x, y), self.knob_r)

        self.screen.blit(self.panel, self.panel_rect)

    def slider_value(self, mx):
        x = mx - self.panel_rect.x
        x = max(self.slider.x, min(x, self.slider.x + self.slider.width))
        self.volume = int((x - self.slider.x) / self.slider.width * 100)

    def handle(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.show_settings = False

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = pygame.mouse.get_pos()

                if self.show_settings:
                    rx, ry = mx - self.panel_rect.x, my - self.panel_rect.y

                    knob_x = self.slider.x + int(self.volume / 100 * self.slider.width)
                    knob_y = self.slider.y + self.slider.height // 2

                    if (rx - knob_x) ** 2 + (ry - knob_y) ** 2 < (self.knob_r + 5) ** 2:
                        self.drag = True
                        return

                    if self.lang_rect.collidepoint(rx, ry):
                        self.language_index = (self.language_index + 1) % len(self.languages)

                    return

                if self.play_rect.collidepoint((mx, my)):
                    self.running = False

                if self.settings_rect.collidepoint((mx, my)):
                    self.show_settings = True

                if self.quit_rect.collidepoint((mx, my)):
                    pygame.quit()
                    sys.exit()

            if e.type == pygame.MOUSEBUTTONUP:
                self.drag = False

            if e.type == pygame.MOUSEMOTION and self.drag and self.show_settings:
                self.slider_value(pygame.mouse.get_pos()[0])

    def draw(self):
        self.draw_bg()
        self.draw_doge()
        self.draw_buttons()

        if self.show_settings:
            dark = pygame.Surface((self.W, self.H))
            dark.set_alpha(160)
            self.screen.blit(dark, (0, 0))
            self.draw_settings()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.scroll += SPEED
            self.handle()
            self.draw()
            pygame.mixer.music.set_volume(self.volume / 100)
            pygame.display.update()