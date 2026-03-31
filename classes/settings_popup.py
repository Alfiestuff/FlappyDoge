import pygame

class SettingsPopup:
    def __init__(self, screen):
        self.screen = screen
        self.active = False

        self.width = 420
        self.height = 320

        self.font = pygame.font.SysFont("Courier", 24)
        self.small_font = pygame.font.SysFont("Courier", 20)

        self.resolutions = [(1280, 720), (1600, 900), (1920, 1080)]
        self.res_index = 0

        self.sound_volume = 50
        self.languages = ["English", "Spanish", "French", "German"]
        self.lang_index = 0

        self.rect = pygame.Rect(
            screen.get_width() // 2 - self.width // 2,
            screen.get_height() // 2 - self.height // 2,
            self.width,
            self.height
        )

        self.close_button = pygame.Rect(0, 0, 28, 28)
        self._update_close_button()

        self.res_box = pygame.Rect(40, 90, 220, 32)
        self.slider = pygame.Rect(40, 180, 220, 10)
        self.lang_box = pygame.Rect(40, 140, 220, 32)

    def _update_close_button(self):
        self.close_button.topleft = (
            self.rect.right - 38,
            self.rect.top + 10
        )

    def open(self):
        self.active = True

    def close(self):
        self.active = False

    def toggle(self):
        self.active = not self.active

    def current_resolution(self):
        return self.resolutions[self.res_index]

    def handle_event(self, event):
        if not self.active:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if self.close_button.collidepoint(mx, my):
                self.close()
                return

            if self.res_box.collidepoint(mx, my):
                self.res_index = (self.res_index + 1) % len(self.resolutions)

            if self.lang_box.collidepoint(mx, my):
                self.lang_index = (self.lang_index + 1) % len(self.languages)

            if self.slider.collidepoint(mx, my):
                self.sound_volume = int(
                    max(0, min(100, ((mx - self.slider.x) / self.slider.width) * 100))
                )

    def draw(self):
        if not self.active:
            return

        self.rect.topleft = (
            self.screen.get_width() // 2 - self.width // 2,
            self.screen.get_height() // 2 - self.height // 2
        )
        self._update_close_button()

        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        pygame.draw.rect(self.screen, (40, 40, 40), self.rect, border_radius=10)
        pygame.draw.rect(self.screen, (90, 90, 90), self.rect, 2, border_radius=10)

        title = self.font.render("Settings", True, (255, 255, 255))
        self.screen.blit(title, (self.rect.x + 20, self.rect.y + 15))

        # RESOLUTION
        pygame.draw.rect(self.screen, (60, 60, 60), self.res_box.move(self.rect.topleft))
        res = self.small_font.render(
            f"{self.current_resolution()[0]} x {self.current_resolution()[1]}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(res, (self.rect.x + 45, self.rect.y + 95))

        # LANGUAGE
        pygame.draw.rect(self.screen, (60, 60, 60), self.lang_box.move(self.rect.topleft))
        lang = self.small_font.render(
            f"Language: {self.languages[self.lang_index]}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(lang, (self.rect.x + 45, self.rect.y + 145))

        # VOLUME
        pygame.draw.rect(self.screen, (60, 60, 60), self.slider.move(self.rect.topleft))

        fill_width = int(self.slider.width * (self.sound_volume / 100))
        pygame.draw.rect(
            self.screen,
            (0, 200, 255),
            (self.rect.x + self.slider.x, self.rect.y + self.slider.y, fill_width, self.slider.height)
        )

        vol = self.small_font.render(f"Volume: {self.sound_volume}%", True, (255, 255, 255))
        self.screen.blit(vol, (self.rect.x + 40, self.rect.y + 155))

        # CLOSE BUTTON
        pygame.draw.rect(self.screen, (200, 60, 60), self.close_button, border_radius=5)
        x = self.font.render("X", True, (255, 255, 255))
        self.screen.blit(x, (self.close_button.x + 6, self.close_button.y - 2))