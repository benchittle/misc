"""
Date: April 18, 2020
Version: 0.3.5
Added:
    locks the cursor to the screen when the game is not paused (see
    Game.start_level, Game.update)

Removed:

Changed:

"""

# Pausing and shot cooldowns need to be resolved -> the cooldowns work off of
# the game clock which runs while paused -> need to to run off a seperate clock
# that also pauses when the game is paused

# Only sprites on the screen need to be updated every frame, others only need to
# render / update when they near the screen (this is probably what causes lag
# with large numbers of Tiles despite other optimizations)
# > Fixing this... those tiles do need to updated for things like projectiles...


import random
import pygame as pg
import config, environment, levelgen, sprites, ui


pg.init() # Try without other inits
pg.font.init()


class Game:

    def __init__(self):
        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption(config.TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False

        self.debug_font = pg.font.SysFont("Courier", 20)

        self.screen_pos = pg.Vector2(0, 0)
        self.screen_rect = pg.Rect(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)


    def start_level(self):
        #pg.event.set_grab(True)

        self.all_sprites = pg.sprite.LayeredUpdates(default_layer=config.SPRITE_LAYER)
        self.menus = pg.sprite.Group()

        self.projectiles = pg.sprite.Group() ##TEMP
        self.ground_items = pg.sprite.Group()

        self.ship = levelgen.Ship(self, (0, 0), 8, 15)
        self.start_pos = self.ship.grid.find_by_tags("start")[0].rect.center
        self.player = sprites.Player(game=self, ship=self.ship, pos=self.start_pos)

        self.inv_menu = ui.PlayerMenu(self, (0, config.SCREEN_HEIGHT / 2), "midleft", 9, "vertical")
        self.menus.add(self.inv_menu)
        self.inv_menu.add_button(0, self.player.equipped_item.image_base, None, None)

        sprites.HandBlaster(self, self.ship, self.start_pos, colour=config.BLUE) ##


    def update(self):
        # Unpaused event loop
        if not self.paused:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                    if event.key == pg.K_SPACE:
                        self.paused = True
                        pg.event.set_grab(False)
                        print("PAUSED")
                    ## TEMP
                    if event.key == pg.K_p:
                        pass

                    # Toggle noclip for the player.
                    if event.key == pg.K_z:
                        self.player.noclip = self.player.noclip == False
                        print("Player Noclip: {}".format(self.player.noclip))
                    # Toggle noclip for Projectiles.
                    if event.key == pg.K_x:
                        sprites.BlasterShot.noclip = sprites.BlasterShot.noclip == False
                        print("Projectile Noclip: {}".format(sprites.BlasterShot.noclip))
                    if event.key == pg.K_r:
                        self.screen_pos.update(pg.Vector2(self.start_pos) - config.SCREEN_MID)
                        for sprite in self.projectiles:
                            sprite.kill()
                        print("RESET")
                    # Output the player's inventory
                    if event.key == pg.K_TAB:
                        print("Player Inventory: {}".format(self.player.inventory))
                    # Try to pick up a nearby item.
                    if event.key == pg.K_e:
                        self.player.pickup_item()

            self.player.update()
            self.ship.update()
            self.all_sprites.update()

        # Paused event loop
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                    if event.key == pg.K_SPACE:
                        self.paused = False
                        pg.event.set_grab(True)
                        print("UNPAUSED")
                    ## TEMP
                    if event.key == pg.K_p:
                        pass

                    # Output the player's inventory
                    if event.key == pg.K_TAB:
                        print("Player Inventory: {}".format(self.player.inventory))

        self.menus.update()
        self.screen.fill(config.BLACK)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.menus.draw(self.screen)
        self.debug()

        pg.display.update(self.screen_rect)

        self.clock.tick_busy_loop(config.FPS)


    def debug(self):
        debug1 = self.debug_font.render(
            "Speed: {:.2f} || Velx: {:.2f} || Vely: {:.2f} || Proj: {}".format(
                self.player.vel.magnitude(), self.player.vel.x, self.player.vel.y, len(self.projectiles)
                ),
            False,
            config.WHITE
        )
        self.screen.blit(debug1, (10, 10))

        debug2 = self.debug_font.render(
            "Time: {} || FPS: {:.0f}".format(
                pg.time.get_ticks(), self.clock.get_fps()
                ),
            False,
            config.WHITE
        )
        self.screen.blit(debug2, (10, 30))

        pos_text = self.debug_font.render(
            "x: {:.0f}, y: {:.0f}".format(
                self.screen_pos.x + config.SCREEN_WIDTH / 2, self.screen_pos.y + config.SCREEN_HEIGHT / 2
                ),
            False,
            config.WHITE)
        self.screen.blit(pos_text, (config.SCREEN_WIDTH - 200, config.SCREEN_HEIGHT - 25))


game = Game()
game.start_level()

while game.running:
    game.update()

pg.quit()
print("Donezo!")