"""
Date: March 29, 2020
Added:
    >added events
        >toggle noclip for player with 'z'
        >toggle noclip for Projectiles with 'x'
    >call ship.update with other sprite updates

Removed:

Changed:
    >'sub' -> 'ship'
    >modified event - pressing 'r' now removes all projectiles as well as
        resetting the player's position
"""


import random
import pygame as pg
from config import *
import config, environment, levelgen, sprites


pg.init() # Try without other inits
pg.font.init()


class Game:

    def __init__(self):
        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption(config.TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.debug_font = pg.font.SysFont("Courier", 20)

        self.screen_pos = pg.Vector2(0, 0)


    def start_level(self):
        self.all_sprites = pg.sprite.LayeredUpdates(default_layer=config.SPRITE_LAYER)
        self.projectiles = pg.sprite.Group() ##TEMP
        self.items = pg.sprite.Group()

        self.ship = levelgen.Ship(self, (0, 0), 8, 15)
        self.start_pos = self.ship.grid.find_by_tags("start")[0].rect.center
        self.player = sprites.Player(game=self, ship=self.ship, pos=self.start_pos)

        sprites.HandBlaster(self, self.ship, self.start_pos, 0)


    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
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
                if event.key == pg.K_TAB:
                    print("Player Inventory: {}".format(self.player.inventory))
                    #print(self.ship.grid)
                if event.key == pg.K_e: ## should be on Player?
                    self.player.pickup_item(self.items.sprites()[0])
                if event.key == pg.K_p:
                    pass

        self.player.update()
        self.ship.update()
        self.all_sprites.update()

        self.screen.fill(config.BLACK)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.debug()

        pg.display.update()

        self.clock.tick_busy_loop(FPS)


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