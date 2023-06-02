from settings import *


class Player:
    def __init__(self):
        self.image = pg.transform.rotate(pg.transform.scale_by(pg.image.load("assets/images/tank1.png"), 2), -90)
        self.cannon_img = pg.transform.rotate(pg.transform.scale_by(pg.image.load("assets/images/cannon.png"), 2), -90)

        self.rotation = 90
        self.rotation_offset = pg.Vector2(8, 0)
        self.pos = pg.Vector2(100, 100)

        self.rotation_speed = 270

        self.drifting = False
        self.moving_backwards = False

        self.max_speed = 400
        self.acceleration = 1.5  # m/s^2
        self.velocity = pg.Vector2(0.000001, 0.000001)

        self.looking = pg.Vector2(cos(radians(self.rotation)), sin(radians(self.rotation))).normalize()

        self.cannon_angle = 0

    def move(self, keys_pressed, dt):
        """
        :param keys_pressed = pg.key.get_pressed() somewhere in the main loop
        :param dt: you know what delta time is
        :return:
        """
        self.moving_backwards = False

        if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
            self.velocity.x += 3 * self.acceleration * dt * cos(radians(self.rotation))
            self.velocity.y -= 3 * self.acceleration * dt * sin(radians(self.rotation))

        elif keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
            self.velocity.x -= 6 * self.acceleration*dt * cos(radians(self.rotation))
            self.velocity.y += 6 * self.acceleration*dt * sin(radians(self.rotation))

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
        self.velocity = pg.Vector2(0.000001, 0.000001) if self.velocity.length() == 0 else self.velocity
        self.velocity.clamp_magnitude_ip(self.max_speed*dt)

        # make the movement feel smooth
        self.velocity = pg.Vector2.lerp(self.velocity.normalize(), self.looking, 0.6 if not self.drifting else 0.02) * self.velocity.length()

        # apply the movement
        self.pos[0] += self.velocity.x - 0.000001  # to make the tank not slowly move......
        self.pos[1] += self.velocity.y - 0.000001


    def draw(self, surf, cam_pos, mouse_pos, dt):
        self.draw_tank(surf, cam_pos)
        self.draw_cannon(surf, mouse_pos, cam_pos, dt)
    

    def draw_tank(self, surf, cam_pos):
        placeholder_image = self.image  # we need to preserve the original image untouched
        placeholder_image = pg.transform.rotate(placeholder_image, self.rotation)
        placeholder_rect = placeholder_image.get_rect(center=self.pos - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)

    def rotate_cannon(self, mouse_pos, cam_pos, dt):
        if self.cannon_angle < 0:
            self.cannon_angle += 360
        elif self.cannon_angle > 360:
            self.cannon_angle -= 360

        desired_cannon_rotation = self.calculate_angle_to_mouse(mouse_pos, cam_pos)
        if desired_cannon_rotation < 0:
            desired_cannon_rotation += 360
        # complicated math - i can explain it if you need
        self.cannon_angle += ((-1)**(sin(radians(self.cannon_angle)) >= sin(radians(-desired_cannon_rotation))) * (-1)**(cos(radians(self.cannon_angle)) >= cos(radians(desired_cannon_rotation))) * self.rotation_speed * dt) if abs(desired_cannon_rotation - self.cannon_angle) > 2 else 0
        print(abs(desired_cannon_rotation - self.cannon_angle), desired_cannon_rotation, self.cannon_angle)

    def draw_cannon(self, surf, mouse_pos, cam_pos, dt):
        self.rotate_cannon(mouse_pos, cam_pos, dt)
        placeholder_image = self.cannon_img 
        placeholder_image = pg.transform.rotate(placeholder_image, self.cannon_angle)
        placeholder_rect = placeholder_image.get_rect(center=self.pos + self.rotation_offset.rotate(-self.cannon_angle) - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)
    

    def calculate_angle_to_mouse(self, mouse_pos, cam_pos):
        x_change = mouse_pos[0] - self.pos[0] + cam_pos[0]
        y_change = mouse_pos[1] - self.pos[1] + cam_pos[1]

        return degrees(atan2(-y_change, x_change))
