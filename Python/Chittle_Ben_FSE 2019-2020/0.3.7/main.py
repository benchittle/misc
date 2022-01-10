"""
Date: April 24, 2020
Version: 0.3.7
Added:
    >GameData
    >LevelData

Removed:
    >Game

Changed:
    >Game was split into 2 smaller classes; its methods are now functions in
        this file
        >Since only certain data, like the player and ship, needed to be
         accessible in the 'Game' class, it seemed more efficient to simply
         make it more of a data storage class.

"""

# Pausing and shot cooldowns need to be resolved -> the cooldowns work off of
# the game clock which runs while paused -> need to to run off a seperate clock
# that also pauses when the game is paused


# Only sprites on the screen need to be updated every frame, others only need to
# render / update when they near the screen (this is probably what causes lag
# with large numbers of Tiles despite other optimizations)
# > Fixing this... those tiles do need to updated for things like projectiles...


# Projectiles can escape when the player moves, I believe this is because the
# position of the projectile and the positions of the walls update in such a
# way that collision is being checked on previous / false positions of the walls


import random
import pygame as pg
import config, environment, levelgen, player, sprites, ui


pg.init() # Try without other inits
pg.font.init()

class GameData:
    def __init__(self):
        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption(config.TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False
        self.debug_font = pg.font.SysFont("Courier", 20) ##TEMP?


class LevelData:
    def __init__(self):
        self.screen_pos = pg.Vector2(0, 0)
        self.screen_rect = pg.Rect(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        self.all_sprites = pg.sprite.LayeredUpdates(default_layer=config.SPRITE_LAYER)
        self.menus = pg.sprite.Group()
        self.projectiles = pg.sprite.Group() ##TEMP
        self.ground_items = pg.sprite.Group()

        self.ship = levelgen.Ship(self, (0, 0), 8, 15)
        self.start_pos = self.ship.grid.find_by_tags("start")[0].rect.center
        self.player = player.Player(lvldata=self, ship=self.ship, pos=self.start_pos)

        self.inv_menu = ui.InventoryMenu(self, (0, config.SCREEN_HEIGHT / 2), "midleft")
        self.menus.add(self.inv_menu)



def debug(game, lvldata):
    debug1 = game.debug_font.render(
        "Speed: {:.2f} || Velx: {:.2f} || Vely: {:.2f} || Proj: {}".format(
            lvldata.player.vel.magnitude(), lvldata.player.vel.x, lvldata.player.vel.y, len(lvldata.projectiles)
            ),
        False,
        config.WHITE
    )
    game.screen.blit(debug1, (10, 10))

    debug2 = game.debug_font.render(
        "Time: {} || FPS: {:.0f}".format(
            pg.time.get_ticks(), game.clock.get_fps()
            ),
        False,
        config.WHITE
    )
    game.screen.blit(debug2, (10, 30))

    pos_text = game.debug_font.render(
        "x: {:.0f}, y: {:.0f}".format(
            lvldata.screen_pos.x + config.SCREEN_WIDTH / 2, lvldata.screen_pos.y + config.SCREEN_HEIGHT / 2
            ),
        False,
        config.WHITE)
    game.screen.blit(pos_text, (config.SCREEN_WIDTH - 200, config.SCREEN_HEIGHT - 25))


game = GameData()
lvldata = LevelData()

sprites.HandBlaster(lvldata, lvldata.start_pos, colour=config.BLUE)

while game.running:
    # Unpaused event loop
    if not game.paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    game.running = False
                if event.key == pg.K_SPACE:
                    game.paused = True
                    pg.event.set_grab(False)
                    print("PAUSED")

                # Toggle noclip for the player.
                if event.key == pg.K_z:
                    lvldata.player.noclip = lvldata.player.noclip == False
                    print("Player Noclip: {}".format(lvldata.player.noclip))
                # Toggle noclip for Projectiles.
                #if event.key == pg.K_x:
                    #sprites.BlasterShot.noclip = sprites.BlasterShot.noclip == False
                    #print("Projectile Noclip: {}".format(sprites.BlasterShot.noclip))
                if event.key == pg.K_r:
                    lvldata.screen_pos.update(pg.Vector2(lvldata.start_pos) - config.SCREEN_MID)
                    for sprite in lvldata.projectiles:
                        sprite.kill()
                    print("RESET")
                # Toggles the visibility of the player's inventory.
                if event.key == pg.K_TAB:
                    lvldata.inv_menu.is_hidden = lvldata.inv_menu.is_hidden == False
                # Try to pick up a nearby item.
                if event.key == pg.K_e:
                    lvldata.player.pickup_item()

        lvldata.player.update()
        lvldata.ship.update()
        lvldata.all_sprites.update()

    # Paused event loop
    else:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    game.running = False
                if event.key == pg.K_SPACE:
                    game.paused = False
                    pg.event.set_grab(True)
                    lvldata.inv_menu.active = None ## TEMP?
                    print("UNPAUSED")

                # Toggles the visibility of the player's inventory.
                if event.key == pg.K_TAB:
                    lvldata.inv_menu.is_hidden = lvldata.inv_menu.is_hidden == False
                if event.key == pg.K_e:
                    lvldata.player.pickup_item()

        # Only make the menu interactable when paused. Checks first to make
        # sure the game wasn't unpaused in the event loop.
        if game.paused:
            lvldata.menus.update()

    game.screen.fill(config.BLACK)
    lvldata.all_sprites.draw(game.screen)
    game.screen.blit(lvldata.player.image, lvldata.player.rect)
    lvldata.menus.draw(game.screen)
    debug(game, lvldata)

    pg.display.update(lvldata.screen_rect)

    game.clock.tick_busy_loop(config.FPS)

pg.quit()
print("Donezo!")