from settings import *
from projectile import Projectile
from game_math import *


class Turret:
    def __init__(self, image_path, cannon_image_path, pos, max_health, size, cannon_turning_speed, bullet_speed, bullet_lifespan, bullet_name):

        self.image = pg.transform.scale_by(pg.image.load(image_path), size)
        self.cannon_image = pg.transform.scale_by(pg.image.load(cannon_image_path), size)

        self.rect = pg.FRect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = pos

        self.max_health = max_health
        self.health = self.max_health

        self.cannon_rotation = 90

        self.rotation_offset = pg.Vector2(2*size, 0)

        self.dead = False

        self.bullet = Projectile()
        self.bullet_name

        self.size = size
        self.cannon_turning_speed = cannon_turning_speed

        self.bullet_speed = bullet_speed  # px/sec
        self.bullet_lifespan = bullet_lifespan  # sec
        self.shooting_range = bullet_lifespan * bullet_speed

        self.cannon_on_target = False

    def draw_cannon(self, surf, cam_pos):
        placeholder_image = self.cannon_image
        placeholder_image = pg.transform.rotate(placeholder_image, self.cannon_rotation)
        placeholder_rect = placeholder_image.get_rect(center=self.rect.center + self.rotation_offset.rotate(-self.cannon_rotation) - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)

    def draw_base(self, surf, cam_pos):
        placeholder_image = self.image  # we need to preserve the original image untouched
        placeholder_rect = placeholder_image.get_rect(center=self.rect.center - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)

    def draw(self, surf, cam_pos):
        self.draw_base(surf, cam_pos)
        self.draw_cannon(surf, cam_pos)

    def rotate_cannon(self, player_pos, dt):
        # make the cannon turn slowly
        desired_cannon_rotation = calculate_angle_to_point(player_pos, self.rect.center)

    def shoot_player(self, surf, layout, player_pos, cam_pos, current_time, dt):
        if dist(player_pos, self.rect.center) <= self.shooting_range and self.cannon_on_target:
            self.bullet.bullet_process(surf, [list(self.rect.center), self.bullet_speed, self.cannon_rotation, self.bullet_lifespan, pg.FRect(0, 0, 10, 10)], self.bullet_name, cam_pos, layout, [True], current_time, dt)

    def update(self, surf, player_pos, cam_pos, layout, current_time, dt):
        self.rotate_cannon(player_pos, dt)
        self.shoot_player(surf, layout, player_pos, cam_pos, current_time, dt)
        self.draw(surf, cam_pos)


