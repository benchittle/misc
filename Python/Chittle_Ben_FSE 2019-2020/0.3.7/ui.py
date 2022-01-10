"""
Date: April 24, 2020
Version: 0.3.7
Added:
    Button.set_image
    Button.set_empty

Removed:

Changed:

"""
import collections
import pygame as pg
import config


class Menu:
    pass

## DIRTY SPRITES??
## COLLAPSIBILITY?
class InventoryMenu(pg.sprite.Sprite):
    BORDER = 4
    def __init__(self, lvldata, pos, anchor):
        super().__init__()
        self.lvldata = lvldata
        self.lvldata.menus.add(self)

        self.image_base = pg.Surface(config.HOTBAR_SIZE)
        self.rect = self.image_base.get_rect()
        setattr(self.rect, anchor, pos)
        self.image_base.fill(config.WHITE)
        self.image_base.fill(
            config.BLACK,
            (self.BORDER, self.BORDER, self.rect.w - 2 * self.BORDER, self.rect.h - 2 * self.BORDER))
        self.image = self.image_base.copy()
        ## SIZE NEEDS TO ADJUSTABLE
        self.button_size = (self.rect.w - 2 * self.BORDER, (self.rect.h - 2 * self.BORDER) // config.INV_SIZE)

        self.buttons = [None] * config.INV_SIZE
        for index in range(config.INV_SIZE):
            self.add_button(index)

        self._active = None
        self.is_hidden = False


    def update(self):
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                self.active = button
                clicks = pg.mouse.get_pressed()
                if clicks[0]:
                    self.lvldata.player.equipped_item = button.index
                elif clicks[2]:
                    self.lvldata.player.drop_item(button.index)
                break
        else:
            self.active = None


    def draw(self):
        self.image = self.image_base.copy()
        images = [(button.image, button.rel_pos) for button in self.buttons]
        self.image.blits(images, doreturn=0)


    @property
    def active(self):
        return self._active


    @active.setter
    def active(self, button):
        if button is None:
            self._active = None
            self.draw()
        elif button is not self.active:
            self.draw()
            self._active = button
            self.active.popup()


    @property
    def is_hidden(self):
        return self._is_hidden


    @is_hidden.setter
    def is_hidden(self, value):
        self._is_hidden = value
        if self.is_hidden:
            self.lvldata.menus.remove(self)
        else:
            self.lvldata.menus.add(self)
            self.update()  ##


    def add_button(self, index):
        # The position of the button relative to the menu Surface.
        rel_pos = pg.Vector2(self.BORDER + config.HOTBAR_OFFSET,
                             self.button_size[1] * index + self.BORDER + config.HOTBAR_OFFSET)
        try:
            # Assume the player has an item in the given index and use it as the
            # icon for the button.
            image = self.lvldata.player.inventory[index].image_base
        except AttributeError:
            # If the player doesn't have an item in the given index, use a
            # default grey button instead.
            image = pg.Surface(self.button_size)
            image.fill(config.BLACK)
            image.fill(config.GRAY, (0, 0, self.button_size[0], self.button_size[1]))

        # A Rect around the button with position relative to the screen.
        rect = pg.Rect(rel_pos + self.rect.topleft, self.button_size)
        self.image.blit(image, rel_pos)
        self.buttons[index] = Button(self, rect, image, rel_pos, index)


class Button:
    def __init__(self, menu, rect, image, rel_pos, index):
        self.menu = menu
        self.rect = rect
        self.rel_pos = rel_pos
        self.index = index
        self.image_def = pg.transform.scale(
            image,
            (self.rect.w - config.HOTBAR_OFFSET * 2, self.rect.h - config.HOTBAR_OFFSET * 2))
        self.image_pop = pg.transform.scale(self.image_def, (self.rect.w, self.rect.h))
        self.image = self.image_def ##simplify??


    def set_image(self, image):
        self.image_def = pg.transform.scale(
            image,
            (self.rect.w - config.HOTBAR_OFFSET * 2, self.rect.h - config.HOTBAR_OFFSET * 2))
        self.image_pop = pg.transform.scale(self.image_def, (self.rect.w, self.rect.h))
        self.image = self.image_def
        self.menu.draw()


    def set_empty(self):
        image = pg.Surface(self.rect.size)
        image.fill(config.BLACK)
        image.fill(config.GRAY, (0, 0, self.rect.w, self.rect.h))
        self.set_image(image)



    def popup(self):
        self.menu.image.blit(self.image_pop, self.rel_pos - (4, 4))



def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()