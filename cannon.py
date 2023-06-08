from settings import *
from projectile import *


class Cannon:
    def __init__(self, pos, bullet_name, image):
        self.rect = pg.Rect(pos, (32, 32))  # if player collides with it, he picks it up

        self.image = image

        self.bullet_name = bullet_name

    def check_collision_with_player(self, player):
        if self.rect is not None:
            if player.rect.colliderect(self.rect):
                player.bullet_name = self.bullet_name
                self.rect = None
                player.cannon_img = pg.transform.rotate(self.image, -90)

    def draw(self, surf, cam_pos):
        if self.rect is not None:
            placeholder = self.image
            placeholder_rect = placeholder.get_rect(center=self.rect.bottomright-cam_pos)
            surf.blit(placeholder, placeholder_rect)

    def update(self, surf, player, cam_pos):
        self.check_collision_with_player(player)
        self.draw(surf, cam_pos)


class BigChungus(Cannon):
    def __init__(self):
        super().__init__((1842, 1592), "buff_bullet", pg.image.load("assets/images/buff_tank/buff_tank_cannon.png"))


class MiniGun(Cannon):
    def __init__(self):
        super().__init__((1336, 752), "minigun_bullet", pg.image.load("assets/images/mini_gun_tank/mini_gun_tank_cannon.png"))