class Tank:
    def __init__(self, image_path, cannon_image_path, pos, max_health, initial_rotation, size, speed, turning_speed,
                 cannon_turning_speed, radius_of_vision, bullet_speed, bullet_lifespan, approach_distance, bullet_name):

        """
        :param image_path: path to image of the bottom part of the tank
        :param cannon_image_path: path to image of the cannon
        :param pos: spawn position of the tank
        :param max_health: obvious one
        :param initial_rotation: how much it is rotated when spawned
        :param size: what size the tank is of
        :param speed: speed of the tank (is is a constant)
        :param turning_speed: how fast he is turning
        :param cannon_turning_speed: how fast does the cannon turn
        :param radius_of_vision: how much does the tank see
        :param approach_distance: how close to get to the player - set to 0 if no such limitation is needed
        """

        self.image = pg.transform.rotate(pg.transform.scale_by(pg.image.load(image_path), size), 90)
        self.cannon_image = pg.transform.rotate(pg.transform.scale_by(pg.image.load(cannon_image_path), size), -90)

        self.rect = pg.FRect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = pos

        self.max_health = max_health
        self.health = self.max_health

        self.rotation = initial_rotation
        self.cannon_rotation = initial_rotation

        self.rotation_offset = pg.Vector2(3*size, 0)

        self.dead = False

        self.bullet = Projectile()
        self.bullet_name = bullet_name

        self.size = size
        self.speed = speed
        self.turning_speed = turning_speed
        self.cannon_turning_speed = cannon_turning_speed

        self.radius_of_vision = radius_of_vision
        self.bullet_speed = bullet_speed  # px/sec
        self.bullet_lifespan = bullet_lifespan # sec
        self.shooting_range = bullet_lifespan * bullet_speed

        self.cannon_on_target = False

        self.approach_distance = approach_distance

        self.desired_cannon_rotation = 0
        self.desired_base_rotation = 0

        self.time_since_last_cannon_patrol_rotation = 0
        self.time_since_last_base_patrol_rotation = 0

        self.cannon_patrol_turning_time = 4  # rotations per second
        self.base_patrol_turning_time = 8  # per second
        self.cannon_rotated_to_the_left = False
        self.base_rotated_to_the_left = False
        self.patrol_rotation_offset = 55  # degrees


    def draw_tank(self, surf, cam_pos):
        placeholder_image = self.image  # we need to preserve the original image untouched
        placeholder_image = pg.transform.rotate(placeholder_image, self.rotation)
        placeholder_rect = placeholder_image.get_rect(center=self.rect.center - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)

    def draw_cannon(self, surf, cam_pos):
        placeholder_image = self.cannon_image
        placeholder_image = pg.transform.rotate(placeholder_image, self.cannon_rotation)
        placeholder_rect = placeholder_image.get_rect(center=self.rect.center + self.rotation_offset.rotate(-self.cannon_rotation) - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)

    def draw(self, surf, cam_pos):
        self.draw_tank(surf, cam_pos)
        self.draw_cannon(surf, cam_pos)


    def move(self, tank_rects, tiles, player_pos, dt):
        print("you forgot to implement this feature in the child class")
        # this function should make the tank move based on many conditions
        # like where the player is located, are there walls in the way and etc. Maybe even a pathfinding algorithm?


    def drive_forward(self, tank_rects, tiles, dt):

        for rect in tank_rects:
            if dist(self.rect.center, rect.center) < 20:
                self.rotation = rotate_to(self.rotation, calculate_angle_to_point(self.rect.center, rect.center), self.turning_speed * dt)
        
        self.rect.centerx += self.speed * cos(radians(self.rotation)) * dt

        for rect in tiles:
            if self.rect.colliderect(rect) and self.rect != rect:
                if cos(radians(self.rotation)) < 0:
                    self.rect.left = rect.right
                else:
                    self.rect.right = rect.left

                break

        self.rect.y += self.speed * sin(radians(-self.rotation)) * dt  # WHY IS SIN ALWAYS NEGATIVE???? I MEAN, I DONT UNDERSTAND


        for rect in tiles:
            if self.rect.colliderect(rect) and self.rect != rect:
                if sin(radians(self.rotation)) < 0:
                    self.rect.bottom = rect.top
                else:
                    self.rect.top = rect.bottom

                break

    def approach_movement(self, tank_rects, tiles, player_pos, dt):
        distance_to_player = dist(player_pos, self.rect.center)
        if distance_to_player <= self.radius_of_vision:
            self.rotation = rotate_to(self.rotation, calculate_angle_to_point(player_pos, self.rect.center), self.turning_speed*dt)

            if (distance_to_player > self.approach_distance) and (abs(calculate_smallest_angle(self.rotation, calculate_angle_to_point(player_pos, self.rect.center))) < 60):
                self.drive_forward(tank_rects, tiles, dt)
        else:
            self.patrol_base(dt)


    def rotate_cannon(self, player_pos, dt):
        # make the cannon turn slowly
        distance = dist(self.rect.center, player_pos)
        if distance < self.radius_of_vision:
            self.desired_cannon_rotation = calculate_angle_to_point(player_pos, self.rect.center)
        else:
            self.patrol_cannon(dt)

        self.cannon_rotation = rotate_to(self.cannon_rotation, self.desired_cannon_rotation, self.cannon_turning_speed*dt)

        if (self.cannon_rotation == self.desired_cannon_rotation) and distance < self.radius_of_vision:
            self.cannon_on_target = True
        else:
            self.cannon_on_target = False


    def shoot_player(self, surf, tiles, player_pos, cam_pos, current_time, dt, player):
        self.bullet.bullet_process(surf, [list(self.rect.center), self.bullet_speed, self.cannon_rotation, self.bullet_lifespan, pg.FRect(0, 0, 10, 10)], self.bullet_name, cam_pos, tiles, [dist(player_pos, self.rect.center) <= self.shooting_range and self.cannon_on_target], current_time, dt, [player])


    def check_if_dead(self):
        if self.health <= 0:
            self.dead = True


    def patrol_cannon(self, dt):
        self.time_since_last_cannon_patrol_rotation += dt

        if self.time_since_last_cannon_patrol_rotation > self.cannon_patrol_turning_time:
            self.time_since_last_cannon_patrol_rotation -= self.cannon_patrol_turning_time
            self.cannon_rotated_to_the_left = not self.cannon_rotated_to_the_left

        self.desired_cannon_rotation = self.rotation + (((-1)**self.cannon_rotated_to_the_left)*self.patrol_rotation_offset)

    def patrol_base(self, dt):
        self.time_since_last_base_patrol_rotation += dt

        if self.time_since_last_base_patrol_rotation > self.base_patrol_turning_time:
            self.time_since_last_base_patrol_rotation -= self.base_patrol_turning_time
            self.base_rotated_to_the_left = not self.base_rotated_to_the_left

        self.rotation = rotate_to(self.rotation, (((-1)**self.base_rotated_to_the_left) * self.patrol_rotation_offset), self.turning_speed*dt)

    def update(self, surf, player_pos, cam_pos, tank_rects, tiles, offset, area, current_time, dt, player):
        if offset[0] * TILE_SIZE < self.rect.x < len(area[0][1][0]) * TILE_SIZE + offset[0] * TILE_SIZE and offset[1] * TILE_SIZE < self.rect.y < len(area[0][1]) * TILE_SIZE + offset[1] * TILE_SIZE:
            self.move(tank_rects, tiles, player_pos, dt)

        self.rotate_cannon(player_pos, dt)
        self.shoot_player(surf, tiles, player_pos, cam_pos, current_time, dt, player)
        self.draw(surf, cam_pos)

        self.check_if_dead()


