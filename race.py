class Race:
  barricade = '='
  lane_stripe = '|'

  def __init__(self, teams):
    self.teams = teams
    self.lane_padding = 1

    # All vehicle bodies should be the same width, so we only have to look at
    # the first one.
    self.lane_size = teams[0].vehicle.body.width + (self.lane_padding * 2)

    # Set vhicles' starting positions
    START_DIST_FROM_TOP = 15
    for n in range(0, len(teams)):
      teams[n].vehicle.x = 1 + self.lane_padding + ((self.lane_size + 1) * n)
      teams[n].vehicle.y =  START_DIST_FROM_TOP
