from settings import *
from projectile import Projectile
from game_math import *


class Turret:
    def __init__(self, image_path, cannon_image_path, pos, max_health, size, cannon_turning_speed, bullet_speed, bullet_lifespan):

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
            self.bullet.bullet_process(surf, [list(self.rect.center), self.bullet_speed, self.cannon_rotation, self.bullet_lifespan, pg.FRect(0, 0, 10, 10)], "dummy_bullet", cam_pos, layout, [True], current_time, dt)

    def update(self, surf, player_pos, cam_pos, layout, current_time, dt):
        self.rotate_cannon(player_pos, dt)
        self.shoot_player(surf, layout, player_pos, cam_pos, current_time, dt)
        self.draw(surf, cam_pos)


class Tank:
    def __init__(self, image_path, cannon_image_path, pos, max_health, initial_rotation, size, speed, turning_speed,
                 cannon_turning_speed, radius_of_vision, bullet_speed, bullet_lifespan, approach_distance):

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

        self.image = pg.transform.rotate(pg.transform.scale_by(pg.image.load(image_path), size), initial_rotation)
        self.cannon_image = pg.transform.rotate(pg.transform.scale_by(pg.image.load(cannon_image_path), size), -initial_rotation)

        self.rect = pg.FRect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = pos

        self.max_health = max_health
        self.health = self.max_health

        self.rotation = initial_rotation
        self.cannon_rotation = initial_rotation

        self.rotation_offset = pg.Vector2(6, 0)

        self.dead = False

        self.bullet = Projectile()

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

        # PROBABLY TEMPORARY

        upper_circle_pos = self.rect.center - cam_pos
        lower_circle_pos = upper_circle_pos[0]+2, upper_circle_pos[1]+2

        # draw shooting range
        pg.draw.circle(surf, (84, 30, 19), lower_circle_pos, self.shooting_range, 4)
        pg.draw.circle(surf, (208, 60, 50), upper_circle_pos, self.shooting_range, 4)

    def move(self, layout, player_pos, dt):
        print("you forgot to implement this feature in the child class")
        # this function should make the tank move based on many conditions
        # like where the player is located, are there walls i the way and etc. Maybe even a pathfinding algorithm?

    def drive_forward(self, layout, dt):
        self.rect.centerx += self.speed * cos(radians(self.rotation)) * dt

        for rect in layout:
            if self.rect.colliderect(rect):
                if cos(radians(self.rotation)) < 0:
                    self.rect.left = rect.right
                else:
                    self.rect.right = rect.left

                break

        self.rect.centery += self.speed * sin(radians(-self.rotation)) * dt  # WHY IS SIN ALWAYS NEGATIVE???? I MEAN, I DONT UNDERSTAND

        for rect in layout:
            if self.rect.colliderect(rect):
                if sin(radians(self.rotation)) < 0:
                    self.rect.bottom = rect.top
                else:
                    self.rect.top = rect.bottom

                break

    def approach_movement(self, layout, player_pos, dt):
        distance_to_player = dist(player_pos, self.rect.center)
        if distance_to_player <= self.radius_of_vision:
            self.rotation = rotate_to(self.rotation, calculate_angle_to_point(player_pos, self.rect.center), self.turning_speed*dt)

            if (distance_to_player > self.approach_distance) and (abs(calculate_smallest_angle(self.rotation, calculate_angle_to_point(player_pos, self.rect.center))) < 60):
                self.drive_forward(layout, dt)


    def rotate_cannon(self, player_pos, dt):
        # make the cannon turn slowly
        if dist(self.rect.center, player_pos) < self.radius_of_vision:
            desired_cannon_rotation = calculate_angle_to_point(player_pos, self.rect.center)
        else:
            desired_cannon_rotation = self.rotation

        self.cannon_rotation = rotate_to(self.cannon_rotation, desired_cannon_rotation, self.cannon_turning_speed*dt)

        if self.cannon_rotation == desired_cannon_rotation:
            self.cannon_on_target = True
        else:
            self.cannon_on_target = False


    def shoot_player(self, surf, layout, player_pos, cam_pos, current_time, dt):
        self.bullet.bullet_process(surf, [list(self.rect.center), self.bullet_speed, self.cannon_rotation, self.bullet_lifespan, pg.FRect(0, 0, 10, 10)], "dummy_bullet", cam_pos, layout, [dist(player_pos, self.rect.center) <= self.shooting_range and self.cannon_on_target], current_time, dt)

    def check_if_dead(self):
        if self.health <= 0:
            self.dead = True

    def update(self, surf, player_pos, cam_pos, layout, current_time, dt):
        self.move(layout, player_pos, dt)

        self.rotate_cannon(player_pos, dt)
        self.shoot_player(surf, layout, player_pos, cam_pos, current_time, dt)
        self.draw(surf, cam_pos)

        self.check_if_dead()


class TankGroup:
    def __init__(self, tanks: list[Tank]):
        self.tanks = tanks  # a list of all tanks

    def update(self, surf, player_pos, cam_pos, layout, current_time, dt):
        tanks_to_remove = []
        for i, tank in enumerate(self.tanks):
            tank.update(surf, player_pos, cam_pos, layout, current_time, dt)

            if tank.dead:
                tanks_to_remove.append(i)

        for i in tanks_to_remove:
            self.tanks.pop(i)

    def draw(self, surf):
        pass

    def move(self, player_pos):
        pass


class DummyTank(Tank):
    def __init__(self, pos, initial_rotation):
        super().__init__("assets/images/tank1.png", "assets/images/Cannon.png", pos, 10, initial_rotation, size=1.5,
                         speed=30, turning_speed=23, cannon_turning_speed=45, radius_of_vision=100, bullet_speed=200,
                         bullet_lifespan=0.5, approach_distance=0)

        self.bullet.create_proccess(name="dummy_bullet", fire_rate=3, bounces=False, img_path="assets/images/bullet.png",
                                    damage=0.2)

    def move(self, layout, player_pos, dt):
        self.approach_movement(layout, player_pos, dt)