class TankGroup:
    def __init__(self, tanks: list[Tank], name):
        self.tanks = tanks  # a list of all tanks
        self.group_name = name

    def update(self, surf, player, cam_pos, tank_rects, tiles, offset, area, current_time, dt):
        tanks_to_remove = []
        for i, tank in enumerate(self.tanks):
            tank.update(surf, player.rect.center, cam_pos, tank_rects, tiles, offset, area, current_time, dt, player)

            if tank.dead:
                tanks_to_remove.append(i)

        for i in tanks_to_remove[::-1]:
            self.tanks.pop(i)

    def draw(self, surf):
        pass

    def move(self, player_pos):
        pass


class NormalTank(Tank):
    def __init__(self, pos, initial_rotation):
        super().__init__("assets/images/player/tank.png", "assets/images/player/cannon.png", pos, max_health=30, initial_rotation=initial_rotation, size=1.2,
                         speed=100, turning_speed=120, cannon_turning_speed=180, radius_of_vision=190, bullet_speed=250,
                         bullet_lifespan=0.6, approach_distance=75, bullet_name="normal_bullet")

        self.bullet.create_proccess(name="normal_bullet", fire_rate=1.5, bounces=False, img_path="assets/images/player/bullet.png",
                                    damage=10, sound=NORMAL_CANNON)

    def move(self, tank_rects, tiles, player_pos, dt):
        self.approach_movement(tank_rects, tiles, player_pos, dt)


