from settings import *


class Load_map:
    def __init__(self, layers):
        self.world_data = load_pygame("assets/world/world.tmx")
        # Makes a list of all the tiles in world
        self.world_tiles = self.make_tiles_array(self.world_data, layers)
        # This is the image that is used to blit the whole world :\
        self.world_img = pg.Surface((self.world_data.width * TILE_SIZE, self.world_data.height * TILE_SIZE))
        self.make_level_img(self.world_data, self.world_img)


    def make_level_img(self, level, surface):
        for i in level.layers:
            for x, y, surf in i.tiles():
                surface.blit(pg.transform.scale_by(surf, DRAWING_COEFICIENT), (x * TILE_SIZE, y * TILE_SIZE))
    

    def draw_level(self, level_img, surface, cam_pos):
        surface.blit(level_img, (0, 0) - cam_pos)


    def make_tiles_array(self, level, collision_layers):
        array = []
        for i in level.layers:
            array = [pg.Rect(x * TILE_SIZE, y * TILE_SIZE, surf.get_width(), surf.get_height()) for x, y, surf in i.tiles() if i.name in collision_layers]
        return array
