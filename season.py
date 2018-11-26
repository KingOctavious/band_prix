from circuit import Circuit

import collections

class Season:
  def __init__(self, year, circuits, teams):
    self.year = year
    self.circuits = circuits
    self.teams = teams
    
    self.current_race = 0
    self.races = [] # Doesn't populate until after race happens

    # Each team's points (dict of team:points)
    self.standings = {}
    for team in teams:
      self.standings[team] = 0

    # Finishing times for each team for each circuit
    self.results = {}
    for circuit in circuits:
      self.results[circuit] = {}
      for team in teams:
        self.results[circuit][team] = None


  # get_ordered_standings
  #
  # Returns ordered dict of team:points
  def get_ordered_standings(self):
    return collections.OrderedDict(sorted(self.standings.items(), key=lambda t: t[1], reverse=True))


  # get_overview
  #
  # Returns list of (race info, winner name) tuples
  def get_overview(self):
    overview = []
    for x in range(0, len(self.circuits)):
      c_name = self.circuits[x].name
      winner_name = ''
      if x < self.current_race:
        # sorted_results = sorted(self.results[self.circuits[x]], key=self.results[self.circuits[x]].__getitem__, reverse=True)
        # winner_name = sorted_results[0][0].name
        winner_name = self.races[x].places[1]

      overview.append((c_name + (' ' * 4), winner_name))

    return overview
    
  
  # get_winner
  #
  # Returns winning team object of the provided race
  def get_winner(self, race):
    return race.places[1]