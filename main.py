from settings import *
from player import Player
from text import Font
from projectile import Projectile
from load_map import Load_map
from enemy import *

# initialize permanent variables
player = Player()

cam_pos = pg.Vector2(0, 0)

font = Font("assets/fonts/font.png", 1)

bullets = Projectile()

load_map = Load_map("assets/world/world.tmx", ["assets/world/floor.csv", "assets/world/walls.csv"])

bullets.create_proccess("ord_bullet", 0.2, False, "assets/images/bullet.png")

test = DummyTank((200, 200), 90)

clock = pg.time.Clock()
FPS = 60  # bcz my potato laptop cannot handle 100 fps

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

    # update gamestate
    player.move(keys_pressed, load_map.world_rects, dt)

    cam_pos[0] += (player.rect.x - cam_pos[0] - DIS_W//2)/10
    cam_pos[1] += (player.rect.y - cam_pos[1] - DIS_H//2)/10
    
    pg.display.set_caption(f"FPS: {clock.get_fps()}, cam_pos: {cam_pos}")

    load_map.list_of_areas_on_layers_to_be_rendered, load_map.offset = load_map.get_area_for_rendering(DISPLAY, cam_pos, load_map.world_csv_data)
    load_map.world_rects = load_map.make_rects_array(load_map.offset, load_map.list_of_areas_on_layers_to_be_rendered, COLLISION_LAYERS)

    # update the screen
    load_map.draw_world(DISPLAY, cam_pos, load_map.offset, load_map.list_of_areas_on_layers_to_be_rendered)

    new_bullet = [[player.rect.center[0], player.rect.center[1]], 400, player.cannon_angle, 2, pg.FRect(0, 0, bullets.proccesses["ord_bullet"]['image'].get_width(), bullets.proccesses["ord_bullet"]['image'].get_height())]
    bullets.bullet_process(DISPLAY, new_bullet, "ord_bullet", cam_pos, load_map.world_rects, mouse_pressed, current_time, dt)

    test.update(DISPLAY, player.rect.center, cam_pos, load_map.world_rects, current_time, dt)
    player.draw(DISPLAY, cam_pos, mouse_pos, dt)

    pg.display.update()
