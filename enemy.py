from settings import *


class TankGroup:
    def __init__(self, tanks):
        self.tanks = tanks

    def update(self):
        pass
        # check if any of the tanks died, if so remove them from the list
        # basically call "update" of every tank


class Tank:
    def __init__(self, pos, max_health, initial_rotation):
        self.pos = pos

        self.max_health = max_health
        self.health = self.max_health

        self.rotation = initial_rotation
        self.turret_rotation = initial_rotation

        self.dead = False

        self.bullet_type = 0

    def draw(self):
        print("you forgot to implement this feature in the child class")

    def move(self):
        print("you forgot to implement this feature in the child class")
