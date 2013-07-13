import pygame
from app.collision import TileCollisionMap
from core.collision import CollisionHandler

GRAVITY = 800
TERMINAL_VELOCITY = 700


class PhysicsObject(object):
  """
  Physics object holds properties for a physics object
  """
  velocity_x = 0.0
  velocity_y = 0.0
  mass = 0.0
  rect = pygame.Rect(0, 0, 0, 0)

  def transform_gravity(self, delta):
    self.velocity_y += (float(delta) / 1000) * GRAVITY
    if self.velocity_y > TERMINAL_VELOCITY:
      self.velocity_y = TERMINAL_VELOCITY

  def transform_position(self, delta):
    self.rect.y = float(self.rect.y) + self.velocity_y * delta / 1000
    self.rect.x = float(self.rect.x) + self.velocity_x * delta / 1000

  def update(self, delta):
    self.transform_gravity(delta)
    self.transform_position(delta)


class PhysicsManager(object):

  def __init__(self, map_data):
    self.collision_map = TileCollisionMap(map_data)
    self.collision_manager = CollisionHandler(
      self.collision_map,
      tilesize=map_data.tileheight
    )
    self.TILE_SIZE = self.collision_manager.TILE_SIZE

  def handle_tile_collision(self, phys_object, delta):
    tile_x = None
    tile_y = None

    if phys_object.velocity_x > 0:
      tile_x = self.collision_manager.collision_vert(
         phys_object.rect.x + phys_object.rect.width,
         phys_object.rect.y,
         phys_object.rect.height
      )

      if tile_x is not None:
        phys_object.rect.x = (
          (tile_x * self.TILE_SIZE) - phys_object.rect.width
        )
    elif phys_object.velocity_x < 0:
      tile_x = self.collision_manager.collision_vert(
         phys_object.rect.x,
         phys_object.rect.y,
         phys_object.rect.height
      )

      if tile_x is not None:
        phys_object.rect.x = (tile_x + 1) * self.TILE_SIZE

    if phys_object.velocity_y < 0:
      tile_y = self.collision_manager.collision_horiz_up(
         phys_object.rect.x,
         phys_object.rect.y,
         phys_object.rect.width
      )

      if tile_y is not None:
        phys_object.rect.y = (tile_y + 1) * self.TILE_SIZE
        phys_object.velocity_y = - phys_object.velocity_y / 2
    else:
      tile_y = self.collision_manager.collision_horiz_down(
         phys_object.rect.x,
         phys_object.rect.y + phys_object.rect.height,
         phys_object.rect.width
      )

      if tile_y is not None:
        phys_object.rect.y = (
          (tile_y * self.TILE_SIZE) - phys_object.rect.height
        )
        phys_object.velocity_y = 0
