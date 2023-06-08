from settings import *
from game_math import *
from projectile import *


class Player:
    def __init__(self):
        self.image = pg.transform.rotate(pg.transform.scale_by(pg.image.load("assets/images/player/tank.png").convert_alpha(), DRAWING_COEFICIENT), -90)
        self.cannon_img = pg.transform.rotate(pg.transform.scale_by(pg.image.load("assets/images/player/cannon.png").convert_alpha(), DRAWING_COEFICIENT), -90)
        self.cursor_img = pg.transform.scale_by(pg.image.load("assets/images/cursor.png").convert_alpha(), DRAWING_COEFICIENT)

        self.rotation = 0
        self.rotation_offset = pg.Vector2(3, 0)

        self.pos = pg.Vector2(100, 100)
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width() - 2, self.image.get_height() - 2)

        self.rotation_speed = 270

        self.drifting = False
        self.moving_backwards = False

        self.max_speed = 200
        self.acceleration = 1.5  # m/s^2
        self.velocity = pg.Vector2(0.001, 0.001)

        self.max_health = 100
        self.health = 100
        self.dead = False

        self.looking = pg.Vector2(cos(radians(self.rotation)), sin(radians(self.rotation))).normalize()

        self.cannon_angle = 0

        self.bullet = Projectile()
        self.bullet_name = "ord_bullet"

        self.bullet.create_proccess("ord_bullet", 1.5, False, "assets/images/player/bullet.png", 25, deals_area_damage=False, damage_r=0, sound=NORMAL_CANNON)
        self.bullet.create_proccess("buff_bullet", 2, False, "assets/images/buff_tank/buff_tank_bullet.png", 50, deals_area_damage=True, damage_r=50, sound=BIG_CHUNGUS)
        self.bullet.create_proccess("minigun_bullet", 0.1, False, "assets/images/mini_gun_tank/mini_gun_tank_bullet.png", 3, deals_area_damage=False, damage_r=0, sound=MINIGUN)
        self.bullet.create_proccess("bomb_bullet", 2, False, "assets/images/buff_tank/buff_tank_bullet.png", 40, deals_area_damage=True, damage_r=20, sound=EL_BOMBE)

        self.bullet_stats = [[self.rect.center[0], self.rect.center[1]], 400, self.cannon_angle, 2, pg.FRect(0, 0, self.bullet.proccesses["ord_bullet"]['image'].get_width(), self.bullet.proccesses["ord_bullet"]['image'].get_height())]
        # -------------------|-----------------position----------------|-velocity-|-rotation-|-lifespan-|-------------------------------------------------------rect----------------------------------------------------------------------|

        self.collided = False

    def move(self, keys_pressed, tiles, dt):
        """
        :param keys_pressed = pg.key.get_pressed() somewhere in the main loop
        :param dt: you know what delta time is :/
        :return:
        """
        self.moving_backwards = False

        if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
            self.velocity.x += 3 * self.acceleration * dt * cos(radians(self.rotation))
            self.velocity.y -= 3 * self.acceleration * dt * sin(radians(self.rotation))

        elif keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
            self.velocity.x -= 6 * self.acceleration* dt * cos(radians(self.rotation))
            self.velocity.y += 6 * self.acceleration* dt * sin(radians(self.rotation))

            self.moving_backwards = True

        else:
            self.velocity.x /= 1.1
            self.velocity.y /= 1.1

        if keys_pressed[pg.K_SPACE]:
            self.drifting = True
        else:
            self.drifting = False

        if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
            self.rotation += self.rotation_speed*dt
        elif keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
            self.rotation -= self.rotation_speed*dt

        # inexplicable sorcery
        self.looking = pg.Vector2.lerp(self.looking, ((-1)**self.moving_backwards)*pg.Vector2(cos(radians(self.rotation)), (-sin(radians(self.rotation)))), 0.05).normalize()

        # limit velocity
        self.velocity = pg.Vector2(0.001, 0.001) if self.velocity.length() == 0 else self.velocity
        self.velocity.clamp_magnitude_ip(self.max_speed*dt)

        # make the movement feel smooth
        self.velocity = pg.Vector2.lerp(self.velocity.normalize(), self.looking, 0.6 if not self.drifting else 0.02) * self.velocity.length()
        # check for collisions and apply movement
        self.collision_check(tiles)

    def check_if_dead(self):
        if self.health <= 0:
            self.dead = True

    def draw(self, surf, cam_pos, mouse_pos, dt):
        self.draw_tank(surf, cam_pos)
        self.draw_cannon(surf, mouse_pos, cam_pos, dt)
        self.draw_cursor(surf, mouse_pos)
    

    def draw_tank(self, surf, cam_pos):
        placeholder_image = self.image  # we need to preserve the original image untouched
        placeholder_image = pg.transform.rotate(placeholder_image, self.rotation)
        placeholder_rect = placeholder_image.get_rect(center=self.rect.center - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)

    def shoot(self, surf, cam_pos, tiles, mouse_pressed, current_time, dt, entities):
        self.bullet_stats = [[self.rect.center[0], self.rect.center[1]], 400, self.cannon_angle, 2, pg.FRect(0, 0, self.bullet.proccesses[self.bullet_name]['image'].get_width(), self.bullet.proccesses[self.bullet_name]['image'].get_height())]
        self.bullet.bullet_process(surf, self.bullet_stats, self.bullet_name, cam_pos, tiles, mouse_pressed, current_time, dt, entities)

    def rotate_cannon(self, mouse_pos, cam_pos, dt):
        desired_cannon_rotation = self.calculate_angle_to_mouse(mouse_pos, cam_pos)
        # complicated math - i can explain it if you need

        smallest_angle = calculate_smallest_angle(self.cannon_angle, desired_cannon_rotation)

        rotation_change = self.rotation_speed * dt * (-1 if smallest_angle < 0 else 1)

        if abs(rotation_change) > abs(smallest_angle):
            self.cannon_angle = desired_cannon_rotation
        else:
            self.cannon_angle += rotation_change

    def draw_cannon(self, surf, mouse_pos, cam_pos, dt):
        self.rotate_cannon(mouse_pos, cam_pos, dt)
        placeholder_image = self.cannon_img 
        placeholder_image = pg.transform.rotate(placeholder_image, self.cannon_angle)
        placeholder_rect = placeholder_image.get_rect(center=self.rect.center + self.rotation_offset.rotate(-self.cannon_angle) - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)
    

    def draw_cursor(self, surf, mouse_pos):
        placeholder_image = self.cursor_img
        placeholder_rect = placeholder_image.get_rect(center=mouse_pos)
        surf.blit(placeholder_image, placeholder_rect)
    

    def calculate_angle_to_mouse(self, mouse_pos, cam_pos):
        x_change = mouse_pos[0] - self.rect.centerx + cam_pos[0]
        y_change = mouse_pos[1] - self.rect.centery + cam_pos[1]

        angle = degrees(atan2(-y_change, x_change))

        return angle
    

    def collision_check(self, tiles):
        # Look man I promise this was not stolen :\
        self.rect.x += self.velocity.x

        collided_this_session = False

        for tile in tiles:
            if tile.colliderect(self.rect):
                collided_this_session = True
                if self.velocity.length() > 1 and not self.collided:
                    CRASHING.play()

                if self.velocity.x < 0:
                    self.rect.left = tile.right
                    self.velocity.x = 0

                if self.velocity.x > 0:
                    self.rect.right = tile.left
                    self.velocity.x = 0

        self.rect.y += self.velocity.y

        for tile in tiles:
            if tile.colliderect(self.rect):
                collided_this_session = True
                if self.velocity.length() > 1 and not self.collided:
                    CRASHING.play()
                if self.velocity.y > 0:
                    self.rect.bottom = tile.top
                    self.velocity.y = 0

                if self.velocity.y < 0:
                    self.rect.top = tile.bottom
                    self.velocity.y = 0

        self.collided = collided_this_session
