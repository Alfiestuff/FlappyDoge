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

        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.close_button = pygame.Rect(0, 0, 28, 28)

        self.res_box = pygame.Rect(40, 80, 240, 32)
        self.lang_box = pygame.Rect(40, 130, 240, 32)
        self.slider = pygame.Rect(40, 200, 240, 12)

    def open(self):
        self.active = True

    def close(self):
        self.active = False

    def toggle(self):
        self.active = not self.active

    def current_resolution(self):
        return self.resolutions[self.res_index]

    def _update_layout(self):
        self.rect.center = self.screen.get_rect().center
        self.close_button.topleft = (self.rect.right - 35, self.rect.top + 10)

    def handle_event(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if self.close_button.collidepoint(mx, my):
                self.close()

            if pygame.Rect(self.rect.x + self.res_box.x,
                           self.rect.y + self.res_box.y,
                           self.res_box.width,
                           self.res_box.height).collidepoint(mx, my):
                self.res_index = (self.res_index + 1) % len(self.resolutions)

            if pygame.Rect(self.rect.x + self.lang_box.x,
                           self.rect.y + self.lang_box.y,
                           self.lang_box.width,
                           self.lang_box.height).collidepoint(mx, my):
                self.lang_index = (self.lang_index + 1) % len(self.languages)

            slider_rect = pygame.Rect(
                self.rect.x + self.slider.x,
                self.rect.y + self.slider.y,
                self.slider.width,
                self.slider.height
            )

            if slider_rect.collidepoint(mx, my):
                self.sound_volume = max(
                    0,
                    min(100, int((mx - slider_rect.x) / slider_rect.width * 100))
                )

    def draw(self):
        if not self.active:
            return

        self._update_layout()

        # DARK BACKDROP
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # WINDOW
        pygame.draw.rect(self.screen, (35, 35, 35), self.rect, border_radius=10)
        pygame.draw.rect(self.screen, (90, 90, 90), self.rect, 2, border_radius=10)

        # TITLE
        title = self.font.render("Settings", True, (255, 255, 255))
        self.screen.blit(title, (self.rect.x + 20, self.rect.y + 15))

        hint = self.small_font.render("ESC to exit", True, (180, 180, 180))
        self.screen.blit(hint, (self.rect.x + 20, self.rect.y + 45))

        # RESOLUTION BOX
        res_rect = pygame.Rect(
            self.rect.x + self.res_box.x,
            self.rect.y + self.res_box.y,
            self.res_box.width,
            self.res_box.height
        )

        pygame.draw.rect(self.screen, (60, 60, 60), res_rect, border_radius=5)

        res_text = self.small_font.render(
            f"Resolution: {self.current_resolution()[0]}x{self.current_resolution()[1]}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(res_text, (res_rect.x + 10, res_rect.y + 5))

        # LANGUAGE BOX
        lang_rect = pygame.Rect(
            self.rect.x + self.lang_box.x,
            self.rect.y + self.lang_box.y,
            self.lang_box.width,
            self.lang_box.height
        )

        pygame.draw.rect(self.screen, (60, 60, 60), lang_rect, border_radius=5)

        lang_text = self.small_font.render(
            f"Language: {self.languages[self.lang_index]}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(lang_text, (lang_rect.x + 10, lang_rect.y + 5))

        # SLIDER
        slider_rect = pygame.Rect(
            self.rect.x + self.slider.x,
            self.rect.y + self.slider.y,
            self.slider.width,
            self.slider.height
        )

        pygame.draw.rect(self.screen, (70, 70, 70), slider_rect, border_radius=5)

        fill = int(slider_rect.width * (self.sound_volume / 100))
        pygame.draw.rect(self.screen, (0, 200, 255),
                         (slider_rect.x, slider_rect.y, fill, slider_rect.height),
                         border_radius=5)

        vol_text = self.small_font.render(
            f"Volume: {self.sound_volume}%",
            True,
            (255, 255, 255)
        )
        self.screen.blit(vol_text, (self.rect.x + 40, self.rect.y + 170))

        # CLOSE BUTTON
        pygame.draw.rect(self.screen, (200, 60, 60), self.close_button, border_radius=5)
        x = self.font.render("X", True, (255, 255, 255))
        self.screen.blit(x, (self.close_button.x + 7, self.close_button.y - 2))