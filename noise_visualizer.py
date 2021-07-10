import sys

import pygame
import pygame_gui
from pygame_gui import UIManager
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
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.display = pygame.Surface(SCREEN_SIZE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.on_init_gui()

        self.map_surf = pygame.Surface((MAP_SIZE, MAP_SIZE))
        self.regenerate_map()


    def on_init_gui(self):
        self.ui_manager = UIManager(SCREEN_SIZE)

        panel = UIPanel(
            relative_rect=pygame.Rect((MAP_SIZE, 0, *PANEL_SIZE)),
            manager=self.ui_manager,
            starting_layer_height=0,
            margins={
                "left": MARGIN,
                "right": MARGIN,
                "top": MARGIN,
                "bottom": MARGIN
            }
        )

        UILabel(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*0, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            text="Map type"
        )

        self.map_type_menu = UIDropDownMenu(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*1, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            options_list=MAP_OPTIONS,
            starting_option=MAP_OPTIONS[0]
        )

        UILabel(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*2, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            text="Tile Size"
        )

        self.tile_size_entry = UITextEntryLine(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*3, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel
        )
        self.tile_size_entry.set_text(str(TILE_SIZE))
        self.tile_size_entry.set_allowed_characters("numbers")

        UILabel(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*4, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            text="Seed"
        )

        self.seed_entry = UITextEntryLine(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*5, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel
        )
        self.seed_entry.set_text(str(SEED))
        self.seed_entry.set_allowed_characters("numbers")

        UILabel(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*6, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            text="Scale"
        )

        self.scale_entry = UITextEntryLine(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*7, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel
        )
        self.scale_entry.set_text(str(SCALE))

        self.scale_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*8, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            start_value=SCALE,
            value_range=(2, 50)
        )

        UILabel(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*9, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            text="Octaves"
        )

        self.octaves_entry = UITextEntryLine(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*10, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel
        )
        self.octaves_entry.set_text(str(OCTAVES))
        self.octaves_entry.set_allowed_characters("numbers")

        self.octaves_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*11, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            start_value=OCTAVES,
            value_range=(1, 10)
        )

        UILabel(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*12, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            text="Persistence"
        )

        self.persistence_entry = UITextEntryLine(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*13, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel
        )
        self.persistence_entry.set_text(str(PERSISTENCE))

        self.persistence_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*14, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            start_value=PERSISTENCE,
            value_range=(0, 5)
        )

        UILabel(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*15, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            text="Lacunarity"
        )

        self.lacunarity_entry = UITextEntryLine(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*16, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel
        )
        self.lacunarity_entry.set_text(str(LACUNARITY))

        self.lacunarity_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*17, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            start_value=LACUNARITY,
            value_range=(0, 5)
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
        time_delta = self.clock.tick(FPS) / 1000.0
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

        scale = int(self.scale_entry.get_text())
        octaves = int(self.octaves_entry.get_text())
        persistence = float(self.persistence_entry.get_text())
        lacunarity = float(self.lacunarity_entry.get_text())

        if map_type == "Random Noise Map":
            noise_map = core.random_noise(MAP_SIZE//tile_size, seed)
            self.scale_entry.disable()
            self.scale_slider.disable()
            self.octaves_entry.disable()
            self.octaves_slider.disable()
            self.persistence_entry.disable()
            self.persistence_slider.disable()
            self.lacunarity_entry.disable()
            self.lacunarity_slider.disable()
        elif map_type == "Perlin Noise Map":
            noise_map = core.perlin_noise(MAP_SIZE//tile_size, seed, scale, octaves, persistence, lacunarity)
            self.scale_entry.enable()
            self.scale_slider.enable()
            self.octaves_entry.enable()
            self.octaves_slider.enable()
            self.persistence_entry.enable()
            self.persistence_slider.enable()
            self.lacunarity_entry.enable()
            self.lacunarity_slider.enable()

        for x in range(len(noise_map)):
            for y in range(len(noise_map)):
                color = BLACK.lerp(WHITE, noise_map[x][y])
                self.map_surf.fill(color, ((x*tile_size, y*tile_size), (tile_size, tile_size)))


if __name__ == '__main__':
    Main().on_run()
