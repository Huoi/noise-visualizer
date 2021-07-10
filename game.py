import random
import sys

import noise
import numpy as np
import pygame
import pygame_gui

from constants import *
import core


def generate_noise_map(size, seed, scale, octaves=1, persistence=0.5, lacunarity=2):
    noise_map = np.zeros((size, size), dtype=float)
    for x in range(size):
        for y in range(size):
            noise_map[x][y] = noise.pnoise3(x / scale, y / scale, seed, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            noise_map[x][y] = (noise_map[x][y] + 1) / 2

    return noise_map


class Game:
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
        for x in range(50):
            for y in range(50):
                alpha = random.random()
                color = BLACK.lerp(WHITE, alpha)
                tile = core.Tile(x*10, y*10, 10, color=color)
                self.tiles.add(tile)


    def on_init_gui(self):
        self.ui_manager = pygame_gui.UIManager((750, 500))

        frame_rect = pygame.Rect((500, 0, 250, 500))
        frame = pygame_gui.elements.ui_panel.UIPanel(frame_rect, 0, self.ui_manager)

        scroll_frame_rect = pygame.Rect((500, 0, 250, 1000))
        scroll_frame = pygame_gui.elements.ui_scrolling_container.UIScrollingContainer(scroll_frame_rect, self.ui_manager)

        scroll_rect = pygame.Rect((225, 0, 25, 500))
        scroll = pygame_gui.elements.ui_vertical_scroll_bar.UIVerticalScrollBar(scroll_rect, 0.5, self.ui_manager, scroll_frame)

        drop_rect = pygame.Rect((0, 0, 100, 50))
        drop = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(["A", "B", "C"], "A", drop_rect, self.ui_manager, scroll_frame)

        #slider_rect = pygame.Rect((500, 10, 200, 40))
        #slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(slider_rect, 1, [1, 2, 3], manager=self.ui_manager)


    def on_quit(self):
        pygame.quit()
        sys.exit()


    def on_render(self):
        self.tiles.draw(self.display)

        self.ui_manager.draw_ui(self.display)

        self.screen.blit(self.display, (0, 0))
        pygame.display.update()


    def on_loop(self):
        time_delta = self.clock.tick(FPS)
        self.tiles.update()
        self.ui_manager.update(time_delta)


    def on_event(self, event):
        self.ui_manager.process_events(event)
        if event.type == pygame.QUIT:
            self.running = False


    def on_run(self):
        if self.on_init() == False:
            self.running = False

        while self.running:
            self.on_render()
            self.on_loop()

            for event in pygame.event.get():
                self.on_event(event)

        self.on_quit()


if __name__ == '__main__':
    #m = generate_noise_map(5, 69, 2)
    #print(m)
    Game().on_run()
