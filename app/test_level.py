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
from app.level import Level
from app.camera import ScrollCamera as Camera
from app.player import Player
from app.enemy import Enemy

from app.renderer import *

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

window_surface = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
pygame.display.update()
pygame.display.flip()
clock = pygame.time.Clock()

enemy = Enemy()
level = Level(enemy)

pygame.display.set_caption('JaxVGDG Project: %s' % level.map_file)

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
