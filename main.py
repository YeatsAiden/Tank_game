from settings import *
import settings
from player import Player
from text import Font
from projectile import Projectile
from load_map import Load_map
from enemy import *
from gate import Gate
from cannon import *


def reset():
    # Global = Bad, but whatever, nobody can tell me what to do ¯\_(ツ)_/¯
    global player, cam_pos, font, bullets, load_map, level_1, levels, gates, clock, FPS, cannons, screen_shake

    # initialize permanent variables
    player = Player()

    cam_pos = pg.Vector2(player.rect.x, player.rect.y)

    font = Font("assets/fonts/font.png", 1)
    font.create_speech_bubble("intro", "Dear player. Due to the fact that we didn't have enough time to finish our game, some parts of the game may look unfinished/unpolished/buggy. The game may not follow the theme of the jam, but we did try and it was a learning experience, and we ask you to enjoy our little but sadistic game and maybe give us some feed back :D. PS please don't roast the code.", pg.Rect(20, 40, 440, 180))

    bullets = Projectile()

    load_map = Load_map("assets/world/world.tmx", ["assets/world/floor.csv", "assets/world/walls.csv", "assets/world/spawns.csv"])

    bullets.create_proccess("ord_bullet", 1.5, False, "assets/images/player/bullet.png", 25, deals_area_damage=False, damage_r=0, sound=NORMAL_CANNON)

    level_1 = TankGroup([], "level_1")
    level_2 = TankGroup([], "level_2")
    level_3 = TankGroup([], "level_3")
    level_4 = TankGroup([], "level_4")
    level_5 = TankGroup([], "level_5")
    levels = [level_1, level_2, level_3, level_4, level_5]
    gates = [0, 1, 2, 3, 4]

    for pos, name in load_map.get_all_spawn_positions(load_map.world_csv_data, 'spawns'):
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
            gates[0] = Gate(["assets/tile_set/gate_vertical_closed.png", "assets/tile_set/gate_vertical_opened.png"], pos)
        elif name == "horizontal_gate_level_2":
            gates[1] = Gate(["assets/tile_set/gate_horizontal_closed.png", "assets/tile_set/gate_horizontal_opened.png"], pos)
        elif name == "horizontal_gate_level_3":
            gates[2] = Gate(["assets/tile_set/gate_horizontal_closed.png", "assets/tile_set/gate_horizontal_opened.png"], pos)
        elif name == "vertical_gate_level_4":
            gates[3] = Gate(["assets/tile_set/gate_vertical_closed.png", "assets/tile_set/gate_vertical_opened.png"], pos)
        elif name == "vertical_gate_level_5":
            gates[4] = Gate(["assets/tile_set/gate_vertical_closed.png", "assets/tile_set/gate_vertical_opened.png"], pos)
        elif name == "player":
            player.rect.center = pos

    clock = pg.time.Clock()
    FPS = 60  # bcz my potato laptop cannot handle 100 fps
    screen_shake = 0
    

    # load cannons
    cannons = [BigChungus(), MiniGun(), ElBombe()]


reset()
async def main():
    global player, cam_pos, font, bullets, load_map, level_1, levels, gates, clock, FPS, cannons, screen_shake
    intro = True
    pg.mixer.music.play(-1)
    while True:
        while intro:
            DISPLAY.fill((33, 33, 35))
            pg.draw.rect(DISPLAY, "black", pg.Rect(20, 50, 440, 180), 4)
            if font.render_dialogue(DISPLAY, "intro"):
                intro = False
            settings.EVENT = pg.event.get()
            for event in settings.EVENT:
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            pg.display.update()

        if player.health <= 0:
            reset()

        entities = []
        DISPLAY.fill((33, 33, 35))

        keys_pressed = pg.key.get_pressed()
        mouse_pressed = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        dt = clock.tick(FPS)/1000

        current_time = time.time()

        settings.EVENT = pg.event.get()
        for event in settings.EVENT:
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # update gamestate
        player.move(keys_pressed, load_map.world_rects, dt)

        cam_pos[0] += (player.rect.x - cam_pos[0] - DIS_W//2)/10
        cam_pos[1] += (player.rect.y - cam_pos[1] - DIS_H//2)/10

        load_map.list_of_areas_on_layers_to_be_rendered, load_map.offset = load_map.get_areas_for_rendering(DISPLAY, cam_pos, load_map.world_csv_data)
        load_map.world_rects = load_map.make_rects_array(load_map.offset, load_map.list_of_areas_on_layers_to_be_rendered) + [gate.rect for gate in gates]

        for level in levels:
            entities += level.tanks
        
        if screen_shake:
            cam_pos[0] += random.randint(-5, 5)
            cam_pos[1] += random.randint(-5, 5)
            screen_shake -= dt
            screen_shake = 0 if screen_shake < 0 else screen_shake
        


        # update the screen
        load_map.draw_world(DISPLAY, cam_pos, load_map.offset, load_map.list_of_areas_on_layers_to_be_rendered)

        for cannon in cannons:
            cannon.update(DISPLAY, player, cam_pos)

        screen_shake += player.shoot(DISPLAY, cam_pos, load_map.world_rects, mouse_pressed, current_time, dt, entities)

        for index, level in enumerate(levels):
            screen_shake += level.update(DISPLAY, player, cam_pos, [tank.rect for tank in level.tanks], load_map.world_rects, load_map.offset, load_map.list_of_areas_on_layers_to_be_rendered, current_time, dt)

            gates[index].draw(DISPLAY, cam_pos)
            if len(level.tanks) == 0 and gates[index].closed:
                if gates[index].closed:
                    screen_shake += 0.6
                gates[index].closed = False

                HURT.play()  # uhh, this sound is very good for the gates opening

        player.draw(DISPLAY, cam_pos, mouse_pos, dt)

        await asyncio.sleep(0)

        pg.display.update()

asyncio.run(main())