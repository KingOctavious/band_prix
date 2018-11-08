from vehicle_body import Vehicle_Body
import vehicle_bodies

class Vehicle:
  MAX_COMPONENT_CONDITION = 100

  def __init__(self, body, color):
    self.body = Vehicle_Body(body.rows) # Do it like this to force copy
    self.color = color

    # Positions based on coordinates of vehicle's top left tile
    self.x = 0
    self.y = 0

    self.distance_traveled = 0
    self.speed = 0 # tiles per second
    self.max_speed = 20

    self.components_condition = {
      'engine': self.MAX_COMPONENT_CONDITION,
      'front axle': self.MAX_COMPONENT_CONDITION,
      'frame': self.MAX_COMPONENT_CONDITION,
      'front left tire': self.MAX_COMPONENT_CONDITION,
      'front right tire': self.MAX_COMPONENT_CONDITION,
      'rear left tire': self.MAX_COMPONENT_CONDITION,
      'rear right tire': self.MAX_COMPONENT_CONDITION
    }

  def advance(self, distance=1):
    self.distance_traveled += distance