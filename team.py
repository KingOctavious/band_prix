class Team:
  def __init__(self, name, color, vehicle, isPlayer=False):
    self.name = name
    self.color = color
    self.vehicle = vehicle
    self.isPlayer = isPlayer
    self.finished_current_race = False

    self.vehicle.body.color = color

  def set_color(self, color):
    self.color = color
    self.vehicle.body.color = color