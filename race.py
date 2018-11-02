class Race:
  barricade = '='
  lane_stripe = '|'

  def __init__(self, teams):
    self.teams = teams
    self.lane_padding = 1

    # All vehicle bodies should be the same width, so we only have to look at
    # the first one.
    self.lane_size = teams[0].vehicle.body.width + (self.lane_padding * 2)


