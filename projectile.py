from settings import *
from particle import Particle


class Projectile:
    def __init__(self):
        self.proccesses = {}
        self.smoke_image = pg.image.load("assets/images/smoke.png")

    # "dirt_explosion", 2, True, False, dirt_img, 0.1     - ?????????
    # uuuuuuuuuuuuhhhhh, forgor to delete that
    def create_proccess(self, name, fire_rate, bounces, img_path, damage=0, deals_area_damage=False, damage_r=0, sound=None):
        """
        name; name of the process
        fire_rate: how fast does it shoot per second
        bounces: does it bounce of the walls (i guess, Aiden forgot to specify that)
        img_path: that's easy
        damage: ....
        deals_area_damage: the purpose is in the name
        damage_r: how far from the collision does the damage reach
        sound: pg.mixer.Sound("whatever")
        """
        # I don't like documenting code 🙄

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
                "sound": sound,
                "particle_processes":  [],
                "particle_indexes": []
            }
        })

    # bullet array structure => [pos, vel, angle, duration, rect] (I promise this isn't stolen from my particle system ( ͡~ ͜ʖ ͡°))
    # ok - Andrey

    def bullet_process(self, surf, new_bullet, bullet_proccess_name, cam_pos, tiles, mouse_pressed, current_time, dt, entities=None):
        screen_shake = 0

        if entities is None:
            entities = []

        if mouse_pressed[0] and current_time - self.proccesses[bullet_proccess_name]["prev_shot"] > self.proccesses[bullet_proccess_name]["fire_rate"]:
            particle = Particle()
            particle.create_proccess("explosion", 2, True, False, False, 20)

            self.proccesses[bullet_proccess_name]["prev_shot"] = current_time
            self.proccesses[bullet_proccess_name]["bullets"].append(new_bullet)
            self.proccesses[bullet_proccess_name]["particle_processes"].append(particle)

            screen_shake += 0.2

            self.proccesses[bullet_proccess_name]["sound"].play()


        if len(self.proccesses[bullet_proccess_name]["bullets"]) > 0:
            for index, bullet in enumerate(self.proccesses[bullet_proccess_name]["bullets"]):
                collided = False

                # check collisions with the static environment, such as Joe mama
                bullet[0][0] += cos(radians(bullet[2])) * bullet[1] * dt
                bullet[4].topleft = bullet[0]
                if self.check_collision(bullet[4], tiles):
                    collided = True
                    if self.proccesses[bullet_proccess_name]["bounces"]:
                        EL_BOMBE.play()
                        bullet[1][0] *= -0.5
                        bullet[0][0] += bullet[1][0] * 2
                    else:
                        DESTRUCTION_OF_TURRET.play()

                bullet[0][1] += sin(radians(-bullet[2])) * bullet[1] * dt
                bullet[4].topleft = bullet[0]
                if self.check_collision(bullet[4], tiles): 
                        collided = True
                        if self.proccesses[bullet_proccess_name]["bounces"]:
                            EL_BOMBE.play()
                            bullet[1][1] *= -0.5
                            bullet[0][1] += bullet[1][1] * 2
                        else:
                            DESTRUCTION_OF_TURRET.play()

                # check if the bullet collided with any entities
                for entity in entities:
                    if not collided:
                        if bullet[4].colliderect(entity):
                            entity.health -= self.proccesses[bullet_proccess_name]["damage"]
                            collided = True
                    elif self.proccesses[bullet_proccess_name]["area_damage"]:
                        distance = dist(entity.rect.center, bullet[4].center)
                        if distance <= self.proccesses[bullet_proccess_name]["damage_radius"]:
                            entity.health -= self.proccesses[bullet_proccess_name]["damage"]*abs(sin(acos(distance/self.proccesses[bullet_proccess_name]["damage_radius"])))

                # draw the bullet
                img = pg.transform.rotate(pg.transform.scale_by(self.proccesses[bullet_proccess_name]["image"], DRAWING_COEFICIENT), bullet[2])
                surf.blit(img, bullet[0] - cam_pos)

                # reduce the lifespan of the bullet
                bullet[3] -= dt

                # delete the bullet if it died
                if bullet[3] <= 0 or (collided and not self.proccesses[bullet_proccess_name]["bounces"]):
                    self.proccesses[bullet_proccess_name]["bullets"].remove(bullet)
                    
                    self.proccesses[bullet_proccess_name]["particle_indexes"].append([len(self.proccesses[bullet_proccess_name]["particle_processes"]) - 1, bullet[0]])
                    screen_shake += 0.05
                    
                    
        for index, pos in self.proccesses[bullet_proccess_name]["particle_indexes"]:
            self.proccesses[bullet_proccess_name]["particle_processes"][index].particle_process(surf, [[pos[0], pos[1]], [random.randint(-50, 50), random.randint(-50, 50)], random.randint(10, 20) , -0.2, 3, pg.FRect(pos[0], pos[1], 1, 1), self.smoke_image], "explosion", cam_pos, tiles, dt)
            
        return screen_shake

    def check_collision(self, victim_rect, rects_array):
        for rect in rects_array:
            if rect.colliderect(victim_rect):
                return True
        return False
