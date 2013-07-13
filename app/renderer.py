import pygame

from app.camera import ScrollCamera as Camera

TILE_SIZE = 16
SCREEN_W = TILE_SIZE * 16
SCREEN_H = TILE_SIZE * 16
SCREEN_SIZE = (SCREEN_W, SCREEN_H)

def render_image(surface, image, x, y, camera):
  surface.blit(image, (x + camera.offset_x, y + camera.offset_y))

def render_line(surface, color, closed, point_list, camera, width=1):
  points = [(i[0] + camera.offset_x, i[1] + camera.offset_y)
            for i in point_list]
  pygame.draw.lines(surface, color, closed, points, width)

def render_rect(surface, color, rect, camera, width=1):
  new_rect = (
   rect[0] + camera.offset_x,
   rect[1] + camera.offset_y,
   rect[2], rect[3]
  )
  pygame.draw.rect(surface, color, new_rect, width)