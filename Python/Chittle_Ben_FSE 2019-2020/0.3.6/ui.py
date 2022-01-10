"""
Date: April 23, 2020
Version: 0.3.6
Added:
    >InventoryMenu.draw
    >InventoryMeny.active
    >Button

Removed:
    >'num_buttons', 'align' parameters in InventoryMenu

Changed:
    >PlayerMenu.add_button - refactored so that this class is designed
        specifically for interacting with the player's inventory, not a broad /
        base menu class
        - changed required arguments
        - uses button classes in a single list rather than related lists
    >'PlayerMenu' -> 'InventoryMenu'
    >InventoryMenu.update - interacts with player's inventory to set the
        player's currently equipped item to the clicked item
        - implemented popop effect when hovering over buttons


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
    def __init__(self, game, pos, anchor):
        super().__init__()
        self.game = game
        self.game.menus.add(self)

        self.image_base = pg.Surface(config.HOTBAR_SIZE)
        self.rect = self.image_base.get_rect()
        setattr(self.rect, anchor, pos)
        self.image_base.fill(config.WHITE)
        self.image_base.fill(config.BLACK, (self.BORDER, self.BORDER, self.rect.w - 2 * self.BORDER, self.rect.h - 2 * self.BORDER))
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
                if pg.mouse.get_pressed()[0]:
                    self.game.player.equipped_item = button.index
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
            self.game.menus.remove(self)
        else:
            self.game.menus.add(self)
            self.update()  ##


    def add_button(self, index):
        # The position of the button relative to the menu Surface.
        rel_pos = pg.Vector2(self.BORDER, self.button_size[1] * index + self.BORDER)

        try:
            # Assume the player has an item in the given index and use it as the
            # icon for the button.
            image = pg.transform.scale(self.game.player.inventory[index].image_base, self.button_size)
        except AttributeError:
            # If the player doesn't have an item in the given index, use a
            # default grey button instead.
            image = pg.Surface(self.button_size)
            image.fill(config.BLACK)
            image.fill(config.GRAY, (4, 4, self.button_size[0] - 8, self.button_size[1] - 8))

        # A Rect around the button with position relative to the screen.
        rect = pg.Rect(rel_pos + self.rect.topleft, self.button_size)
        self.image.blit(image, rel_pos)
        self.buttons[index] = Button(self, rect, image, rel_pos, index)


class Button:
    def __init__(self, menu, rect, image, rel_pos, index):
        self.menu = menu
        self.rect = rect
        self.image = image
        self.rel_pos = rel_pos
        self.popup_image = pg.transform.scale(self.image, (self.image.get_width() + 8, self.image.get_height() + 8))
        self.index = index


    def popup(self):
        self.menu.image.blit(self.popup_image, self.rel_pos - (4, 4))



def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()