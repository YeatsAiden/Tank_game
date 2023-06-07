from settings import *
from player import Player
from text import Font
from projectile import Projectile
from load_map import Load_map
from enemy import *
from gate import Gate

# initialize permanent variables
player = Player()

cam_pos = pg.Vector2(0, 0)

font = Font("assets/fonts/font.png", 1)

bullets = Projectile()

load_map = Load_map("assets/world/world.tmx", ["assets/world/floor.csv", "assets/world/walls.csv", "assets/world/spawns.csv"])

bullets.create_proccess("ord_bullet", 1.5, False, "assets/images/player/bullet.png", 25)

level_1 = TankGroup([], "level_1")
level_2 = TankGroup([], "level_2")
level_3 = TankGroup([], "level_3")
level_4 = TankGroup([], "level_4")
level_5 = TankGroup([], "level_5")
levels = [level_1, level_2, level_3, level_4, level_5]
gates = []

for pos, name in load_map.get_all_spawn_positions(load_map.world_csv_data, 'spawns'):
    # print(name)
    if name == "normal_tank":
        level_1.tanks.append(NormalTank(pos, random.randint(-180, 180)))
    elif name == "mini_tank":
        level_2.tanks.extend([MiniTank(pos + [random.randint(-20, 20), random.randint(-20, 20)], random.randint(-180, 180)) for _ in range(5)])
    elif name == "buff_tank":
        level_3.tanks.append(BuffTank(pos, random.randint(-180, 180)))
    elif name == "fast_tank":
        level_4.tanks.append(FastTank(pos, random.randint(-180, 180)))
    elif name == "mini_gun_tank":
        level_5.tanks.append(MiniGunTank(pos, random.randint(-180, 180)))
    elif name == "vertical_gate_level_1":
        gates.insert(0 ,Gate(["assets/tile_set/gate_vertical_closed.png", "assets/tile_set/gate_vertical_opened.png"], pos))
    elif name == "horizontal_gate_level_2":
        gates.insert(1, Gate(["assets/tile_set/gate_horizontal_closed.png", "assets/tile_set/gate_horizontal_opened.png"], pos))
    elif name == "horizontal_gate_level_3":
        gates.insert(2, Gate(["assets/tile_set/gate_horizontal_closed.png", "assets/tile_set/gate_horizontal_opened.png"], pos))
    elif name == "vertical_gate_level_4":
        gates.insert(3 ,Gate(["assets/tile_set/gate_vertical_closed.png", "assets/tile_set/gate_vertical_opened.png"], pos))
    elif name == "vertical_gate_level_5":
        gates.insert(4 ,Gate(["assets/tile_set/gate_vertical_closed.png", "assets/tile_set/gate_vertical_opened.png"], pos))
    elif name == "player":
        player.rect.center = pos

clock = pg.time.Clock()
FPS = 60  # bcz my potato laptop cannot handle 100 fps


while True:
    entities = []
    DISPLAY.fill((33, 33, 35))

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

    load_map.list_of_areas_on_layers_to_be_rendered, load_map.offset = load_map.get_areas_for_rendering(DISPLAY, cam_pos, load_map.world_csv_data)
    load_map.world_rects = load_map.make_rects_array(load_map.offset, load_map.list_of_areas_on_layers_to_be_rendered) + [gate.rect for gate in gates]

    for level in levels:
        entities += level.tanks

    # update the screen
    load_map.draw_world(DISPLAY, cam_pos, load_map.offset, load_map.list_of_areas_on_layers_to_be_rendered)

    new_bullet = [[player.rect.center[0], player.rect.center[1]], 400, player.cannon_angle, 2, pg.FRect(0, 0, bullets.proccesses["ord_bullet"]['image'].get_width(), bullets.proccesses["ord_bullet"]['image'].get_height())]
    bullets.bullet_process(DISPLAY, new_bullet, "ord_bullet", cam_pos, load_map.world_rects, mouse_pressed, current_time, dt, entities)
    
    for index, level in enumerate(levels):
        level.update(DISPLAY, player, cam_pos, [tank.rect for tank in level.tanks], load_map.world_rects, current_time, dt)
        gates[index].draw(DISPLAY, cam_pos)
        if len(level.tanks) == 0:
            gates[index].closed = False

    player.draw(DISPLAY, cam_pos, mouse_pos, dt)

    pg.display.update()
