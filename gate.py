from settings import *

class Gate:
    def __init__(self, img_paths, pos):
        self.image_closed = pg.image.load(img_paths[0]).convert_alpha()
        self.image_opened = pg.image.load(img_paths[1]).convert_alpha()
        self.rect = self.image_closed.get_rect(topleft = pos - [3, 3])
        self.closed = True
    

    def draw(self, surf, cam_pos):
        if self.closed:
            surf.blit(self.image_closed, self.rect.topleft - cam_pos)
        else:
            surf.blit(self.image_opened, self.rect.topleft - cam_pos)
            self.rect.width = 0
            self.rect.height = 0