from random import randint, uniform
import sys

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu
from pygame_gui.elements.ui_horizontal_slider import UIHorizontalSlider
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine

from constants import *
import core


# --------------------------------------------------------------------------- #

pygame.init()
screen = pygame.display.set_mode((750, 500))
pygame.display.set_caption("Noise Visualizer")
clock = pygame.time.Clock()
running = True

apply_color = APPLY_COLOR
use_falloff = USE_FALLOFF
map_surf = pygame.Surface((500, 500))

# --------------------------------------------------------------------------- #

ui_manager = UIManager((750, 500))

panel = UIPanel(
    relative_rect=pygame.Rect((MAP_SIZE, 0, *PANEL_SIZE)),
    manager=ui_manager,
    starting_layer_height=0,
    margins={
        "left": 5,
        "right": 5,
        "top": 5,
        "bottom": 5
    }
)

UILabel(
    relative_rect=pygame.Rect((0, 0, 240, 27)),
    manager=ui_manager,
    container=panel,
    text="Map type"
)

map_type_menu = UIDropDownMenu(
    relative_rect=pygame.Rect((0, 27*1, 240, 27)),
    manager=ui_manager,
    container=panel,
    options_list=MAP_OPTIONS,
    starting_option=MAP_OPTIONS[0]
)

UILabel(
    relative_rect=pygame.Rect((0, 27*2, 120, 27)),
    manager=ui_manager,
    container=panel,
    text="Tile Size"
)

tile_size_entry = UITextEntryLine(
    relative_rect=pygame.Rect((0, 27*3, 120, 27)),
    manager=ui_manager,
    container=panel
)
tile_size_entry.set_text(str(TILE_SIZE))
tile_size_entry.set_allowed_characters("numbers")

UILabel(
    relative_rect=pygame.Rect((120, 27*2, 120, 27)),
    manager=ui_manager,
    container=panel,
    text="Seed"
)

seed_entry = UITextEntryLine(
    relative_rect=pygame.Rect((120, 27*3, 120, 27)),
    manager=ui_manager,
    container=panel
)
seed_entry.set_text(str(SEED))
seed_entry.set_allowed_characters("numbers")

UILabel(
    relative_rect=pygame.Rect((0, 27*4, 120, 27)),
    manager=ui_manager,
    container=panel,
    text="Apply Colors"
)

apply_color_button = UIButton(
    relative_rect=pygame.Rect((120, 27*4, 120, 27)),
    manager=ui_manager,
    container=panel,
    text=str(apply_color)
)

UILabel(
    relative_rect=pygame.Rect((0, 27*5, 120, 27)),
    manager=ui_manager,
    container=panel,
    text="Falloff Map"
)

use_falloff_button = UIButton(
    relative_rect=pygame.Rect((120, 27*5, 120, 27)),
    manager=ui_manager,
    container=panel,
    text=str(use_falloff)
)

UILabel(
    relative_rect=pygame.Rect((0, 27*6, 120, 27)),
    manager=ui_manager,
    container=panel,
    text="Scale"
)

scale_entry = UITextEntryLine(
    relative_rect=pygame.Rect((120, 27*6, 120, 27)),
    manager=ui_manager,
    container=panel
)
scale_entry.set_text(str(SCALE))

scale_slider = UIHorizontalSlider(
    relative_rect=pygame.Rect((0, 27*7, 240, 27)),
    manager=ui_manager,
    container=panel,
    start_value=SCALE,
    value_range=SCALE_RANGE
)

UILabel(
    relative_rect=pygame.Rect((0, 27*8, 120, 27)),
    manager=ui_manager,
    container=panel,
    text="Octaves"
)

octaves_entry = UITextEntryLine(
    relative_rect=pygame.Rect((120, 27*8, 120, 27)),
    manager=ui_manager,
    container=panel
)
octaves_entry.set_text(str(OCTAVES))
octaves_entry.set_allowed_characters("numbers")

octaves_slider = UIHorizontalSlider(
    relative_rect=pygame.Rect((0, 27*9, 240, 27)),
    manager=ui_manager,
    container=panel,
    start_value=OCTAVES,
    value_range=OCTAVES_RANGE
)

UILabel(
    relative_rect=pygame.Rect((0, 27*10, 120, 27)),
    manager=ui_manager,
    container=panel,
    text="Persistence"
)

persistence_entry = UITextEntryLine(
    relative_rect=pygame.Rect((120, 27*10, 120, 27)),
    manager=ui_manager,
    container=panel
)
persistence_entry.set_text(str(PERSISTENCE))

persistence_slider = UIHorizontalSlider(
    relative_rect=pygame.Rect((0, 27*11, 240, 27)),
    manager=ui_manager,
    container=panel,
    start_value=PERSISTENCE,
    value_range=PERSISTENCE_RANGE
)

UILabel(
    relative_rect=pygame.Rect((0, 27*12, 120, 27)),
    manager=ui_manager,
    container=panel,
    text="Lacunarity"
)

lacunarity_entry = UITextEntryLine(
    relative_rect=pygame.Rect((120, 27*12, 120, 27)),
    manager=ui_manager,
    container=panel
)
lacunarity_entry.set_text(str(LACUNARITY))

