import pygame


class DogeUI:
    def __init__(self, screen, size=120):
        self.screen = screen
        self.W, self.H = screen.get_size()

        # load image safely
        img = pygame.image.load("Images/Doge.png").convert_alpha()

        ratio = img.get_width() / img.get_height()
        self.doge = pygame.transform.scale(img, (size, int(size / ratio)))

        # position doge
        self.doge_pos = (self.W // 2 + 200, self.H // 2 - 50)

        # language system (simple example)
        self.languages = ["EN", "ES", "FR", "DE"]
        self.lang_index = 0

        self.font = pygame.font.SysFont("Courier", 24)

        # language button
        self.lang_rect = pygame.Rect(20, 105, 260, 30)

    def toggle_language(self):
        self.lang_index = (self.lang_index + 1) % len(self.languages)

    def draw(self):
        # draw doge
        self.screen.blit(self.doge, self.doge_pos)

        # draw language button
        lang_text = self.font.render(
            f"Language: {self.languages[self.lang_index]}",
            True,
            (255, 255, 255)
        )

        pygame.draw.rect(self.screen, (60, 60, 60), self.lang_rect, border_radius=6)
        self.screen.blit(lang_text, (self.lang_rect.x + 10, self.lang_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.lang_rect.collidepoint(event.pos):
                self.toggle_language()