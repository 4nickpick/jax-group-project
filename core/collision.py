
class CollisionMap(object):
  COLLISION = 1
  collision_map = []

  def get_tile(self, x, y):
    tile_type = self.collision_map[x][y]
    return tile_type

  def collision(self, x, y):
    tile_type = self.get_tile(x, y)
    return tile_type == self.COLLISION


class CollisionHandler(object):

  def __init__(self, collision_map, tilesize=16):
    self.collision_map = collision_map
    self.TILE_SIZE = tilesize

  def collision_horiz_down(self, x, y, width):
    tile_pixels = x - (x % self.TILE_SIZE)
    test_end = x + width

    tile_y = y / self.TILE_SIZE
    tile_x = tile_pixels / self.TILE_SIZE

    while tile_pixels < test_end:
      if self.collision_map.collision(tile_x, tile_y):
        return tile_y
      else:
        tile_x += 1
        tile_pixels += self.TILE_SIZE

    return None

  def collision_horiz_up(self, x, y, width):
    tile_pixels = x - (x % self.TILE_SIZE)
    test_end = x + width

    tile_y = y / self.TILE_SIZE
    tile_x = tile_pixels / self.TILE_SIZE

    while tile_pixels < test_end:
      if self.collision_map.collision(tile_x, tile_y):
        return tile_y
      else:
        tile_x += 1
        tile_pixels += self.TILE_SIZE

    return None

  def collision_vert(self, x, y, height):
    tile_pixels = y - (y % self.TILE_SIZE)
    test_end = y + height

    tile_x = x / self.TILE_SIZE
    tile_y = tile_pixels / self.TILE_SIZE

    while tile_pixels < test_end:
      if self.collision_map.collision(tile_x, tile_y):
        return tile_x
      else:
        tile_y += 1
        tile_pixels += self.TILE_SIZE

    return None
