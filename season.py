from circuit import Circuit

class Season:
  def __init__(self, year, circuits, teams):
    self.year = year
    self.circuits = circuits
    self.teams = teams
    
    self.next_race = 0

    # Each team's points
    self.standings = {}
    for team in teams:
      self.standings[team] = 0

    # Finishing times for each team for each circuit
    self.results = {}
    for circuit in circuits:
      self.results[circuit] = {}
      for team in teams:
        self.results[circuit][team] = None

  # get_overview
  #
  # Returns list of (race info, winner name) tuples
  def get_overview(self):
    overview = []
    for x in range(0, len(self.circuits)):
      c_name = self.circuits[x].name
      winner_name = ''
      if x < self.next_race:
        sorted_results = sorted(self.results[self.circuits[x]], key=self.results[self.circuits[x]].__getitem__, reverse=True)
        winner_name = sorted_results[0][0].name

      overview.append((c_name + (' ' * 4), winner_name))

    return overview
    
  
    