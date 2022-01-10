import pygame as pg
import player, environment, level

pg.init() # Try without other inits
pg.font.init()

def debug():
    debug1 = debug_font.render(
        "Speed: {:.2f} || Velx: {:.2f} || Vely: {:.2f} || Bullets: {}".format(
            player1.speed, player1.velx, player1.vely, len(sprites["projectiles"])
            ),
        False,
        (255, 255, 255)
    )
    dp.blit(debug1, (10, 10))

    debug2 = debug_font.render(
        "Time: {} || FPS: {:.0f}".format(
            pg.time.get_ticks(), clock.get_fps()
            ),
        False,
        (255, 255, 255)
    )
    dp.blit(debug2, (10, 30))

    '''debug3 = debug_font.render(
        "Health: {} || Shield: {:.0f}".format(
            sprites["targets"].sprites()[0].health, sprites["targets"].sprites()[0].shield
            ),
        False,
        (255, 255, 255)
    )
    dp.blit(debug3, (10, 60))'''

    pos_text = debug_font.render(
        "x: {:.0f}, y: {:.0f}".format(
            player1.rect.x, player1.rect.y
            ),
        False,
        (255, 255, 255))
    dp.blit(pos_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 25))

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

dp = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Prelims done, Continuing...")
clock = pg.time.Clock()
debug_font = pg.font.SysFont("Courier", 20)

sprites = {
    "player" : player.Player.instances,
    "walls" : environment.Wall.instances,
    "projectiles" : player.Projectile.instances,
    "targets" : environment.Target.instances
    }

motion_settings = {
    "friction" : 0.05,
    "slow_threshold" : 0.4,
    "accel" : 0.5,
    "max_speed" : 7
    }


level1 = level.Level(sprites, level.playground)
level1.setup()

player1 = player.Player(
    sprites=sprites,
    x=50,
    y=650,
    motion=motion_settings
    )


run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
    dp.fill((0, 0, 0))

    debug()

    for group in sprites.values():
        group.update()
        group.draw(dp)





    pg.display.update()
    clock.tick_busy_loop(FPS)


pg.quit()
print("Donezo!")