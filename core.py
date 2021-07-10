import random

import noise
import numpy as np
import pygame


def random_noise(size, seed):
    random.seed(seed)
    map_ = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            map_[x][y] = random.random()

    return map_


def perlin_noise(size, seed, scale, octaves=1, persistence=0.5, lacunarity=2):
    noise_map = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            noise_map[x][y] = noise.pnoise3(x / scale, y / scale, seed, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            noise_map[x][y] = (noise_map[x][y] + 1) / 2

    return noise_map


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color=pygame.Color((0, 0, 0)), image=None):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size

        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = pygame.Rect((self.x, self.y, self.size, self.size))
