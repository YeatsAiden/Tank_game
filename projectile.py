from settings import *


class Projectile:
    def __init__(self):
        self.proccesses = {}

    # "dirt_explosion", 2, True, False, dirt_img, 0.1     - ?????????
    def create_proccess(self, name, fire_rate, bounces, img_path, damage=0, deals_area_damage=False, damage_r=0):
        """
        name; name of the process
        fire_rate: how fast does it shoot per second
        bounces: does it bounce of the walls (i guess, Aiden forgot to specify that)
        img_path: that's easy
        damage: ....
        deals_area_damage: the purpose is in the name
        damage_r: how far from the collision does the damage reach
        """

        self.proccesses.update({
            name: {
                "damage": damage,
                "area_damage": deals_area_damage,
                "damage_radius": damage_r,
                "can_append": False,
                "repetition_index": 0,
                "bullets": [],
                "fire_rate": fire_rate,
                "prev_shot": 0,
                "bounces": bounces,
                "image": pg.image.load(img_path).convert_alpha(),
            }
        })

    # bullet array structure => [pos, vel, angle, duration, count_down, rect] (I promise this isn't stolen from my particle system ( ͡~ ͜ʖ ͡°))
    # ok - Andrey

    def bullet_process(self, surf, new_bullet, bullet_proccess_name, cam_pos, tiles, mouse_pressed, current_time):
        self.proccesses[bullet_proccess_name]["can_append"] = False
        if mouse_pressed[0] and current_time - self.proccesses[bullet_proccess_name]["prev_shot"] > self.proccesses[bullet_proccess_name]["fire_rate"]:
            self.proccesses[bullet_proccess_name]["can_append"] = True
            self.proccesses[bullet_proccess_name]["prev_shot"] = current_time

        if self.proccesses[bullet_proccess_name]["can_append"]:
            self.proccesses[bullet_proccess_name]["bullets"].append(new_bullet)

        if len(self.proccesses[bullet_proccess_name]["bullets"]) > 0:
            for bullet in self.proccesses[bullet_proccess_name]["bullets"]:
                collided = False

                bullet[0][0] += cos(radians(bullet[2])) * bullet[1][0]
                bullet[5].x = bullet[0][0]
                if self.check_collision(bullet[5], tiles):
                    collided = True
                    if self.proccesses[bullet_proccess_name]["bounces"]:
                        bullet[1][0] *= -0.5
                        bullet[0][0] += bullet[1][0] * 2

                bullet[0][1] += sin(radians(-bullet[2])) * bullet[1][1]
                bullet[5].y = bullet[0][1]
                if self.check_collision(bullet[5], tiles):
                    collided = True
                    if self.proccesses[bullet_proccess_name]["bounces"]:
                        bullet[1][1] *= -0.5
                        bullet[0][1] += bullet[1][1] * 2

                img = pg.transform.rotate(pg.transform.scale(self.proccesses[bullet_proccess_name]["image"], [self.proccesses[bullet_proccess_name]["image"].get_width() * 2, self.proccesses[bullet_proccess_name]["image"].get_height() * 2]), bullet[2])
                surf.blit(img, bullet[0] - cam_pos)

                bullet[3] -= bullet[4]

                if bullet[3] <= 0 or (collided and not self.proccesses[bullet_proccess_name]["bounces"]):
                    self.proccesses[bullet_proccess_name]["bullets"].remove(bullet)

    def check_collision(self, victim_rect, rects_array):
        for rect in rects_array:
            if rect.colliderect(victim_rect):
                return True
        return False
