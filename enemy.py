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
    def __init__(self, image_path, canon_image_path, pos, max_health, initial_rotation, size, speed, turning_speed,
                 canon_turning_speed, radius_of_vision):

        """
        :param image_path: path to image of the bottom part of the tank
        :param canon_image_path: path to image of the canon
        :param pos: spawn position of the tank
        :param max_health: obvious one
        :param initial_rotation: how much it is rotated when spawned
        :param size: what size the tank is of
        :param speed: speed of the tank (is is a constant)
        :param turning_speed: how fast he is turning
        :param canon_turning_speed: how fast does the canon turn
        :param radius_of_vision: how much does the tank see
        """

        self.image = pg.transform.rotate(pg.transform.scale_by(pg.image.load(image_path), size), initial_rotation)
        self.canon_image = pg.transform.rotate(pg.transform.scale_by(pg.image.load(canon_image_path), size), -initial_rotation)

        self.pos = pos

        self.max_health = max_health
        self.health = self.max_health

        self.rotation = initial_rotation
        self.canon_rotation = initial_rotation

        self.rotation_offset = pg.Vector2(8, 0)

        self.dead = False

        self.bullet_type = Projectile()

        self.size = size
        self.speed = speed
        self.turning_speed = turning_speed
        self.canon_turning_speed = canon_turning_speed

        self.radius_of_vision = radius_of_vision

    def draw_tank(self, surf, cam_pos):
        placeholder_image = self.image  # we need to preserve the original image untouched
        placeholder_image = pg.transform.rotate(placeholder_image, self.rotation)
        placeholder_rect = placeholder_image.get_rect(center=self.pos - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)

    def draw_cannon(self, surf, player_pos, cam_pos):
        self.canon_rotation = calculate_angle_to_point(player_pos, self.pos)
        placeholder_image = self.canon_image
        placeholder_image = pg.transform.rotate(placeholder_image, self.canon_rotation)
        placeholder_rect = placeholder_image.get_rect(center=self.pos + self.rotation_offset.rotate(-self.canon_rotation) - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)

    def draw(self, surf, player_pos, cam_pos):
        self.draw_tank(surf, cam_pos)
        self.draw_cannon(surf, player_pos, cam_pos)

    def move(self):
        print("you forgot to implement this feature in the child class")
        # this function should make the tank move based on many conditions
        # like where the player is located, are there walls i the way and etc. Maybe even a pathfinding algorithm?


class DummyTank(Tank):
    def __init__(self, pos, initial_rotation):
        super().__init__("assets/images/tank1.png", "assets/images/Cannon.png", pos, 10, initial_rotation, 2, 3, 90, 180, 100)
        self.bullet_type.create_proccess(name="weak_bullet", fire_rate=3, bounces=False,
                                         img_path="assets/images/bullet.png", damage=0.2)



