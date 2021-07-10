import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color=pygame.Color((0, 0, 0)), image=None):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size

        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = pygame.Rect((self.x, self.y, self.size, self.size))
