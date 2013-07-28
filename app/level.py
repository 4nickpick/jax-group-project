import os
import pygame
from pygame import locals

from app.physics import PhysicsManager
from app.camera import ScrollCamera as Camera
from app.renderer import *

from contrib.pytmx import tmxloader


"""
class PygameGUIContext(UIContext):

  def event_poll(self, event):
    Go through events
    pass

  def key_pressed(self, key):
    Return whether the user pressed the key
    keys = pygame.key.get_pressed()
    if key == 'TAB':
      return keys[locals.K_TAB]
    elif key == 'RETURN':
      return keys[locals.K_RETURN]
"""


class PygameUIRenderer(object):

  hot_item = None
  active_item = None
  keyboard_item = None
  key_down = None
  font = None
  text = {}

  def __init__(self, surface):
    self.surface = surface
    pygame.font.init()
    self.font = pygame.font.Font(pygame.font.get_default_font(), 11)

  def button(self, unique_id, x, y, text=None):
    rect = pygame.Rect(x, y, 80, 30)
    color = (100, 0, 0)

    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()[0]
    user_activates_button = False

    # Check for hotness
    if pygame.mouse.get_focused():
      if rect.collidepoint(mouse_pos):
        self.hot_item = unique_id
        if self.active_item is None and mouse_press:
          self.active_item = unique_id

    if self.hot_item == unique_id:
      color = (255, 0, 0)
      if self.active_item == unique_id:
        rect = pygame.Rect(rect[0] + 3, rect[1] + 3, 80, 30)

    self.draw_rect(rect, color)
    if text is not None:
      self.draw_text(rect, text)

    if self.hot_item == unique_id and self.active_item == unique_id:
      if not pygame.mouse.get_pressed()[0]:
        user_activates_button = True

    return user_activates_button

  def text_field(self, unique_id, x, y):
    """
    Display text field
    """
    rect = pygame.Rect(x, y, 180, 30)
    color = (100, 0, 0)

    if unique_id not in self.text:
      self.text[unique_id] = ''

    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()[0]
    text_changes = False

    # Check for hotness
    if pygame.mouse.get_focused():
      if rect.collidepoint(mouse_pos):
        self.hot_item = unique_id
        if self.active_item is None and mouse_press:
          self.active_item = unique_id

    if self.keyboard_item is None:
      self.keyboard_item = unique_id

    if self.active_item == unique_id or self.hot_item == unique_id:
      color = (255, 0, 0)

    self.draw_rect(rect, color)

    if self.keyboard_item == unique_id:
      self.draw_text(rect, self.text[unique_id] + '_')
    else:
      self.draw_text(rect, self.text[unique_id])

    if self.keyboard_item == unique_id:
      if self.key_down:
        self.text[unique_id] += pygame.key.name(self.key_down)
        text_changes = True

    return text_changes

  def draw_rect(self, rect, color):
    """
    Render a rectangle
    """
    render_rect(self.surface, color, rect)

  def draw_text(self, rect, text):
    """
    Draw some text
    """
    text_surface = self.font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    new_rect = (
     rect[0] + (rect[2] - text_rect[2]) / 2,
     rect[1] + (rect[3] - text_rect[3]) / 2,
     rect[2],
     rect[3]
    )

    self.surface.blit(text_surface, new_rect)

  def draw_line(self):
    """
    """
    pass

  def draw_char(self):
    """
    """
    pass

  def draw_string(self):
    """
    """
    pass

  def process_event(self, event):
    if event.type == locals.KEYDOWN:
      self.key_down = event.key


class Context(PygameUIRenderer):

  def __init__(self, surface):
    super(Context, self).__init__(surface)

  def prepare(self):
    self.hot_item = None

  def finish(self):
    mouse_press = pygame.mouse.get_pressed()[0]
    if not mouse_press:
      self.active_item = None
    elif self.active_item is None:
      self.active_item = -1
    self.key_down = None


class Level(object):

  camera = Camera(SCREEN_W, SCREEN_H)

  def __init__(self, player):
    self.map_file = "test_megaman_map.tmx"

    self.map_data = tmxloader.load_pygame(
      os.path.join("data", "maps", self.map_file)
    )
    self.physics_manager = PhysicsManager(self.map_data)

    self.player = player
    self.all_sprites = pygame.sprite.RenderPlain((self.player,))

  def draw(self, surface):
    tile_width = self.map_data.tilewidth
    tile_height = self.map_data.tileheight

    for layer in xrange(0, len(self.map_data.tilelayers)):
      for y in xrange(0, self.map_data.height):
        for x in xrange(0, self.map_data.width):
          image = self.map_data.getTileImage(x, y, layer)
          if image:
            render_image(
              surface, image, x * tile_width, y * tile_height, self.camera)

    for object_group in self.map_data.objectgroups:
      for obj in object_group:
        if hasattr(obj, 'points'):
          points = [(i[0] + obj.x, i[1] + obj.y) for i in obj.points]
          render_line(
            surface, (255, 128, 128), obj.closed, points, self.camera, 2)
        else:
          render_rect(
            surface,
            (255, 128, 128),
            (obj.x + self.camera.offset_x,
             obj.y + self.camera.offset_y,
             obj.width,
             obj.height)
          )

          #    ui_context = PygameGUIContext(PygameUIRenderer(surface))

    render_image(
      surface,
      self.player.image,
      self.player.rect.x,
      self.player.rect.y,
      self.camera
    )

  def update(self, delta):
    self.all_sprites.update(delta)
    self.camera.update(self.player.rect, delta)
    self.physics_manager.handle_tile_collision(
      self.player.physics_object, delta)

  def do_ui(self):
    #if button(self.ui_context, 0, 0, 50, 20):
      #print 'hi'
    pass

  def add_sprite(self, new_sprite):
    self.all_sprites.add(new_sprite)
