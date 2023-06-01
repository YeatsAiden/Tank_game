from settings import *


class Tank:
    def __init__(self, pos, max_health):
        self.pos = pos
        self.max_health = max_health
        self.health = self.max_health
        self.turret_angle
