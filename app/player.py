import os
import sys
import pygame

from pygame import locals

from app.animation import SurfaceAnimation
from app.animation import RectFrame
from app.animation import AnimatedSprite
from app.physics import PhysicsObject
from app.physics import PhysicsManager
from app.physics import TERMINAL_VELOCITY

#this needs to be abstracted out
from app.renderer import *


class Player(AnimatedSprite):

  image_file = "megaman.png"
  physics_object = PhysicsObject()
    
  def __init__(self):
    super(Player, self).__init__()

    run = SurfaceAnimation(
      'run',
      [RectFrame(188, 12, 24, 22),
       RectFrame(218, 10, 16, 24),
       RectFrame(238, 12, 24, 22)],
      total_time=100
    )

    jump = SurfaceAnimation(
      'jump',
      [RectFrame(265, 4, 26, 30)]
    )

    idle = SurfaceAnimation(
      'idle',
      [RectFrame(103, 10, 21, 24, total_time=10000),
       RectFrame(133, 10, 21, 24, total_time=250),
       RectFrame(103, 10, 21, 24, total_time=250),
       RectFrame(160, 10, 20, 24, total_time=400)],
    )

    self.animation_manager.set_animations([run, jump, idle])

    self.update_frame(0)
    self.rect.x = TILE_SIZE
    self.rect.y = TILE_SIZE * 14 - self.rect.height

  def update_physics_object(self, delta):
    self.physics_object.rect = self.rect
    self.physics_object.update(delta)

  def update_animation(self):
    if self.physics_object.velocity_y < 0:
      self.animation_manager.set_animation('jump')
    elif self.physics_object.velocity_y == 0:
      if self.physics_object.velocity_x > 0:
        self.animation_manager.set_animation('run')
      elif self.physics_object.velocity_x < 0:
        self.animation_manager.set_animation('run')

    if self.physics_object.velocity_x > 0:
      self.animation_manager.get_animation().set_flip(False)
    elif self.physics_object.velocity_x < 0:
      self.animation_manager.get_animation().set_flip(True)
    elif self.physics_object.velocity_y == 0:
      last_animation = self.animation_manager.get_animation()
      self.animation_manager.set_animation('idle')

      if last_animation.name != 'idle':
        last_orientation = last_animation.flip
        self.animation_manager.get_animation().set_flip(last_orientation)

  def update(self, delta):
    keys = pygame.key.get_pressed()
    if keys[locals.K_RIGHT]:
      self.physics_object.velocity_x = 125.0
    elif keys[locals.K_LEFT]:
      self.physics_object.velocity_x = -100.0
    else:
      self.physics_object.velocity_x = 0
    if keys[locals.K_z]:
      if self.physics_object.velocity_y is 0:
        self.physics_object.velocity_y = -TERMINAL_VELOCITY / 3

    self.update_animation()
    self.update_frame(delta)
    self.update_physics_object(delta)

  def get_surface(self, delta):
    return