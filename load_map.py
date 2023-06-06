from settings import *
from game_math import *


# Note I don't care a bit about "YoU CAn ONlY InDEnT YoUR CoDE 4 TiMeS" :p
class Load_map:
    def __init__(self, world_data_path, world_csv_data_paths):
        self.world_csv_data = [[data.split("/")[-1].replace(".csv", ""), pandas.read_csv(data)] for data in world_csv_data_paths]

        self.tile_set_img = pg.image.load("assets/tile_set/tile_set.png").convert_alpha()

        # structure of self.world_tiles = [[layer_name, 2d_tile_array]]
        self.list_of_areas_on_layers_to_be_rendered = []
        self.offset = []
        # Just an array of rects to collide with :Y
        self.world_rects = []

        self.world_image = 0

        self.images_dict = self.make_image_dict(self.tile_set_img)


    def make_rects_array(self, offset, areas_in_layers_to_be_rendered, collision_layers):
        array = []
        for name, layer in areas_in_layers_to_be_rendered:
            y = 0
            for row in layer:
                x = 0
                for tile in row:
                    if tile != -1 and name in collision_layers:
                        rect = pg.FRect((x + offset[0]) * TILE_SIZE - TILE_SIZE, (y + offset[1]) * TILE_SIZE - TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        array.append(rect)
                    x += 1
                y += 1

        return array
    
    def make_image_dict(self, tile_set_img):
        # Find out yourself :\, I already forgor how it works
        tile_img = {}
        for y in range(0, tile_set_img.get_height(), TILE_SIZE):
            for x in range(0, tile_set_img.get_width(), TILE_SIZE):
                img = clip_img(tile_set_img, x, y, TILE_SIZE, TILE_SIZE)

                if self.check_if_sprite_is_not_transparent(img):
                    tile_img[y//TILE_SIZE * tile_set_img.get_width()//TILE_SIZE + x//TILE_SIZE] = img
        
        return tile_img


    def check_if_sprite_is_not_transparent(self, surf):
        for y in range(0, surf.get_height()):
            for x in range(0, surf.get_width()):
                color = surf.get_at((x, y))

                if color[3] > 0:
                    return True
        return False


    def get_area_for_rendering(self, surf, cam_pos, world_csv_data):
        # More stuff, not really interesting ...
        layers = []
        for layer_name, csv_data in world_csv_data:
            starting_row = int(cam_pos[1] // TILE_SIZE) if cam_pos[1] > 0 else 0 
            ending_row = int((cam_pos[1] + surf.get_height()) // TILE_SIZE) + 1 if cam_pos[1] > 0 else surf.get_height() // TILE_SIZE
            starting_column = int(cam_pos[0] // TILE_SIZE)if cam_pos[0] > 0 else 0 
            ending_column = int((cam_pos[0] + surf.get_width()) // TILE_SIZE) + 1 if cam_pos[0] > 0 else surf.get_width() // TILE_SIZE

            area = csv_data.iloc[starting_row:ending_row, starting_column:ending_column]
            layers.append([layer_name, area.values])

            offset_area = csv_data.iloc[0:starting_row + 1, 0:starting_column + 1].values
            offset = [len(offset_area[0]), len(offset_area)]

        return layers, offset
    

    def make_world_image(self, areas_in_layers_to_be_rendered):
        # Kinda CRINGE
        img = pg.Surface((len(areas_in_layers_to_be_rendered[0][1][0]) * TILE_SIZE, len(areas_in_layers_to_be_rendered[0][1]) * TILE_SIZE))
        for name, layer in areas_in_layers_to_be_rendered:
            y = 0
            for row in layer:
                x = 0
                for tile in row:
                    if tile != -1:
                        img.blit(self.images_dict[tile], (x * TILE_SIZE, y * TILE_SIZE))
                    x += 1
                y += 1 
        return img


    def draw_world(self, surf, cam_pos, offset, areas_in_layers_to_be_rendered):
        surf.blit(self.make_world_image(areas_in_layers_to_be_rendered), (0, 0) - cam_pos + [offset[0] * TILE_SIZE, offset[1] * TILE_SIZE] - [TILE_SIZE, TILE_SIZE])
