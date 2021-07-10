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

        self.tiles = pygame.sprite.Group()
        self.regenerate_map()


    def on_init_gui(self):
        self.ui_manager = UIManager(SCREEN_SIZE)

        panel = UIPanel(
            relative_rect=pygame.Rect((500, 0, *PANEL_SIZE)),
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
        self.scale_entry.set_allowed_characters("numbers")

        self.scale_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect((0, ELEMENT_HEIGHT*8, PANEL_SIZE[0] - MARGIN*2, ELEMENT_HEIGHT)),
            manager=self.ui_manager,
            container=panel,
            start_value=SCALE,
            value_range=(1, 50)
        )


    def on_quit(self):
        pygame.quit()
        sys.exit()


    def on_render(self):
        self.tiles.draw(self.display)
        self.ui_manager.draw_ui(self.display)
        self.screen.blit(self.display, (0, 0))
        pygame.display.update()


    def on_loop(self):
        time_delta = self.clock.tick(FPS) / 1000.0
        self.tiles.update()
        self.ui_manager.update(time_delta)


    def on_event(self, event):
        self.ui_manager.process_events(event)
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.USEREVENT:
            if (
                event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED or
                event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED
            ):
                self.regenerate_map()
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                self.scale_entry.set_text(str(self.scale_slider.get_current_value()))
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
        self.tiles.empty()

        map_type = self.map_type_menu.selected_option
        tile_size = int(self.tile_size_entry.get_text())
        seed = int(self.seed_entry.get_text())

        scale = int(self.scale_entry.get_text())

        if map_type == "Random Noise Map":
            noise_map = core.random_noise(MAP_SIZE//tile_size, seed)
        elif map_type == "Perlin Noise Map":
            noise_map = core.perlin_noise(MAP_SIZE//tile_size, seed, scale)

        for x in range(len(noise_map)):
            for y in range(len(noise_map)):
                color = BLACK.lerp(WHITE, noise_map[x][y])
                tile = core.Tile(x*tile_size, y*tile_size, tile_size, color=color)
                self.tiles.add(tile)


if __name__ == '__main__':
    #m = generate_noise_map(5, 69, 2)
    #print(m)
    Main().on_run()
