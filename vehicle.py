import libtcodpy as tcod
from vehicle_body import Vehicle_Body
import vehicle_bodies

class Vehicle:
  MAX_COMPONENT_CONDITION = 100

  def __init__(self, body, color=tcod.white):
    self.body = Vehicle_Body(body.rows) # Do it like this to force copy
    self.color = color
    
    # Store this so we can fix the body between races
    self.original_body = Vehicle_Body(body.rows)
    
    # Positions based on coordinates of vehicle's top left tile
    self.x = 0
    self.y = 0

    self.condition = 100
    self.hp_per_component = self.condition / (self.body.length * self.body.width)
    self.is_player = False
    self.distance_traveled = 0
    self.speed = 0 # tiles per second
    self.max_speed = 30
    self.current_max_speed_from_power = 0
    self.acceleration = 0
    self.max_acceleration = 6 # speed units per second


  def apply_damage(self, damage):
    self.condition -= damage
    # Need to keep damage > 0 so that vehicle can finish the race
    if self.condition < 1:
      self.condition = 1


  def apply_power(self, power_percentage):
    modifier_from_damage = self.condition / 100

    if power_percentage > 0:
      self.current_max_speed_from_power = round(power_percentage * self.max_speed * modifier_from_damage)
      self.acceleration = round(power_percentage * self.max_acceleration * modifier_from_damage)

    else:
      self.current_max_speed_from_power -= 0.1
      if self.current_max_speed_from_power < 0:
        self.current_max_speed_from_power = 0
      self.acceleration -= 0.1
      if self.acceleration < 0:
        self.acceleration = 0


  def advance(self, distance=1):
    self.distance_traveled += distance

  
  def reset(self):
    self.body = Vehicle_Body(self.original_body.rows)
    self.distance_traveled = 0
    self.speed = 0
    self.current_max_speed_from_power = 0
    self.acceleration = 0
    self.condition = 100
    self.distance_traveled = 0