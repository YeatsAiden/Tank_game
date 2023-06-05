from settings import *


class Player:
    def __init__(self):
        self.image = pg.transform.rotate(pg.transform.scale_by(pg.image.load("assets/images/tank1.png").convert_alpha(), DRAWING_COEFICIENT), -90)
        self.cannon_img = pg.transform.rotate(pg.transform.scale_by(pg.image.load("assets/images/cannon.png").convert_alpha(), DRAWING_COEFICIENT), -90)
        self.cursor_img = pg.transform.scale_by(pg.image.load("assets/images/cursor.png").convert_alpha(), DRAWING_COEFICIENT)

        self.rotation = 0
        self.rotation_offset = pg.Vector2(3, 0)

        self.pos = pg.Vector2(300, 300)

        self.rotation_speed = 270

        self.drifting = False
        self.moving_backwards = False

        self.max_speed = 200
        self.acceleration = 1.5  # m/s^2
        self.velocity = pg.Vector2(0.001, 0.001)

        self.looking = pg.Vector2(cos(radians(self.rotation)), sin(radians(self.rotation))).normalize()

        self.cannon_angle = 0

        self.collision_state = {"right": False, "left": False, "top": False, "bottom": False}
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

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


    def draw(self, surf, cam_pos, mouse_pos, dt):
        self.draw_tank(surf, cam_pos)
        self.draw_cannon(surf, mouse_pos, cam_pos, dt)
        self.draw_cursor(surf, mouse_pos)
    

    def draw_tank(self, surf, cam_pos):
        placeholder_image = self.image  # we need to preserve the original image untouched
        placeholder_image = pg.transform.rotate(placeholder_image, self.rotation)
        placeholder_rect = placeholder_image.get_rect(center=self.rect.center - cam_pos)
        surf.blit(placeholder_image, placeholder_rect)
        

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
        x_change = mouse_pos[0] - self.rect.x + cam_pos[0]
        y_change = mouse_pos[1] - self.rect.y + cam_pos[1]

        angle = degrees(atan2(-y_change, x_change))

        print(angle)

        return angle
    

    def collision_check(self, tiles):
        # Look man I promise this was not stolen :\
        self.collision_state = {"right": False, "left": False, "top": False, "bottom": False}

        self.rect.x += self.velocity.x

        for tile in tiles:
            if tile.colliderect(self.rect):
                if self.velocity.x < 0:
                    self.collision_state['left'] = True
                    self.rect.left = tile.right
                    self.velocity.x = 0

                if self.velocity.x > 0:
                    self.collision_state['right'] = True
                    self.rect.right = tile.left
                    self.velocity.x = 0

        self.rect.y += self.velocity.y

        for tile in tiles:
            if tile.colliderect(self.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = tile.top
                    self.collision_state['bottom'] = True
                    self.velocity.y = 0

                if self.velocity.y < 0:
                    self.rect.top = tile.bottom
                    self.collision_state['top'] = True
                    self.velocity.y = 0
