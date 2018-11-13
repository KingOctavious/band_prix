import global_data as g

class Race:

  def __init__(self, teams, circuit, lyrics):
    self.teams = teams
    self.circuit = circuit
    self.lyrics = lyrics

    self.lane_padding = 2

    # All vehicle bodies should be the same width, so we only have to look at
    # the first one.
    self.lane_size = teams[0].vehicle.body.width + (self.lane_padding * 2)

    # finished_teams
    #
    # Vector of place:team tuples.
    # Couldn't use dict with place keys because that wouldn't work if any teams
    # tie.
    self.finished_teams = []

    # finish_times
    #
    # Dict of teams and finishing times at end of race
    self.finish_times = {}

    # Set vhicles' starting positions
    for n in range(0, len(teams)):
      teams[n].vehicle.x = 1 + self.lane_padding + ((self.lane_size + 1) * n)
      teams[n].vehicle.y =  int(g.TRACK_ROWS_TO_DISPLAY / 2)#START_DIST_FROM_TOP
