
class Singleton(type):
  """
  We only want one instance of a singleton
  """
  _instances = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]


class UIContext(object):
  """
  The interface state
  """
  __metaclass__ = Singleton

  mouse_x = 0
  mouse_y = 0
  mouse_down = False

  hot_item = 0
  active_item = 0

  keyboard_item = 0
  keyboard_focus = 0
  key_entered = 0
  key_mod = 0
  key_char = 0

  last_widget = 0

  def __init__(self, renderer):
    self.renderer = renderer

  def prepare(self):
    """
    Prepare GUI
    """
    self.hot_item = 0

  def finish(self):
    """
    Finish GUI
    """
    if not self.mouse_down:
      self.active_item = 0
    elif self.active_item == 0:
      self.active_item = -1

    if self.key_entered == 'TAB':
      self.keyboard_item = 0

    self.key_entered = 0
    self.key_char = 0

  def region_hit(self, x, y, width, height):
    hit = True
    if (self.mouse_x < x or
        self.mouse_y < y or
        self.mouse_x >= x + width or
       self.mouse_y >= y + height):
      hit = False
    return hit

  def event_poll(self, event):
    """
    Go through events
    """
    raise NotImplementedError

  def key_pressed(self, key):
    """
    Return whether the user pressed the key
    """
    raise NotImplementedError


class UIRenderer(object):

  def draw_rect(self, x, y, width, height, color):
    """
    """
    raise NotImplementedError

  def draw_line(self):
    """
    """
    raise NotImplementedError

  def draw_char(self):
    """
    """
    raise NotImplementedError

  def draw_string(self):
    """
    """
    raise NotImplementedError


def button(context, ui_id, x, y, text=None):
  """
  Render a button, return true on press, else false
  """
  height = 24
  width = 64

  if context.region_hit(x, y, width, height):
    context.hot_item = ui_id
    if context.active_item == 0 and context.mouse_down:
      context.active_item = ui_id

  if context.keyboard_item == 0:
    context.keyboard_item = ui_id

  if context.keyboard_item == ui_id:
    context.renderer.draw_rect(
      x - 6, y - 6, width + 20, height + 20, '0xff00ff'
    )

  context.renderer.draw_rect(x + 8, y + 8, width, height, '0x000000')

  if context.hot_item == ui_id:
    if context.active_item == ui_id:
      context.renderer.draw_rect(x + 2, y + 2, width, height, '0xffffff')
    else:
      context.renderer.draw_rect(x, y, width, height, '0xffffff')
  else:
    context.renderer.draw_rect(x, y, width, height, '0xaaaaaa')

  if text:
    context.draw_string(text, x + len(text), y + height / 4)

  if context.keyboard_item == ui_id:
    if context.key_pressed('TAB'):
      context.keyboard_item = 0

      if 'SHIFT' in context.key_mod:
        context.keyboard_item = context.last_widget

      context.key_entered = 0

    if context.key_pressed('RETURN'):
      return True

  context.last_widget = ui_id

  if (context.mouse_down and
      context.hot_item == ui_id and
     context.active_item == ui_id):
    return True

  return False
