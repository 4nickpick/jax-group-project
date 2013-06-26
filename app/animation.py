from core import animation
from core.utils import load_image
import pygame


class FloatRect(pygame.Rect):
  def set_x(self, x):
    self._x = x

  def get_x(self):
    return round(self._x)

  x = property(get_x, set_x)


class RectFrame(animation.Frame):
  """
  A frame class that contains the pygame Rect class instance
  to represent a single frame in an image.
  """

  def __init__(self, x, y, w, h, total_time=200, callbacks=[]):
    self.rect = FloatRect(x, y, w, h)
    self.image = None
    super(RectFrame, self).__init__(
      total_time=total_time, callbacks=callbacks
    )

  def flip(self):
    if self.image:
      self.image = pygame.transform.flip(self.image, 1, 0)

  def get_subsurface(self, image):
    if not self.image:
      self.image = image.subsurface(self.rect)
    return self.image


class SurfaceAnimation(animation.Animation):

  flip = False

  def set_flip(self, flip):
    if self.flip != flip:
      self.flip = flip
      for frame in self.frames:
        frame.flip()


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

  def update_frame(self, delta):
    frame = self.animation_manager.get_next_frame(delta)
    if frame:
      self.image = frame.get_subsurface(self._image)

      old_rect = self.rect
      self.rect = self.image.get_rect()

      self.rect.x = old_rect.x
      self.rect.y = old_rect.y + (old_rect.height - self.rect.height)

  def update(self, delta):
    """
    Note:
      self._image is a reference kept to get subsurfaces
      May want to cache subsurfaces in the future if it's too slow
    """
    self.update_frame(delta)
