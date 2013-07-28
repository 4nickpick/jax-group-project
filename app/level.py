import os
import pygame

from app.physics import PhysicsManager
from app.camera import ScrollCamera as Camera
from app.renderer import *

from contrib.pytmx import tmxloader


class Level(object):

  camera = Camera(SCREEN_W, SCREEN_H)

  def __init__(self, player):
    self.map_file = "test_megaman_map.tmx"

    self.map_data = tmxloader.load_pygame(
      os.path.join("data", "maps", self.map_file)
    )
    self.physics_manager = PhysicsManager(self.map_data)

    self.player = player
    self.all_sprites = pygame.sprite.RenderPlain((self.player,))

  def draw(self, surface):
    tile_width = self.map_data.tilewidth
    tile_height = self.map_data.tileheight

    for layer in xrange(0, len(self.map_data.tilelayers)):
      for y in xrange(0, self.map_data.height):
        for x in xrange(0, self.map_data.width):
          image = self.map_data.getTileImage(x, y, layer)
          if image:
            render_image(
              surface, image, x * tile_width, y * tile_height, self.camera)

    for object_group in self.map_data.objectgroups:
      for obj in object_group:
        if hasattr(obj, 'points'):
          points = [(i[0] + obj.x, i[1] + obj.y) for i in obj.points]
          render_line(
            surface, (255, 128, 128), obj.closed, points, self.camera, 2)
        else:
          render_rect(
            surface,
            (255, 128, 128),
            (obj.x + self.camera.offset_x,
             obj.y + self.camera.offset_y,
             obj.width,
             obj.height)
          )

          #    ui_context = PygameGUIContext(PygameUIRenderer(surface))

    render_image(
      surface,
      self.player.image,
      self.player.rect.x,
      self.player.rect.y,
      self.camera
    )

  def update(self, delta):
    self.all_sprites.update(delta)
    self.camera.update(self.player.rect, delta)
    self.physics_manager.handle_tile_collision(
      self.player.physics_object, delta)

  def do_ui(self):
    #if button(self.ui_context, 0, 0, 50, 20):
      #print 'hi'
    pass

  def add_sprite(self, new_sprite):
    self.all_sprites.add(new_sprite)
