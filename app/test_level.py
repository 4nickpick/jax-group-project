import os
import sys
import pygame
from pygame import locals

from app.animation import SurfaceAnimation

from app.animation import RectFrame
from app.animation import AnimatedSprite
from app.physics import PhysicsObject
from app.physics import PhysicsManager
from app.physics import TERMINAL_VELOCITY
from app.camera import ScreenCamera as Camera

from contrib.pytmx import tmxloader

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TILE_SIZE = 16
screen_w = TILE_SIZE * 16
screen_h = TILE_SIZE * 16
screen_size = (screen_w, screen_h)


class Player(AnimatedSprite):

  image_file = "megaman.png"
  physics_object = PhysicsObject()

  def __init__(self):
    super(Player, self).__init__()

    run = SurfaceAnimation(
      'run',
      [RectFrame(188, 12, 24, 22),
       RectFrame(218, 10, 16, 24),
       RectFrame(238, 12, 24, 22)],
      total_time=100
    )

    jump = SurfaceAnimation(
      'jump',
      [RectFrame(265, 4, 26, 30)]
    )

    idle = SurfaceAnimation(
      'idle',
      [RectFrame(103, 10, 21, 24, total_time=10000),
       RectFrame(133, 10, 21, 24, total_time=250),
       RectFrame(103, 10, 21, 24, total_time=250),
       RectFrame(160, 10, 20, 24, total_time=400)],
    )

    self.animation_manager.set_animations([run, jump, idle])

    self.update_frame(0)
    self.rect.x = TILE_SIZE
    self.rect.y = TILE_SIZE * 14 - self.rect.height

  def update_physics_object(self, delta):
    self.physics_object.rect = self.rect
    self.physics_object.update(delta)

  def update_animation(self):
    if self.physics_object.velocity_y < 0:
      self.animation_manager.set_animation('jump')
    elif self.physics_object.velocity_y == 0:
      if self.physics_object.velocity_x > 0:
        self.animation_manager.set_animation('run')
      elif self.physics_object.velocity_x < 0:
        self.animation_manager.set_animation('run')

    if self.physics_object.velocity_x > 0:
      self.animation_manager.get_animation().set_flip(False)
    elif self.physics_object.velocity_x < 0:
      self.animation_manager.get_animation().set_flip(True)
    elif self.physics_object.velocity_y == 0:
      last_animation = self.animation_manager.get_animation()
      self.animation_manager.set_animation('idle')

      if last_animation.name != 'idle':
        last_orientation = last_animation.flip
        self.animation_manager.get_animation().set_flip(last_orientation)

  def update(self, delta):
    keys = pygame.key.get_pressed()
    if keys[locals.K_RIGHT]:
      self.physics_object.velocity_x = 125.0
    elif keys[locals.K_LEFT]:
      self.physics_object.velocity_x = -100.0
    else:
      self.physics_object.velocity_x = 0
    if keys[locals.K_z]:
      if self.physics_object.velocity_y is 0:
        self.physics_object.velocity_y = -TERMINAL_VELOCITY / 3

    self.update_animation()
    self.update_frame(delta)
    self.update_physics_object(delta)

  def get_surface(self, delta):
    return


class Level(object):

  camera = Camera(screen_w, screen_h)

  def __init__(self):
    self.map_file = "test_megaman_map.tmx"

    self.map_data = tmxloader.load_pygame(
      os.path.join("data", "maps", self.map_file)
    )
    self.physics_manager = PhysicsManager(self.map_data)

    self.player = Player()
    self.all_sprites = pygame.sprite.RenderPlain((self.player,))

  def render_image(self, surface, image, x, y):
    surface.blit(image, (x + self.camera.offset_x, y + self.camera.offset_y))

  def render_line(self, surface, color, closed, point_list, width=1):
    points = [(i[0] + self.camera.offset_x, i[1] + self.camera.offset_y)
              for i in point_list]
    pygame.draw.lines(surface, color, closed, points, width)

  def render_rect(self, surface, color, rect, width=1):
    new_rect = (
     rect[0] + self.camera.offset_x,
     rect[1] + self.camera.offset_y,
     rect[2], rect[3]
    )
    pygame.draw.rect(surface, color, new_rect, width)

  def draw(self, surface):
    tile_width = self.map_data.tilewidth
    tile_height = self.map_data.tileheight

    for layer in xrange(0, len(self.map_data.tilelayers)):
      for y in xrange(0, self.map_data.height):
        for x in xrange(0, self.map_data.width):
          image = self.map_data.getTileImage(x, y, layer)
          if image:
            self.render_image(surface, image, x * tile_width, y * tile_height)

    for object_group in self.map_data.objectgroups:
      for obj in object_group:
        if hasattr(obj, 'points'):
          points = [(i[0] + obj.x, i[1] + obj.y) for i in obj.points]
          self.render_line(surface, (255, 128, 128), obj.closed, points, 2)
        else:
          self.render_rect(
            surface,
            (255, 128, 128),
            (obj.x, obj.y, obj.width, obj.height),
            2
          )

    self.render_image(
      surface, self.player.image, self.player.rect.x, self.player.rect.y)

  def update(self, delta):
    self.all_sprites.update(delta)
    self.camera.update(self.player.rect, delta)
    self.physics_manager.handle_tile_collision(
      self.player.physics_object, delta)

window_surface = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.update()
pygame.display.flip()
clock = pygame.time.Clock()
level = Level()
pygame.display.set_caption('jax group game: %s' % level.map_file)

frame_number = 0
record = False

while True:
  clock.tick(60)

  for event in pygame.event.get():
    if event.type == locals.QUIT:
      pygame.quit()
      sys.exit()

  level.update(clock.get_time())

  window_surface.fill(BLACK)
  level.draw(window_surface)
  pygame.display.flip()

  if record:
    pygame.image.save(window_surface, 'frames/frame%06i.png' % (frame_number))
    frame_number += 1
