"""
Animation base classes

@author Stephen Pridham
"""


class Frame(object):
  """
  Container class for a single frame.
  The list of callbacks are called with the delta argument
  to hook functionality to individual frames if needed.
  You can also have varied time per frame, say if a certain frame
  is longer than others for some reason or another.

  Usage:
  >> def play_footstep(delta):
  >>   sound_manager.play("metal_footstep.wav")
  >> Frame(..., callbacks=[play_footstep])
  """
  def __init__(self, total_time=0.5, callbacks=None):
    self.total_time = total_time
    self.callbacks = callbacks


class Animation(object):
  """
  Container class for a single animation.
  This class calls the callbacks for the frames.
  """
  delta = 0

  def __init__(self, name, frames, current_frame=0):
    self.name = name
    self.frames = frames
    self.current_frame = current_frame

  def get_next_frame(self, delta):
    if not self.frames:
      return None

    self.delta += delta

    if self.delta > self.frames[self.current_frame].total_time:
      self.delta = 0
      self.current_frame += 1
      if self.current_frame > (len(self.frames) - 1):
        self.restart()
      for callback in self.frames[self.current_frame].callbacks:
        callback(delta)

    return self.frames[self.current_frame]

  def get_frame_at(self, index):
    try:
      return self.frame[index]
    except IndexError:
      raise IndexError("Animation frame chosen out of index")

  def set_frame_at(self, index):
    self.current_frame = index

  def restart(self):
    self.current_frame = 0
    self.delta = 0


class AnimationManager(object):
  """
  Manager class for a number of animations.

  Usage:
  >> manager = AnimationManager()
  >> manager.set_animations([
  >>   Animation(
  >>    'walk_right',
  >>    [Frame(...), Frame(...), Frame(...)]
  >>  )
  >>   Animation(
  >>    'walk_left',
  >>    [Frame(...), Frame(...), Frame(...)]
  >>   )
  >> ])

  To set next frame in animation:
  >> image = spritesheet.subsurface(
  >>  manager.get_next_frame(delta_milliseconds)
  >> )
  """
  current_animation = None
  animations = {}

  def __init__(self, animations=[]):
    self.set_animations(animations)

    for a in self.animations.iteritems():
      if not isinstance(a[1], Animation):
        raise ValueError("%r only accepts animations" % self.__repr__())

    if self.animations:
      self.current_animation = list(self.animations[0])

  def __unicode__(self):
    if self.current_animation:
      return unicode(self.current_animation)
    else:
      return super(AnimationManager, self).__unicode__()

  def get_next_frame(self, delta, animation=None):
    """
    Get the next frame in the current or specified animation
    """
    current_animation = self.get_animation(animation)
    if current_animation:
      return current_animation.get_next_frame(delta)

  def get_animation(self, animation=None):
    """
    Get the current or specified animation
    """
    if animation in self.animations:
      current_animation = self.animations[animation]
    elif self.current_animation in self.animations:
      current_animation = self.animations[self.current_animation]
    else:
      raise KeyError("Invalid animation %s for %r" % (
          animation, self.__repr__())
      )

    return current_animation

  def get_frame_at(self, index):
    return self.get_animation().get_frame_at(index)

  def set_frame_at(self, index):
    self.get_animation().set_frame_at(index)

  def set_animation(self, animation_name):
    """
    Set current animation state
    """
    if animation_name not in self.animations:
      raise KeyError(
        "The animation %s is not available for %r" %
        (animation_name, self.__repr__())
      )
    self.current_animation = animation_name
    self.reset()

  def set_animations(self, animations):
    """
    Push a list of animations
    """
    for animation in animations:
      self.push(animation)

  def push(self, animation):
    self.animations[animation.name] = animation
    if self.current_animation is None:
      self.current_animation = animation.name

  def pop(self, animation):
    if animation is self.current_animation:
      raise ValueError(
        "You're popping the current animation for %r" % self.__repr__()
      )
    animation = self.animations[animation]
    del self.animations[animation]
    return animation

  def reset(self, animation_name=None):
    self.get_animation(animation_name).reset()
