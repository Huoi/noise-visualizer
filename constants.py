import pygame

MAP_SIZE = 500

BLACK = pygame.Color((0, 0, 0))
WHITE = pygame.Color((255, 255, 255))
BLUE = pygame.Color((0, 0, 255))
YELLOW = pygame.Color((255, 255, 0))
GREEN = pygame.Color((0, 255, 0))
GRAY = pygame.Color((55, 55, 55))

REGION_COLORS = {
    0.45: BLUE,
    0.55: YELLOW,
    0.6: GREEN,
    0.8: GRAY,
    1: WHITE
}

PANEL_SIZE = (250, 500)
MARGIN = 5
ELEMENT_HEIGHT = 27

SEED = 0
MAP_OPTIONS = [
    "Random Noise Map",
    "Perlin Noise Map",
    "Simplex Noise Map",
    "Falloff Map"
]
TILE_SIZE = 5
APPLY_COLOR = False
USE_FALLOFF = False

SCALE = 15
OCTAVES = 8
PERSISTENCE = 0.5
LACUNARITY = 2.0

SEED_RANGE = (0, 100)
SCALE_RANGE = (1, 30)
OCTAVES_RANGE = (1, 8)
PERSISTENCE_RANGE = (0.0, 5.0)
LACUNARITY_RANGE = (0.0, 5.0)
