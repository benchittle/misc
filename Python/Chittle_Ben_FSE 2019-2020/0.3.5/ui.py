"""
Date: April 18, 2020
Version: 0.3.5
Added:
    PlayerMenu.BORDER

Removed:
    Button

Changed:
    PlayerMenu.add_button
    PlayerMenu.update

"""
import pygame as pg
import config

## DIRTY SPRITES??
class PlayerMenu(pg.sprite.Sprite):
    BORDER = 4
    def __init__(self, game, pos, anchor, num_buttons, align):
        super().__init__()
        self.game = game
        self.game.menus.add(self)

        self.image = pg.Surface(config.HOTBAR_SIZE)
        self.rect = self.image.get_rect()
        setattr(self.rect, anchor, pos)
        ## SIZE NEEDS TO ADJUSTABLE
        self.image.fill(config.WHITE)
        self.image.fill(config.BLACK, (self.BORDER, self.BORDER, self.rect.w - 2 * self.BORDER, self.rect.h - 2 * self.BORDER))

        self.align = align
        if self.align == "vertical":
            self.button_size = (self.rect.w - 2 * self.BORDER, (self.rect.h - 2 * self.BORDER) // num_buttons)
        elif self.align == "horizontal":
            self.button_size = ((self.rect.w - 2 * self.BORDER) // num_buttons, self.rect.h - 2 * self.BORDER)

        self.buttons = [None] * num_buttons #Use sprite.Group?
        self.events = [None] * num_buttons

        self.is_hidden = False


    def update(self):
        mouse = pg.mouse.get_pos()
        for rect in self.buttons:
            if rect is not None:
                if rect.collidepoint(mouse):
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


    def add_button(self, index, icon, text, event):
        #SURFACE IS CURRENTLY JUST BENING USED AS COLOUR
        if self.align == "vertical":
            pos = pg.Vector2(self.BORDER, self.button_size[1] * index + self.BORDER)
        elif self.align == "horizontal":
            pos = pg.Vector2(self.button_size[0] * index + self.BORDER, self.BORDER)

        image = pg.transform.scale(icon, self.button_size)
        rect = pg.Rect(pos + self.rect.topleft, self.button_size)
        self.image.blit(image, pos)
        self.buttons[index] = rect
        self.events[index] = event












def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()