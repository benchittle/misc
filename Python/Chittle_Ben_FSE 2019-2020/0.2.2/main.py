import pygame as pg
from settings import *
import player, environment, maps


pg.init() # Try without other inits
pg.font.init()




class Game:
    def __init__(self):
        self.dp = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.debug_font = pg.font.SysFont("Courier", 20)

        self.dp_pos = pg.Vector2(0, 0)


    def start_level(self):
        self.level_dict = maps.TEST_LEVEL #LEVEL_PLAYGROUND
        self.all_sprites = pg.sprite.Group() # Layered update?
        self.walls = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()

        self.player = player.Player(game=self, data=self.level_dict["player"])
        for x, y, w, h in self.level_dict["walls"]: #col
            environment.Wall(self, x, y, w, h, (255, 0, 0))


    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

        self.all_sprites.update() # layered?

        self.dp.fill(BLACK)
        self.all_sprites.draw(self.dp)
        self.debug()
        pg.display.update()

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