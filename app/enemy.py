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


class Enemy(AnimatedSprite):

  image_file = "enemies.png"
  physics_object = PhysicsObject()
    
  def __init__(self):
    super(Enemy, self).__init__()

    run = SurfaceAnimation(
      'run',
      [RectFrame(0, 0, 20, 20),
       RectFrame(28, 0, 20, 20)],
      total_time=100
    )

    jump = SurfaceAnimation(
      'jump',
      [RectFrame(0, 0, 20, 20)]
    )

    idle = SurfaceAnimation(
      'idle',
      [RectFrame(0, 0, 20, 20)],
    )

    self.animation_manager.set_animations([run, jump, idle])

    self.update_frame(0)
    self.rect.x = TILE_SIZE * 14
    self.rect.y = TILE_SIZE * 10 - self.rect.height
    
    self.physics_object.velocity_x = -25

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

    self.update_animation()
    self.update_frame(delta)
    self.update_physics_object(delta)

  def get_surface(self, delta):
    return