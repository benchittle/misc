import random
import pygame as pg
from config import *
import player, environment, randomGen


pg.init() # Try without other inits
pg.font.init()




class Game:
    DIRECTIONS = {
        "n" : "top",
        "e" : "right",
        "s" : "bottom",
        "w" : "left",
        "top" : "n",
        "right" : "e",
        "bottom" : "s",
        "left" : "w"
        }
    OPPOSITES = {
        "n" : "s",
        "e" : "w",
        "s" : "n",
        "w" : "e",
        "top" : "bottom",
        "right" : "left",
        "bottom" : "top",
        "left" : "right"
    }

    def __init__(self):
        self.dp = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.debug_font = pg.font.SysFont("Courier", 20)

        self.dp_pos = pg.Vector2(0, 0)
        #self.dp_rect = pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


    def start_level(self):
        self.all_sprites = pg.sprite.Group() # Layered update?
        self.walls = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()

        self.sub = randomGen.Sub(self, random.randint(3, 6), random.randint(5, 10))
        print(self.sub)
        self.start_pos = self.sub.find_by_tags("start")[0].rect.center
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
                    self.dp_pos.update(pg.Vector2(self.start_pos) - (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.all_sprites.update() # layered?

        self.dp.fill(BLACK)
        self.all_sprites.draw(self.dp)
        self.debug()
        #self.dp_rect.center = self.player.pos - self.dp_pos
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
        self.dp.blit(debug1, (10, 10))

        debug2 = self.debug_font.render(
            "Time: {} || FPS: {:.0f}".format(
                pg.time.get_ticks(), self.clock.get_fps()
                ),
            False,
            (255, 255, 255)
        )
        self.dp.blit(debug2, (10, 30))

        pos_text = self.debug_font.render(
            "x: {:.0f}, y: {:.0f}".format(
                self.dp_pos.x + SCREEN_WIDTH / 2, self.dp_pos.y + SCREEN_HEIGHT / 2
                ),
            False,
            (255, 255, 255))
        self.dp.blit(pos_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 25))




game = Game()
game.start_level()

while game.running:
    game.update()

pg.quit()
print("Donezo!")