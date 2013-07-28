import pygame
from pygame import locals

from core.imgui import UIContext


class PygameUIContext(UIContext):
  """
  An immediate mode graphical user interface implentation for pygame
  """

  font = None

  def __init__(self, surface):
    super(PygameUIContext, self).__init__(surface)
    self.font = pygame.font.Font(pygame.font.get_default_font(), 11)

  def check_and_set_hotness(self, unique_id, rect):
    """
    When the user mouses over the widget, the widget is now 'hot'
    When the widget is 'hot' and the user releases the mouse button,
    that means the user just clicked the widget and now that widget is
    'active'.
    """
    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()[0]
    new_rect = pygame.rect.Rect(rect)

    if pygame.mouse.get_focused():
      if new_rect.collidepoint(mouse_pos):
        self.hot_item = unique_id
        if self.active_item is None and mouse_press:
          self.active_item = unique_id

  def check_and_set_keyboard_focus(self, unique_id):
    """
    If the keyboard focus is None, then the first widget declared
    recieves focus. If the user clicks the widget, then we change
    the keyboard focus to the clicked widget
    """
    if self.keyboard_item is None:
      self.keyboard_item = unique_id
    elif self.pressed_widget(unique_id):
      self.keyboard_item = unique_id

  def pressed_widget(self, unique_id):
    """
    Check if the user clicked the widget
    """
    is_activated = False
    if self.hot_item == unique_id and self.active_item == unique_id:
      if not pygame.mouse.get_pressed()[0]:
        is_activated = True
    return is_activated

  def get_mouse_press(self):
    """
    Check if the user clicked mouse button 1 (left click)
    """
    return pygame.mouse.get_pressed()[0]

  def get_tab_press(self):
    """
    Check if user pressed 'Tab' useful for keyboard focus switching
    """
    if self.key_down:
      if self.key_down.key == locals.K_TAB:
        self.keyboard_item = None

  def button(self, unique_id, x=0, y=0, text=None, rect=None):
    """
    Render a button widget
    """
    if rect is None:
      rect = pygame.Rect(x, y, 80, 30)
    color = (100, 0, 0)

    self.check_and_set_hotness(unique_id, rect)
    self.check_and_set_keyboard_focus(unique_id)

    if self.is_hot(unique_id):
      color = (255, 0, 0)
      if self.is_active(unique_id):
        rect = pygame.Rect(rect[0] + 3, rect[1] + 3, rect[2], rect[3])

    if self.keyboard_item == unique_id:
      self.draw_rect(rect, color)
      self.draw_rect(rect, (0, 255, 0), outline=1)
    else:
      self.draw_rect(rect, color)

    if text is not None:
      self.draw_text(rect, text, align='center')

    pressed_return = False
    if self.keyboard_item == unique_id:
      if self.key_down:
        if self.key_down.key == locals.K_TAB:
          self.keyboard_item = None
          self.key_char = None
          self.key_down = None
        elif self.key_down.key == locals.K_RETURN:
          pressed_return = True

    return self.pressed_widget(unique_id) or pressed_return

  def text_field(self, unique_id, x=0, y=0, rect=None):
    """
    Render text widget
    """
    if rect is None:
      rect = pygame.Rect(x, y, 180, 30)
    color = (100, 0, 0)

    if unique_id not in self.text:
      self.text[unique_id] = ''

    text_changes = False

    self.check_and_set_hotness(unique_id, rect)

    if self.keyboard_item is None:
      self.keyboard_item = unique_id

    if self.is_hot(unique_id):
      color = (255, 0, 0)

    if self.keyboard_item == unique_id:
      self.draw_rect(rect, color)
      self.draw_rect(rect, (0, 255, 0), outline=1)
      self.draw_text(rect, self.text[unique_id] + '_', align='left')
    else:
      self.draw_rect(rect, color)
      self.draw_text(rect, self.text[unique_id], align='left')

    if self.keyboard_item == unique_id:
      if self.key_down:
        if self.key_down.key == locals.K_TAB:
          self.keyboard_item = None
          self.key_char = None
          self.key_down = None
        elif self.key_down.key == locals.K_SPACE:
          self.text[unique_id] += ' '
        elif self.key_down.key == locals.K_BACKSPACE:
          if len(self.text[unique_id]):
            self.text[unique_id] = self.text[unique_id][:-1]
        elif self.key_down.key == locals.K_RETURN:
          pass
        elif self.key_char:
          text_width = self.text_size(self.text[unique_id] + self.key_char)[0]
          if text_width + 2 < rect[2]:
            self.text[unique_id] += self.key_char

        text_changes = True

    if self.pressed_widget(unique_id):
      self.keyboard_item = unique_id

    return text_changes

  def text_size(self, text):
    """
    Return text (width, height)
    """
    return self.font.size(text)

  def draw_rect(self, rect, color, outline=0):
    """
    Render a rectangle
    """
    pygame.draw.rect(self.surface, color, rect, outline)

  def draw_text(self, rect, text, align='left'):
    """
    Draw some text
    """
    text_surface = self.font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()

    offset_x = (rect[2] - text_rect[2])
    offset_y = (rect[3] - text_rect[3])

    if align == 'center':
      offset_x /= 2
      offset_y /= 2
    elif align == 'left':
      offset_x = 2
      offset_y /= 2

    new_rect = (
     rect[0] + offset_x,
     rect[1] + offset_y,
     rect[2],
     rect[3]
    )

    self.surface.blit(text_surface, new_rect)

  def process_event(self, event):
    """
    Process events polled
    """
    if event.type == locals.KEYDOWN:
      self.key_down = event
      if self.key_down.key < 127:
        self.key_char = self.key_down.unicode
