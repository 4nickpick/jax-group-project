import pygame, sys, os
from pygame.locals import *

from core.animation import AnimationManager
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

tile_w = 32
tile_h = 32
tile_size = (tile_w, tile_h)

grid_w = screen_w / tile_w
grid_h = screen_h / tile_h
grid_size = (grid_w, grid_h)

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
    
class Level():

  def __init__(self):
    self.map_file = "test_map.tmx" 
    self.map_data = tmxloader.load_pygame(os.path.join("data", "maps", self.map_file))
        
  def draw(self,screen):
    #test out the tmx format - draws 3 layers of tmx
      for layer in range (0,3):
        for x in range(0,grid_w):
          for y in range(0,grid_h):
            image = self.map_data.getTileImage(x, y, layer)
            if image != 0:
              screen.blit(image, (x*tile_w,y*tile_h))

window_surface = pygame.display.set_mode(screen_size, 0, 32) #abstracted screen size
window_surface.fill(WHITE)
pygame.display.set_caption('Jax group game')
pygame.display.update()
pygame.display.flip()
clock = pygame.time.Clock()

dude = Dude()
level = Level() #not a sprite per se, so not added to all_sprites
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
