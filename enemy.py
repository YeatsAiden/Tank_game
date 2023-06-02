from settings import *
from projectile import Projectile


class TankGroup:
    def __init__(self, tanks):
        self.tanks = tanks  # a list of all tanks

    def update(self):
        pass
        # check if any of the tanks died, if so remove them from the list
        # basically call "update" of every tank

    def draw(self, surf):
        pass

    def move(self, player_pos):
        pass


class Tank:
    def __init__(self, image_path, cannon_image_path, pos, max_health, initial_rotation, size, speed, turning_speed,
                 cannon_turning_speed, radius_of_vision, bullet_lifespan, bullet_speed):

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
        :param bullet_lifespan: how long will the bullet live
        """

        self.image = pg.transform.rotate(pg.transform.scale_by(pg.image.load(image_path), size), initial_rotation)
        self.cannon_image = pg.transform.rotate(pg.transform.scale_by(pg.image.load(cannon_image_path), size), -initial_rotation)

        self.pos = pos

        self.max_health = max_health
        self.health = self.max_health

        self.rotation = initial_rotation
        self.cannon_rotation = initial_rotation

        self.rotation_offset = pg.Vector2(8, 0)

        self.dead = False

        self.bullet = Projectile()

        self.size = size
        self.speed = speed
        self.turning_speed = turning_speed
        self.cannon_turning_speed = cannon_turning_speed

        self.radius_of_vision = radius_of_vision

        self.bullet_lifespan = bullet_lifespan
        self.bullet_speed = bullet_speed
        self.radius_of_shoot = self.bullet_speed * self.bullet_lifespan

    def draw_tank(self, surf, cam_pos):
        placeholder_image = self.image  # we need to preserve the original image untouched
        placeholder_image = pg.transform.rotate(placeholder_image, self.rotation)
        placeholder_rect = placeholder_image.get_rect(center=self.pos - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)

    def draw_cannon(self, surf, cam_pos):
        placeholder_image = self.cannon_image
        placeholder_image = pg.transform.rotate(placeholder_image, self.cannon_rotation)
        placeholder_rect = placeholder_image.get_rect(center=self.pos + self.rotation_offset.rotate(-self.cannon_rotation) - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)

    def draw(self, surf, cam_pos):
        self.draw_tank(surf, cam_pos)
        self.draw_cannon(surf, cam_pos)

    def move(self, level_map, player_pos):
        print("you forgot to implement this feature in the child class")
        # this function should make the tank move based on many conditions
        # like where the player is located, are there walls i the way and etc. Maybe even a pathfinding algorithm?

    def rotate_cannon(self, player_pos, dt):
        # make the cannon turn slowly
        desired_cannon_rotation = calculate_angle_to_point(player_pos, self.pos)
        # complicated math - i can explain it if you need
        # this is like a mini XNOR gate, i promise i can explain
        self.cannon_rotation += ((-1)**(sin(radians(self.cannon_rotation)) >= sin(radians(-desired_cannon_rotation))) * (-1)**(cos(radians(self.cannon_rotation)) >= cos(radians(desired_cannon_rotation))) * self.turning_speed * dt) if abs(desired_cannon_rotation - self.cannon_rotation) > 2 else 0

    def shoot(self, surf, cam_pos, tiles, player_pos, current_time):
        if dist(player_pos, self.pos) <= self.radius_of_shoot:
            self.bullet.bullet_process(surf, [self.pos.copy(), [5, 5], self.cannon_rotation, self.bullet_lifespan*FPS, 1, pg.Rect(0, 0, self.bullet.proccesses["ord_bullet"]['image'].get_width(), self.bullet.proccesses["ord_bullet"]['image'].get_height())], "idk1.0", cam_pos, tiles, True, current_time)

    def update(self, surf, player_pos, cam_pos, dt):
        self.rotate_cannon(player_pos, dt)
        self.draw(surf, cam_pos)


class DummyTank(Tank):
    def __init__(self, pos, initial_rotation):
        super().__init__(image_path="assets/images/tank1.png", cannon_image_path="assets/images/Cannon.png", pos=pos,
                         max_health=10, initial_rotation=initial_rotation, size=2, speed=3, turning_speed=90,
                         cannon_turning_speed=180, radius_of_vision=100, bullet_lifespan=1, bullet_speed=100)

        self.bullet.create_proccess(name="weak_bullet", fire_rate=3, bounces=False,
                                         img_path="assets/images/bullet.png", damage=0.2)



