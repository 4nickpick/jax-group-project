import sys
import pygame
from pygame import locals


from app.level import Level
from app.imgui import PygameUIContext
from app.enemy import Enemy

from app.renderer import *

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

window_surface = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
ui_context = PygameUIContext(window_surface)
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
    ui_context.process_event(event)

  level.update(clock.get_time())

  window_surface.fill(BLACK)
  level.draw(window_surface)

  ui_context.prepare()
  if ui_context.button('button_1', 0, 0, text="Quit"):
    pygame.quit()
    sys.exit()
  if ui_context.text_field('text_field', rect=(85, 0, 100, 30)):
    pass
  ui_context.finish()

  pygame.display.flip()

  if record:
    pygame.image.save(window_surface, 'frames/frame%06i.png' % (frame_number))
    frame_number += 1
