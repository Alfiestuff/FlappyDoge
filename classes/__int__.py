img = pygame.image.load("Images/Doge.png").convert_alpha()

size = 70  # width you want
ratio = img.get_height() / img.get_width()

self.doge = pygame.transform.scale(img, (size, int(size * ratio)))

self.doge_pos = (W // 2 + 200, H // 2 - 50)