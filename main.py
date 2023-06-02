from settings import *
from player import Player
from text import Font
from projectile import Projectile
from enemy import *

# initialize permanent variables
player = Player()

cam_pos = pg.Vector2(0, 0)

font = Font("assets/fonts/font.png", 1)

bullets = Projectile()

bullets.create_proccess("ord_bullet", 0.2, False, "assets/images/bullet.png")

test = DummyTank((0, 0), 90)

while True:
    DISPLAY.fill((250, 250, 250))

    keys_pressed = pg.key.get_pressed()
    mouse_pressed = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    dt = clock.tick(FPS)/1000

    current_time = time.time()

    EVENT = pg.event.get()
    for event in EVENT:
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    # update game-state
    player.move(keys_pressed, dt)
    rects = [pg.Rect(0, 0, 50, 10),
             pg.Rect(0, 100, 10, 50)]

    bullets.bullet_process(DISPLAY, [player.pos.copy(), [5, 5], player.cannon_angle, 30, 1, pg.Rect(0, 0, bullets.proccesses["ord_bullet"]['image'].get_width(), bullets.proccesses["ord_bullet"]['image'].get_height())], "ord_bullet", cam_pos, rects, mouse_pressed, current_time)

    cam_pos[0] += (player.pos[0] - cam_pos[0] - DIS_W//2)/10
    cam_pos[1] += (player.pos[1] - cam_pos[1] - DIS_H//2)/10

    pg.display.set_caption(f"FPS: {clock.get_fps()}, cam_pos: {cam_pos}")

    # update the screen
    

    player.draw(DISPLAY, cam_pos, mouse_pos, dt)
    test.update(DISPLAY, player.pos, cam_pos, dt)


    pg.display.update()
