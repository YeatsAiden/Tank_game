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

        self.image = pg.image.load(image_path)
        self.canon_image = pg.image.load(canon_image_path)

        self.pos = pos

        self.max_health = max_health
        self.health = self.max_health

        self.rotation = initial_rotation
        self.turret_rotation = initial_rotation

        self.dead = False

        self.bullet_type = Projectile()

        self.size = size
        self.speed = speed
        self.turning_speed = turning_speed
        self.canon_turning_speed = canon_turning_speed

    def draw(self):
        pass
    # IM TO LAZY TO DO THIS RIGHT NOW

    def move(self):
        print("you forgot to implement this feature in the child class")
        # this function should make the tank move based on many conditions
        # like where the player is located, are there walls i the way and etc. Maybe even a pathfinding algorithm?


class DummyTank(Tank):
    def __init__(self, pos, initial_rotation):
        super().__init__("assets/images/tank1.png", "assets/images/Cannon.png", pos, 10, initial_rotation, 2, 3, 90, 180)
        self.bullet_type.create_proccess(name="weak_bullet", fire_rate=3, bounces=False,
                                         img_path="assets/images/bullet.png", damage=0.2)



