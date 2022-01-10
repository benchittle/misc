"""
Date: April 9, 2020
Version: 0.3.3
>Added this module:

"""
import pygame as pg
import config


class Hotbar:
    def __init__(self, game):
        self.game = game

        self.image = pg.Surface(config.HOTBAR_SIZE)
        self.rect = self.image.get_rect(midleft=(0, config.SCREEN_HEIGHT / 2))
        self.image.fill(config.WHITE)
        self.image.fill(config.BLACK, (0, 4, self.rect.w - 4, self.rect.h - 8))

    def update(self):
        pass













def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()