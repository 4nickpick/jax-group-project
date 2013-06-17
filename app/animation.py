from core import animation
from core.utils import load_image
import pygame


class RectFrame(animation.Frame):
  """
  A frame class that contains the pygame Rect class instance
  to represent a single frame in an image.
  """

  def __init__(self, x, y, w, h, total_time=200, callbacks=[]):
    self.rect = pygame.Rect(x, y, w, h)
    super(RectFrame, self).__init__(
      total_time=total_time, callbacks=callbacks
    )


class AnimatedSprite(pygame.sprite.Sprite):
  """
  A useful helper class to encapsulate pygame image loading
  and etc..
  """

  animation_manager = animation.AnimationManager()
  image_file = None

  def __init__(self, image_file=None):
    pygame.sprite.Sprite.__init__(self)
    if image_file:
      self.image_file = image_file
    if self.image_file:
      self.set_image(image_file)
    if self._image is None:
      raise ValueError("Image value cannot be none for an animated sprite")

  def set_image(self, image_file):
    if image_file:
      self.image_file = image_file
    self._image, self.rect = load_image(self.image_file)

  def update(self, delta):
    """
    Note: 
      self._image is a reference kept to get subsurfaces
      May want to cache subsurfaces in the future if it's too slow
    """
    frame = self.animation_manager.get_next_frame(delta)
    if frame:
      self.image = self._image.subsurface(frame.rect)
