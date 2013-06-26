from pygame import Rect


class Camera(object):
  def __init__(self, width, height):
    self.state = Rect(0, 0, width, height)

  def update(self, target_rect, delta):
    pass

  @property
  def offset_x(self):
    return self.state.x

  @property
  def offset_y(self):
    return self.state.y


class ScrollCamera(Camera):

  def update(self, target_rect, delta):
    x = -target_rect.x + self.state.width / 2
    y = -target_rect.y + self.state.height / 2

    x = min(0, x)
    x = max(-(self.state.width - self.state.width / 2), x)
    y = max(-(self.state.height - self.state.height / 2), y)

    self.state = Rect(x, y, self.state.width, self.state.height)


class ScreenCamera(Camera):

  def update(self, target_rect, delta):

    left_face = target_rect.x + self.state.x
    top_face = target_rect.y + self.state.y

    if left_face > self.state.width:
      self.state.x -= self.state.width
    elif left_face < 0:
      self.state.x += self.state.width

    if top_face > self.state.height:
      self.state.y -= self.state.height
    elif top_face < 0:
      self.state.y += self.state.height
