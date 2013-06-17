import os
import pygame

def load_image(name, colorkey=None):
  try:
    fullname = os.path.join('data', name)
  except AttributeError:
    raise ValueError('Failed to load "None" image')

  try:
    image = pygame.image.load(fullname)
  except pygame.error as e:
    raise SystemExit('failed to load image %s %r' % (fullname, e))

  image = image.convert_alpha()

  if colorkey is not None:
    if colorkey is -1:
      colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
  return image, image.get_rect()