lacunarity_slider = UIHorizontalSlider(
    relative_rect=pygame.Rect((0, 27*13, 240, 27)),
    manager=ui_manager,
    container=panel,
    start_value=LACUNARITY,
    value_range=LACUNARITY_RANGE
)

generate_rand_button = UIButton(
    relative_rect=pygame.Rect((60, 27*14, 120, 27)),
    manager=ui_manager,
    container=panel,
    text="Random"
)

# --------------------------------------------------------------------------- #

def regenerate_map():
    global apply_color
    global use_falloff

    map_type = map_type_menu.selected_option
    tile_size = int(tile_size_entry.get_text())
    seed = int(seed_entry.get_text())

    scale = int(scale_entry.get_text())
    octaves = int(octaves_entry.get_text())
    persistence = float(persistence_entry.get_text())
    lacunarity = float(lacunarity_entry.get_text())

    if map_type == "Random Noise Map":
        noise_map = core.random_noise(500//tile_size, seed)
        use_falloff_button.enable()
        scale_entry.disable()
        scale_slider.disable()
        octaves_entry.disable()
        octaves_slider.disable()
        persistence_entry.disable()
        persistence_slider.disable()
        lacunarity_entry.disable()
        lacunarity_slider.disable()
    elif map_type == "Perlin Noise Map":
        noise_map = core.perlin_noise(500//tile_size, seed, scale, octaves, persistence, lacunarity)
        use_falloff_button.enable()
        scale_entry.enable()
        scale_slider.enable()
        octaves_entry.enable()
        octaves_slider.enable()
        persistence_entry.enable()
        persistence_slider.enable()
        lacunarity_entry.enable()
        lacunarity_slider.enable()
    elif map_type == "Simplex Noise Map":
        noise_map = core.simplex_noise(500//tile_size, seed, scale, octaves, persistence, lacunarity)
        use_falloff_button.enable()
        scale_entry.enable()
        scale_slider.enable()
        octaves_entry.enable()
        octaves_slider.enable()
        persistence_entry.enable()
        persistence_slider.enable()
        lacunarity_entry.enable()
        lacunarity_slider.enable()
    elif map_type == "Falloff Map":
        noise_map = core.generate_falloff_map(500//tile_size)
        use_falloff_button.disable()
        scale_entry.disable()
        scale_slider.disable()
        octaves_entry.disable()
        octaves_slider.disable()
        persistence_entry.disable()
        persistence_slider.disable()
        lacunarity_entry.disable()
        lacunarity_slider.disable()

    map_size = len(noise_map)
    if use_falloff and map_type != "Falloff Map":
        falloff_map = core.generate_falloff_map(map_size)
        for x in range(map_size):
            for y in range(map_size):
                noise_map[x][y] = max(0, min(noise_map[x][y] - falloff_map[x][y], 1))
    if apply_color:
        color_map = core.generate_color_map(noise_map, REGION_COLORS)
        for x in range(map_size):
            for y in range(map_size):
                color = color_map[x][y]
                map_surf.fill(color, ((x*tile_size, y*tile_size), (tile_size, tile_size)))
    else:
        for x in range(map_size):
            for y in range(map_size):
                color = BLACK.lerp(WHITE, noise_map[x][y])
                map_surf.fill(color, ((x*tile_size, y*tile_size), (tile_size, tile_size)))


def randomize():
    map_type = map_type_menu.selected_option
    if map_type != "Falloff Map":
        seed_entry.set_text(str(randint(*SEED_RANGE)))
        if map_type != "Random Noise Map":
            scale_entry.set_text(str(randint(*SCALE_RANGE)))
            octaves_entry.set_text(str(randint(*OCTAVES_RANGE)))
            persistence_entry.set_text(str(uniform(*PERSISTENCE_RANGE)))
            lacunarity_entry.set_text(str(uniform(*LACUNARITY_RANGE)))

# --------------------------------------------------------------------------- #

regenerate_map()

while running:
    ui_manager.draw_ui(screen)
    screen.blit(map_surf, (0, 0))

    for event in pygame.event.get():
        ui_manager.process_events(event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if (event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED or event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED):
                regenerate_map()
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == scale_slider:
                    scale_entry.set_text(str(scale_slider.get_current_value()))
                elif event.ui_element == octaves_slider:
                    octaves_entry.set_text(str(octaves_slider.get_current_value()))
                elif event.ui_element == persistence_slider:
                    persistence_entry.set_text(str(persistence_slider.get_current_value()))
                elif event.ui_element == lacunarity_slider:
                    lacunarity_entry.set_text(str(lacunarity_slider.get_current_value()))

                regenerate_map()
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == apply_color_button:
                    if apply_color:
                        apply_color = False
                        apply_color_button.set_text(str(False))
                    else:
                        apply_color = True
                        apply_color_button.set_text(str(True))
                elif event.ui_element == use_falloff_button:
                    if use_falloff:
                        use_falloff = False
                        use_falloff_button.set_text(str(False))
                    else:
                        use_falloff = True
                        use_falloff_button.set_text(str(True))
                elif event.ui_element == generate_rand_button:
                    randomize()

                regenerate_map()

    time_delta = clock.tick(60) / 1000.0
    ui_manager.update(time_delta)
    pygame.display.update()
