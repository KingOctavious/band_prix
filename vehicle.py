import libtcodpy as tcod
from vehicle_body import Vehicle_Body
import vehicle_bodies

class Vehicle:
  MAX_COMPONENT_CONDITION = 100

  def __init__(self, body, color=tcod.white):
    self.body = Vehicle_Body(body.rows) # Do it like this to force copy
    self.color = color

    # Positions based on coordinates of vehicle's top left tile
    self.x = 0
    self.y = 0

    self.is_player = False
    self.distance_traveled = 0
    self.speed = 0 # tiles per second
    self.max_speed = 30
    self.current_max_speed_from_power = 0
    self.acceleration = 0
    self.max_acceleration = 6 # speed units per second

    self.components_condition = {
      'engine': self.MAX_COMPONENT_CONDITION,
      'front axle': self.MAX_COMPONENT_CONDITION,
      'frame': self.MAX_COMPONENT_CONDITION,
      'front left tire': self.MAX_COMPONENT_CONDITION,
      'front right tire': self.MAX_COMPONENT_CONDITION,
      'rear left tire': self.MAX_COMPONENT_CONDITION,
      'rear right tire': self.MAX_COMPONENT_CONDITION
    }

  def apply_power(self, power_percentage):
    if power_percentage > 0:
      self.current_max_speed_from_power = round(power_percentage * self.max_speed)
      self.acceleration = round(power_percentage * self.max_acceleration)

    else:
      self.current_max_speed_from_power -= 0.1
      if self.current_max_speed_from_power < 0:
        self.current_max_speed_from_power = 0
      self.acceleration -= 0.1
      if self.acceleration < 0:
        self.acceleration = 0




  def advance(self, distance=1):
    self.distance_traveled += distance