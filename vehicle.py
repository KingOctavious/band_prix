import vehicle_bodies

class Vehicle:
  MAX_COMPONENT_CONDITION = 100

  def __init__(self, body):
    self.body = body

    # Positions based on coordinates of vehicle's top left tile
    self.x = 0
    self.y = 0

    self.distance_traveled = 0
    self.speed = 0

    self.components_condition = {
      'engine': self.MAX_COMPONENT_CONDITION,
      'front axle': self.MAX_COMPONENT_CONDITION,
      'frame': self.MAX_COMPONENT_CONDITION,
      'front left tire': self.MAX_COMPONENT_CONDITION,
      'front right tire': self.MAX_COMPONENT_CONDITION,
      'rear left tire': self.MAX_COMPONENT_CONDITION,
      'rear right tire': self.MAX_COMPONENT_CONDITION
    }

  def printBody(self):
    self.body.printBody()