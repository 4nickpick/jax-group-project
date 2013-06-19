import sys
import os
import pygame
from pygame.locals import QUIT

from core.animation import Animation

from app.animation import RectFrame
from app.animation import AnimatedSprite

from contrib.pytmx import tmxloader

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen_w = 640
screen_h = 480
screen_size = (screen_w, screen_h)


class Dude(AnimatedSprite):

  image_file = "megaman.png"

  def __init__(self):
    super(Dude, self).__init__()

    self.animation_manager.set_animations(
      [
        Animation(
          'run_right',
          [RectFrame(188, 12, 24, 24),
           RectFrame(218, 10, 16, 24),
           RectFrame(238, 12, 24, 24)]
        ),
      ]
    )


class Level(object):

  def __init__(self):
    self.map_file = "test_map.tmx"
    self.map_data = tmxloader.load_pygame(
      os.path.join("data", "maps", self.map_file)
    )

  def draw(self, surface):
    tile_width = self.map_data.tilewidth
    tile_height = self.map_data.tileheight
    for layer in xrange(0, len(self.map_data.tilelayers)):
      for y in xrange(0, self.map_data.height):
        for x in xrange(0, self.map_data.width):
          image = self.map_data.getTileImage(x, y, layer)
          if image:
            surface.blit(image, (x * tile_width, y * tile_height))


window_surface = pygame.display.set_mode(screen_size, 0, 32)
window_surface.fill(WHITE)
pygame.display.set_caption('Jax group game')
pygame.display.update()
pygame.display.flip()
clock = pygame.time.Clock()

dude = Dude()
level = Level()
all_sprites = pygame.sprite.RenderPlain((dude,))


while True:
  clock.tick(60)

  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  all_sprites.update(clock.get_time())

  window_surface.fill(WHITE)
  level.draw(window_surface)
  all_sprites.draw(window_surface)
  pygame.display.flip()
