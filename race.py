import global_data as g

class Race:

  def __init__(self, teams, circuit, lyrics, song_title):
    self.teams = teams
    self.circuit = circuit
    self.lyrics = lyrics
    self.song_title = song_title

    self.lane_padding = 1

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

    # places
    #
    # Dict of place:team finalized at end of race.
    self.places = {}

    # Set vehicles' starting positions
    for n in range(0, len(teams)):
      teams[n].vehicle.x = 1 + self.lane_padding + ((self.lane_size + 1) * n)
      teams[n].vehicle.y =  int(g.TRACK_ROWS_TO_DISPLAY / 2)
