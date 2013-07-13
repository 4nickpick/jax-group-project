from core.collision import CollisionMap


class TileCollisionMap(CollisionMap):

  def __init__(self, map_data):
    self.collision_map = map_data
    self.TILE_SIZE = map_data.tileheight * map_data.tilewidth

  def get_tile(self, x, y):
    tile_type = self.collision_map.getTileImage(x, y, 0)
    return bool(tile_type)
