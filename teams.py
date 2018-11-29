import libtcodpy as tcod

import random
from team import Team
from vehicle import Vehicle
import vehicle_bodies

ALL_TEAMS = [
  Team('Kasvot Vaxt', tcod.light_cyan, Vehicle(vehicle_bodies.v_bod_1)),
  Team('ViscDuds', tcod.purple, Vehicle(vehicle_bodies.v_bod_1)),
  Team('The Billiards', tcod.sea, Vehicle(vehicle_bodies.v_bod_1)),
  Team('Strange Dan Gustafvist', tcod.yellow, Vehicle(vehicle_bodies.v_bod_1)),
  Team('Italian Horse', tcod.red, Vehicle(vehicle_bodies.v_bod_1)),
  Team('The Unicorns', tcod.light_purple, Vehicle(vehicle_bodies.v_bod_1)),
  Team('Harold of the Boulders', tcod.gray, Vehicle(vehicle_bodies.v_bod_1)),
  Team('PrimeThem', tcod.sepia, Vehicle(vehicle_bodies.v_bod_1)),
  Team('Dreaded Blimp', tcod.turquoise, Vehicle(vehicle_bodies.v_bod_1)),
  Team('Has', tcod.white, Vehicle(vehicle_bodies.v_bod_1)),
]

def pick_season_teams(player_team):
  indexes = []
  while len(indexes) < 4:
    index = random.randint(0, len(ALL_TEAMS) - 1)
    if index not in indexes:
      indexes.append(index)

  teams = [
    ALL_TEAMS[indexes[0]],
    ALL_TEAMS[indexes[1]],
    player_team,
    ALL_TEAMS[indexes[2]],
    ALL_TEAMS[indexes[3]]
  ]

  return teams