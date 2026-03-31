import pygame


class Pause:
    def __init__(self):
        self.active = False
        self.font = pygame.font.SysFont("Courier", 32)
        self.button_font = pygame.font.SysFont("Courier", 26)

        self.button_rect = pygame.Rect(0, 0, 180, 60)

    def toggle(self):
        self.active = not self.active

    def draw_button(self, screen, rect, text):
        mx, my = pygame.mouse.get_pos()
        hover = rect.collidepoint((mx, my))

        color = (80, 160, 255) if hover else (50, 120, 220)

        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=12)

        txt = self.button_font.render(text, True, (255, 255, 255))
        screen.blit(
            txt,
            (rect.centerx - txt.get_width() // 2,
             rect.centery - txt.get_height() // 2)
        )

    def draw(self, screen):
        w, h = screen.get_size()

        overlay = pygame.Surface((w, h))
        overlay.set_alpha(180)
        overlay.fill((40, 40, 40))
        screen.blit(overlay, (0, 0))

        title = self.font.render("PAUSED", True, (255, 255, 255))
        screen.blit(title, (w // 2 - title.get_width() // 2, 120))

        self.button_rect.center = (w // 2, h // 2)
        self.draw_button(screen, self.button_rect, "RESUME")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.toggle()