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
        self.state = "menu"

        self.W, self.H = self.screen.get_size()

        self.languages = ["English", "Spanish", "French"]
        self.language_index = 0

        self.text = {
            "English": {"play": "PLAY", "quit": "QUIT"},
            "Spanish": {"play": "JUGAR", "quit": "SALIR"},
            "French": {"play": "JOUER", "quit": "QUITTER"}
        }

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

        self.play_rect = pygame.Rect(0, 0, 160, 45)
        self.quit_rect = pygame.Rect(0, 0, 160, 45)

        self.update_layout()

    def update_layout(self):
        self.W, self.H = self.screen.get_size()

        cx, y = self.W // 2, self.H // 2 + 30

        self.play_rect.center = (cx, y)
        self.quit_rect.center = (cx, y + 70)

    def draw_background(self):
        self.screen.blit(self.sky, (0, 0))
        draw_grass(self.screen, self.grass, self.scroll)

    def draw_doge(self):
        rect = self.doge.get_rect(center=self.doge_pos)
        self.screen.blit(self.doge, rect)

    def draw_button(self, rect, base_color, text):
        mx, my = pygame.mouse.get_pos()
        hover = rect.collidepoint(mx, my)

        color = tuple(min(255, c + 30) for c in base_color) if hover else base_color

        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2, border_radius=12)

        label = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(
            label,
            (rect.centerx - label.get_width() // 2,
             rect.centery - label.get_height() // 2)
        )

    def draw_ui(self):
        lang = self.languages[self.language_index]

        self.draw_button(self.play_rect, (200, 50, 50), self.text[lang]["play"])
        self.draw_button(self.quit_rect, (0, 120, 255), self.text[lang]["quit"])

    def handle(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos

                if self.play_rect.collidepoint(mx, my):
                    self.state = "play"
                    self.running = False

                if self.quit_rect.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

    def draw(self):
        self.draw_background()
        self.draw_doge()
        self.draw_ui()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.scroll += SPEED
            self.update_layout()
            self.handle()
            self.draw()
            pygame.display.update()

        return self.state