import random

import noise
import numpy as np


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
            noise_map[x][y] = noise.pnoise3(x / scale, y / scale, seed, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            noise_map[x][y] = (noise_map[x][y] + 1) / 2

    return noise_map
