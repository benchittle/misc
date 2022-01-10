"""
Date: April 10, 2020
Version: 0.3.4
Added:
    >PlayerMenu.is_hidden
    >additional parameters to PlayerMenu
    >PlayerMenu.add_button
    >Button

Removed:

Changed:
    >'Hotbar' -> PlayerMenu
    >PlayerMenu now inherits from pygame.sprite.Sprite

"""
import pygame as pg
import config

## DIRTY SPRITES??
class PlayerMenu(pg.sprite.Sprite):
    def __init__(self, game, pos, anchor, num_buttons, align):
        super().__init__()
        self.game = game
        self.game.menus.add(self)

        self.image = pg.Surface(config.HOTBAR_SIZE)
        self.rect = self.image.get_rect()
        setattr(self.rect, anchor, pos)
        ## SIZE NEEDS TO ADJUSTABLE
        self.image.fill(config.WHITE)
        self.image.fill(config.BLACK, (0, 4, self.rect.w - 4, self.rect.h - 8))

        self.align = align
        if self.align == "vertical":
            self.button_size = (self.rect.w, self.rect.h / num_buttons)
        elif self.align == "horizontal":
            self.button_size = self.rect.w / num_buttons, self.rect.h

        self.buttons = []
        self.is_hidden = False


    def update(self):
        pass


    @property
    def is_hidden(self):
        return self._is_hidden


    @is_hidden.setter
    def is_hidden(self, value):
        self._is_hidden = value
        if self.is_hidden:
            self.game.menus.remove(self)
        else:
            self.game.menus.add(self)
            self.update()  ##


    def add_button(self, index, image, text, event):
        if self.align == "vertical":
            pos = rect.x, rect.y + self.button_size * index
        elif self.align == "horizontal":
            pos = rect.x + self.button_size * index, rect.y

        rect = pg.Rect(pos, self.button_size)


class Button(pg.sprite.Sprite):
    def __init__(self, parent, rect, surface):
        super().__init__()
        self.game = parent.game
        self.parent = parent
        self.rect = pg.Rect(rect)
        self.surface = surface


















def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()