class MiniTank(Tank):
    def __init__(self, pos, initial_rotation):
        super().__init__("assets/images/mini_tank/mini_tank.png", "assets/images/mini_tank/mini_tank_cannon.png", pos, max_health=7, initial_rotation=initial_rotation, size=1,
                         speed=60, turning_speed=90, cannon_turning_speed=180, radius_of_vision=300, bullet_speed=300,
                         bullet_lifespan=0.75, approach_distance=10, bullet_name="mini_bullet")

        self.bullet.create_proccess(name="mini_bullet", fire_rate=1, bounces=False, img_path="assets/images/mini_tank/mini_tank_bullet.png",
                                    damage=1, sound=MINI_TURRET)

    def move(self, tank_rects, tiles, player_pos, dt):
        self.approach_movement(tank_rects, tiles, player_pos, dt)


class BuffTank(Tank):
    def __init__(self, pos, initial_rotation):
        super().__init__("assets/images/buff_tank/buff_tank.png", "assets/images/buff_tank/buff_tank_cannon.png", pos, max_health=70, initial_rotation=initial_rotation, size=2,
                         speed=15, turning_speed=40, cannon_turning_speed=90, radius_of_vision=400, bullet_speed=400,
                         bullet_lifespan=1.5, approach_distance=200, bullet_name="buff_bullet")

        self.bullet.create_proccess(name="buff_bullet", fire_rate=10, bounces=False, img_path="assets/images/buff_tank/buff_tank_bullet.png",
                                    damage=25, sound=BIG_CHUNGUS)

    def move(self, tank_rects, tiles, player_pos, dt):
        self.approach_movement(tank_rects, tiles, player_pos, dt)


class FastTank(Tank):
    def __init__(self, pos, initial_rotation):
        super().__init__("assets/images/fast_tank/fast_tank.png", "assets/images/fast_tank/fast_tank_cannon.png", pos, max_health=30, initial_rotation=initial_rotation, size=1,
                         speed=200, turning_speed=270, cannon_turning_speed=180, radius_of_vision=200, bullet_speed=250,
                         bullet_lifespan=1.5, approach_distance=75, bullet_name="fast_bullet")

        self.bullet.create_proccess(name="fast_bullet", fire_rate=1, bounces=False, img_path="assets/images/fast_tank/fast_tank_bullet.png",
                                    damage=10, sound=NORMAL_CANNON)

    def move(self, tank_rects, tiles, player_pos, dt):
        self.approach_movement(tank_rects, tiles, player_pos, dt)


class MiniGunTank(Tank):
    def __init__(self, pos, initial_rotation):
        super().__init__("assets/images/mini_gun_tank/mini_gun_tank.png", "assets/images/mini_gun_tank/mini_gun_tank_cannon.png", pos, max_health=30, initial_rotation=initial_rotation, size=1.6,
                         speed=50, turning_speed=90, cannon_turning_speed=270, radius_of_vision=200, bullet_speed=250,
                         bullet_lifespan=0.5, approach_distance=75, bullet_name="a_lot_of_bullets")

        self.bullet.create_proccess(name="a_lot_of_bullets", fire_rate=0.1, bounces=False, img_path="assets/images/mini_gun_tank/mini_gun_tank_bullet.png",
                                    damage=1, sound=MINIGUN)

    def move(self, tank_rects, tiles, player_pos, dt):
        self.approach_movement(tank_rects, tiles, player_pos, dt)


# class BossTank(Tank):
#     def __init__(self, pos, initial_rotation):
#         super().__init__("assets/images/player/tank.png", "assets/images/player/cannon.png", pos, max_health=500, initial_rotation=initial_rotation, size=6,
#                          speed=10, turning_speed=40, cannon_turning_speed=180, radius_of_vision=1000, bullet_speed=300,
#                          bullet_lifespan=4, approach_distance=300, bullet_name="boss_bullet")
#
#         self.bullet.create_proccess(name="boss_bullet", fire_rate=10, bounces=False, img_path="assets/images/player/bullet.png",
#                                     damage=2, sound=NORMAL_CANNON)
#
#     def move(self, tank_rects, tiles, player_pos, dt):
#         self.approach_movement(tank_rects, tiles, player_pos, dt)



