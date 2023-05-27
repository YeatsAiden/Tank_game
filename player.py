from settings import *


class Player:
    def __init__(self):
        self.image = pg.transform.rotate(pg.transform.scale_by(pg.image.load("assets/images/tank1.png"), 2), -90)
        self.rotation = 90
        self.pos = [100, 100]

        self.rotation_speed = 270

        self.drifting = False
        self.moving_backwards = False

        self.max_speed = 5
        self.acceleration = 1.5  # m/s^2
        self.velocity = pg.Vector2(0.001, 0.001)

        self.looking = pg.Vector2(cos(radians(self.rotation)), sin(radians(self.rotation))).normalize()

    def move(self, keys_pressed, dt):
        """
        :param keys_pressed = pg.key.get_pressed() somewhere in the main loop
        :param dt: you know what delta time is
        :return:
        """
        self.moving_backwards = False

        if keys_pressed[pg.K_UP]:
            self.velocity.x += 3 * self.acceleration * dt * cos(radians(self.rotation))
            self.velocity.y -= 3 * self.acceleration * dt * sin(radians(self.rotation))

        elif keys_pressed[pg.K_DOWN]:
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

        if keys_pressed[pg.K_LEFT]:
            self.rotation += self.rotation_speed*dt
        elif keys_pressed[pg.K_RIGHT]:
            self.rotation -= self.rotation_speed*dt


        self.looking = pg.Vector2.lerp(self.looking, ((-1)**self.moving_backwards)*pg.Vector2(cos(radians(self.rotation)), (-sin(radians(self.rotation)))), 0.05).normalize()

        # limit velocity
        self.velocity = pg.Vector2(0.001, 0.001) if self.velocity.length() == 0 else self.velocity
        self.velocity.clamp_magnitude(self.max_speed*dt)

        # make the movement feel smooth
        self.velocity = pg.Vector2.lerp(self.velocity.normalize(), self.looking, 0.6 if not self.drifting else 0.02) * self.velocity.length()

        # apply the movement
        self.pos[0] += self.velocity.x
        self.pos[1] += self.velocity.y


    def draw(self, surf, cam_pos):
        placeholder_image = self.image  # we need to preserve the original image untouched
        placeholder_image = pg.transform.rotate(placeholder_image, self.rotation)
        placeholder_rect = placeholder_image.get_rect()
        placeholder_rect.center = self.pos

        placeholder_rect[0] -= (cam_pos[0] - DIS_W//2)
        placeholder_rect[1] -= (cam_pos[1] - DIS_H//2)

        surf.blit(placeholder_image, placeholder_rect)
