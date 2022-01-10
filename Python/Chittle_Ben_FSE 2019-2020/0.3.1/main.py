"""
Date
Changed

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

        self.sub = levelgen.Sub(self, (0, 0), 8, 15)
        self.start_pos = self.sub.grid.find_by_tags("start")[0].rect.center
        self.player = sprites.Player(game=self, pos=self.start_pos)

        sprites.HandBlaster(self, self.start_pos, 0)


    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_z:
                    self.player.collisions = self.player.collisions == False
                if event.key == pg.K_r:
                    self.screen_pos.update(pg.Vector2(self.start_pos) - config.SCREEN_MID)
                if event.key == pg.K_TAB:
                    print(self.player.inventory)
                    #print(self.sub.grid)
                if event.key == pg.K_e:
                    self.player.pickup_item(self.items.sprites()[0])

        self.player.update()
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