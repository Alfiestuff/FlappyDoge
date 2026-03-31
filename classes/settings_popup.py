import pygame
import sys

class SettingsPopup:
    def __init__(self, screen):
        self.screen = screen
        self.active = False

        self.width = 400
        self.height = 300

        self.rect = pygame.Rect(
            (screen.get_width() // 2 - self.width // 2,
             screen.get_height() // 2 - self.height // 2),
            (self.width, self.height)
        )

        self.font = pygame.font.SysFont("Courier", 24)

        self.resolutions = [(1280, 720), (1600, 900), (1920, 1080)]
        self.res_index = 0

        self.sound_volume = 50  # 0 - 100

        self.close_button = pygame.Rect(
            self.rect.right - 40,
            self.rect.top + 10,
            30,
            30
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

            # close button
            if self.close_button.collidepoint(mx, my):
                self.close()

            # change resolution (click inside box area)
            if pygame.Rect(self.rect.x + 40, self.rect.y + 80, 200, 30).collidepoint(mx, my):
                self.res_index = (self.res_index + 1) % len(self.resolutions)

            # sound slider
            slider = pygame.Rect(self.rect.x + 40, self.rect.y + 160, 200, 10)
            if slider.collidepoint(mx, my):
                self.sound_volume = int(((mx - slider.x) / slider.width) * 100)

    def draw(self):
        if not self.active:
            return

        # dark overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # window
        pygame.draw.rect(self.screen, (40, 40, 40), self.rect, border_radius=10)
        pygame.draw.rect(self.screen, (80, 80, 80), self.rect, 2, border_radius=10)

        # title
        title = self.font.render("Settings", True, (255, 255, 255))
        self.screen.blit(title, (self.rect.x + 20, self.rect.y + 20))

        # resolution
        res_text = self.font.render(
            f"Resolution: {self.current_resolution()[0]}x{self.current_resolution()[1]}",
            True,
            (255, 255, 255)
        )
        pygame.draw.rect(self.screen, (60, 60, 60), (self.rect.x + 40, self.rect.y + 80, 200, 30))
        self.screen.blit(res_text, (self.rect.x + 45, self.rect.y + 85))

        # sound slider
        pygame.draw.rect(self.screen, (60, 60, 60), (self.rect.x + 40, self.rect.y + 160, 200, 10))
        pygame.draw.rect(
            self.screen,
            (0, 200, 255),
            (self.rect.x + 40, self.rect.y + 160, 2 * self.sound_volume, 10)
        )

        sound_text = self.font.render(f"Sound: {self.sound_volume}%", True, (255, 255, 255))
        self.screen.blit(sound_text, (self.rect.x + 40, self.rect.y + 130))

        # close button
        pygame.draw.rect(self.screen, (200, 50, 50), self.close_button)
        x = self.font.render("X", True, (255, 255, 255))
        self.screen.blit(x, (self.close_button.x + 7, self.close_button.y))