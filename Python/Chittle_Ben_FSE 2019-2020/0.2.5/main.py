import random
import pygame as pg
from config import *
import player, environment, randomGen3


pg.init() # Try without other inits
pg.font.init()


class Game:

    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.debug_font = pg.font.SysFont("Courier", 20)

        self.screen_pos = pg.Vector2(0, 0)
        #self.dp_rect = pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


    def start_level(self):
        self.all_sprites = pg.sprite.LayeredUpdates(default_layer=SPRITE_LAYER) # Layered update?
        self.walls = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()

        self.sub = randomGen3.Sub(self, (0, 0), 8, 15)
        self.start_pos = self.sub.grid.find_by_tags("start")[0].rect.center
        self.player = player.Player(game=self, pos=self.start_pos)


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
                    self.screen_pos.update(pg.Vector2(self.start_pos) - (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                if event.key == pg.K_q:
                    print(self.sub.grid)


        self.all_sprites.update() # layered?

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.debug()

        pg.display.update()#self.dp_rect)

        self.clock.tick_busy_loop(FPS)


    def debug(self):
        debug1 = self.debug_font.render(
            "Speed: {:.2f} || Velx: {:.2f} || Vely: {:.2f} || Proj: {}".format(
                self.player.vel.magnitude(), self.player.vel.x, self.player.vel.y, len(self.projectiles)
                ),
            False,
            (255, 255, 255)
        )
        self.screen.blit(debug1, (10, 10))

        debug2 = self.debug_font.render(
            "Time: {} || FPS: {:.0f}".format(
                pg.time.get_ticks(), self.clock.get_fps()
                ),
            False,
            (255, 255, 255)
        )
        self.screen.blit(debug2, (10, 30))

        pos_text = self.debug_font.render(
            "x: {:.0f}, y: {:.0f}".format(
                self.screen_pos.x + SCREEN_WIDTH / 2, self.screen_pos.y + SCREEN_HEIGHT / 2
                ),
            False,
            (255, 255, 255))
        self.screen.blit(pos_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 25))


game = Game()
game.start_level()

while game.running:
    game.update()

pg.quit()
print("Donezo!")