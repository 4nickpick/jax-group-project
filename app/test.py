import pygame, sys, os
from pygame.locals import *

from core.animation import AnimationManager
from core.animation import Animation

from app.animation import RectFrame
from app.animation import AnimatedSprite


pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


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

window_surface = pygame.display.set_mode((640, 480), 0, 32)
window_surface.fill(WHITE)
pygame.display.set_caption('Jax group game')
pygame.display.update()
pygame.display.flip()
clock = pygame.time.Clock()

dude = Dude()
all_sprites = pygame.sprite.RenderPlain((dude,))

while True:
  clock.tick(60)

  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  all_sprites.update(clock.get_time())

  window_surface.fill(WHITE)
  all_sprites.draw(window_surface)
  pygame.display.flip()
