"""
Immediate Mode Graphics User Interface
A declaritive, top down approach to user interfaces

Usage:
  >>> class MyContext(UIContext):
  >>>   # implement methods
  >>>   pass
  >>> ui_context = MyContext(window_surface)
  >>> ui_context.prepare()
  >>> if ui_context.button('button_1', 0, 0, text="Quit"):
  >>>   window.exit()
  >>> if ui_context.text_field('text_field', rect=(85, 0, 100, 30)):
  >>>   do_something_else_on_text_change()
  >>> ui_context.finish()
"""


class UIContext(object):
  """
  Base class for UI context
  """

  hot_item = None
  active_item = None
  keyboard_item = None
  key_down = None
  key_char = None
  text = {}
  surface = None

  def __init__(self, surface):
    self.surface = surface

  def prepare(self):
    self.hot_item = None

  def finish(self):
    if not self.get_mouse_press():
      self.active_item = None
    elif self.active_item is None:
      self.active_item = -1

    if self.get_tab_press():
      self.keyboard_item = None

    self.key_down = None
    self.key_char = None

  def is_hot(self, unique_id):
    return self.hot_item == unique_id

  def is_active(self, unique_id):
    return self.active_item == unique_id

  def has_keyboard_focus(self, unique_id):
    return self.keyboard_item == unique_id

  def check_and_set_hotness(self, unique_id, rect):
    raise NotImplementedError

  def check_and_set_keyboard_focus(self, unique_id):
    raise NotImplementedError

  def pressed_widget(self, unique_id):
    raise NotImplementedError

  def get_mouse_press(self):
    raise NotImplementedError

  def get_tab_press(self):
    raise NotImplementedError
