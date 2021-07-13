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


class Main:
    def __init__(self):
        self.running = True


    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((750, 500))
        self.display = pygame.Surface((750, 500))
        pygame.display.set_caption("Noise Visualizer")
        self.clock = pygame.time.Clock()

        self.apply_color = APPLY_COLOR
        self.use_falloff = USE_FALLOFF
        self.on_init_gui()
        self.map_surf = pygame.Surface((MAP_SIZE, MAP_SIZE))
        self.regenerate_map()


    def on_init_gui(self):
        self.ui_manager = UIManager((750, 500))

        panel = UIPanel(
            relative_rect=pygame.Rect((MAP_SIZE, 0, *PANEL_SIZE)),
            manager=self.ui_manager,
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
            manager=self.ui_manager,
            container=panel,
            text="Map type"
        )

        self.map_type_menu = UIDropDownMenu(
            relative_rect=pygame.Rect((0, 27*1, 240, 27)),
            manager=self.ui_manager,
            container=panel,
            options_list=MAP_OPTIONS,
            starting_option=MAP_OPTIONS[0]
        )

        UILabel(
            relative_rect=pygame.Rect((0, 27*2, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text="Tile Size"
        )

        self.tile_size_entry = UITextEntryLine(
            relative_rect=pygame.Rect((0, 27*3, 120, 27)),
            manager=self.ui_manager,
            container=panel
        )
        self.tile_size_entry.set_text(str(TILE_SIZE))
        self.tile_size_entry.set_allowed_characters("numbers")

        UILabel(
            relative_rect=pygame.Rect((120, 27*2, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text="Seed"
        )

        self.seed_entry = UITextEntryLine(
            relative_rect=pygame.Rect((120, 27*3, 120, 27)),
            manager=self.ui_manager,
            container=panel
        )
        self.seed_entry.set_text(str(SEED))
        self.seed_entry.set_allowed_characters("numbers")

        UILabel(
            relative_rect=pygame.Rect((0, 27*4, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text="Apply Colors"
        )

        self.apply_color_button = UIButton(
            relative_rect=pygame.Rect((120, 27*4, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text=str(self.apply_color)
        )

        UILabel(
            relative_rect=pygame.Rect((0, 27*5, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text="Falloff Map"
        )

        self.use_falloff_button = UIButton(
            relative_rect=pygame.Rect((120, 27*5, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text=str(self.use_falloff)
        )

        UILabel(
            relative_rect=pygame.Rect((0, 27*6, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text="Scale"
        )

        self.scale_entry = UITextEntryLine(
            relative_rect=pygame.Rect((120, 27*6, 120, 27)),
            manager=self.ui_manager,
            container=panel
        )
        self.scale_entry.set_text(str(SCALE))

        self.scale_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect((0, 27*7, 240, 27)),
            manager=self.ui_manager,
            container=panel,
            start_value=SCALE,
            value_range=SCALE_RANGE
        )

        UILabel(
            relative_rect=pygame.Rect((0, 27*8, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text="Octaves"
        )

        self.octaves_entry = UITextEntryLine(
            relative_rect=pygame.Rect((120, 27*8, 120, 27)),
            manager=self.ui_manager,
            container=panel
        )
        self.octaves_entry.set_text(str(OCTAVES))
        self.octaves_entry.set_allowed_characters("numbers")

        self.octaves_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect((0, 27*9, 240, 27)),
            manager=self.ui_manager,
            container=panel,
            start_value=OCTAVES,
            value_range=OCTAVES_RANGE
        )

        UILabel(
            relative_rect=pygame.Rect((0, 27*10, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text="Persistence"
        )

        self.persistence_entry = UITextEntryLine(
            relative_rect=pygame.Rect((120, 27*10, 120, 27)),
            manager=self.ui_manager,
            container=panel
        )
        self.persistence_entry.set_text(str(PERSISTENCE))

        self.persistence_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect((0, 27*11, 240, 27)),
            manager=self.ui_manager,
            container=panel,
            start_value=PERSISTENCE,
            value_range=PERSISTENCE_RANGE
        )

        UILabel(
            relative_rect=pygame.Rect((0, 27*12, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text="Lacunarity"
        )

        self.lacunarity_entry = UITextEntryLine(
            relative_rect=pygame.Rect((120, 27*12, 120, 27)),
            manager=self.ui_manager,
            container=panel
        )
        self.lacunarity_entry.set_text(str(LACUNARITY))

        self.lacunarity_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect((0, 27*13, 240, 27)),
            manager=self.ui_manager,
            container=panel,
            start_value=LACUNARITY,
            value_range=LACUNARITY_RANGE
        )

        self.generate_rand_button = UIButton(
            relative_rect=pygame.Rect((60, 27*14, 120, 27)),
            manager=self.ui_manager,
            container=panel,
            text="Random"
        )


    def on_quit(self):
        pygame.quit()
        sys.exit()


    def on_render(self):
        self.ui_manager.draw_ui(self.display)
        self.display.blit(self.map_surf, (0, 0))
        self.screen.blit(self.display, (0, 0))
        pygame.display.update()


    def on_loop(self):
        time_delta = self.clock.tick(60) / 1000.0
        self.ui_manager.update(time_delta)


    def on_event(self, event):
        self.ui_manager.process_events(event)
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.USEREVENT:
            if (event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED or
                event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED):
                self.regenerate_map()
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.scale_slider:
                    self.scale_entry.set_text(str(self.scale_slider.get_current_value()))
                elif event.ui_element == self.octaves_slider:
                    self.octaves_entry.set_text(str(self.octaves_slider.get_current_value()))
                elif event.ui_element == self.persistence_slider:
                    self.persistence_entry.set_text(str(self.persistence_slider.get_current_value()))
                elif event.ui_element == self.lacunarity_slider:
                    self.lacunarity_entry.set_text(str(self.lacunarity_slider.get_current_value()))

                self.regenerate_map()
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.apply_color_button:
                    if self.apply_color:
                        self.apply_color = False
                        self.apply_color_button.set_text(str(False))
                    else:
                        self.apply_color = True
                        self.apply_color_button.set_text(str(True))
                elif event.ui_element == self.use_falloff_button:
                    if self.use_falloff:
                        self.use_falloff = False
                        self.use_falloff_button.set_text(str(False))
                    else:
                        self.use_falloff = True
                        self.use_falloff_button.set_text(str(True))
                elif event.ui_element == self.generate_rand_button:
                    self.randomize()

                self.regenerate_map()


    def on_run(self):
        if self.on_init() == False:
            self.running = False

        while self.running:
            self.on_render()
            self.on_loop()

            for event in pygame.event.get():
                self.on_event(event)

        self.on_quit()


    def regenerate_map(self):
        map_type = self.map_type_menu.selected_option
        tile_size = int(self.tile_size_entry.get_text())
        seed = int(self.seed_entry.get_text())
        apply_color = self.apply_color
        use_falloff = self.use_falloff

        scale = int(self.scale_entry.get_text())
        octaves = int(self.octaves_entry.get_text())
        persistence = float(self.persistence_entry.get_text())
        lacunarity = float(self.lacunarity_entry.get_text())

        if map_type == "Random Noise Map":
            noise_map = core.random_noise(500//tile_size, seed)
            self.use_falloff_button.enable()
            self.disable_noise_widgets()
        elif map_type == "Perlin Noise Map":
            noise_map = core.perlin_noise(500//tile_size, seed, scale, octaves, persistence, lacunarity)
            self.use_falloff_button.enable()
            self.enable_noise_widgets()
        elif map_type == "Simplex Noise Map":
            noise_map = core.simplex_noise(500//tile_size, seed, scale, octaves, persistence, lacunarity)
            self.use_falloff_button.enable()
            self.enable_noise_widgets()
        elif map_type == "Falloff Map":
            noise_map = core.generate_falloff_map(500//tile_size)
            self.use_falloff_button.disable()
            self.disable_noise_widgets()

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
                    self.map_surf.fill(color, ((x*tile_size, y*tile_size), (tile_size, tile_size)))
        else:
            for x in range(map_size):
                for y in range(map_size):
                    color = BLACK.lerp(WHITE, noise_map[x][y])
                    self.map_surf.fill(color, ((x*tile_size, y*tile_size), (tile_size, tile_size)))


    def randomize(self):
        map_type = self.map_type_menu.selected_option
        if map_type != "Falloff Map":
            self.seed_entry.set_text(str(randint(*SEED_RANGE)))
            if map_type != "Random Noise Map":
                self.scale_entry.set_text(str(randint(*SCALE_RANGE)))
                self.octaves_entry.set_text(str(randint(*OCTAVES_RANGE)))
                self.persistence_entry.set_text(str(uniform(*PERSISTENCE_RANGE)))
                self.lacunarity_entry.set_text(str(uniform(*LACUNARITY_RANGE)))


    def enable_noise_widgets(self):
        self.scale_entry.enable()
        self.scale_slider.enable()
        self.octaves_entry.enable()
        self.octaves_slider.enable()
        self.persistence_entry.enable()
        self.persistence_slider.enable()
        self.lacunarity_entry.enable()
        self.lacunarity_slider.enable()


    def disable_noise_widgets(self):
        self.scale_entry.disable()
        self.scale_slider.disable()
        self.octaves_entry.disable()
        self.octaves_slider.disable()
        self.persistence_entry.disable()
        self.persistence_slider.disable()
        self.lacunarity_entry.disable()
        self.lacunarity_slider.disable()


if __name__ == '__main__':
    Main().on_run()
