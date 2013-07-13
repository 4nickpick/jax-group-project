#convert to abstract class

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

class Entity(AnimatedSprite):

  image_file = "megaman.png"
  physics_object = PhysicsObject()
    
  def __init__(self):
    super(Entity, self).__init__()

    #self.animation_manager.set_animations()

    #self.update_frame(0)
    #self.rect.x = TILE_SIZE
    #self.rect.y = TILE_SIZE * 14 - self.rect.height

  def update_physics_object(self, delta):
    raise NotImplementedError("Subclass has not implemented this.")

  def update_animation(self):
    raise NotImplementedError("Subclass has not implemented this.")

  def update(self, delta):
    raise NotImplementedError("Subclass has not implemented this.")

    #self.update_animation()
    #self.update_frame(delta)
    #self.update_physics_object(delta)

  def get_surface(self, delta):
    return