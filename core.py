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


def perlin_noise(size, seed, scale, octaves, persistence, lacunarity):
    noise_map = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            noise_map[x][y] = noise.pnoise3(x/scale, y/scale, seed, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            noise_map[x][y] = (noise_map[x][y] + 1) / 2

    return noise_map


def simplex_noise(size, seed, scale, octaves, persistence, lacunarity):
    noise_map = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            noise_map[x][y] = noise.snoise3(x/scale, y/scale, seed, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            noise_map[x][y] = (noise_map[x][y] + 1) / 2

    return noise_map


def generate_color_map(noise_map, region_colors):
    size = len(noise_map)
    color_map = np.empty((size, size), dtype=pygame.Color)
    for x in range(size):
        for y in range(size):
            for key, value in region_colors.items():
                if noise_map[x][y] <= key:
                    color_map[x][y] = value
                    break

    return color_map


def generate_falloff_map(map_size, a=3, b=2.2):
    falloff_map = np.zeros((map_size, map_size))
    for i in range(map_size):
        for j in range(map_size):
            x = i / map_size * 2 - 1
            y = j / map_size * 2 - 1

            value = max(abs(x), abs(y))
            falloff_map[i][j] = pow(value, a) / (pow(value, a) + pow(b - b*value, a))

    return falloff_map


if __name__ == '__main__':
    m = simplex_noise(5, 5, 5)
    print(m)
