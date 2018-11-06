import libtcodpy as tcod

import circuits
from input_handlers import handle_keys
from race import Race
from team import Team
from time import sleep
from track_direction import Track_Direction as td
from vehicle import Vehicle
from vehicle_body import Vehicle_Body
import vehicle_bodies


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
fullscreen = False
GAME_TITLE = 'Band Prix'
font_path = 'terminal10x10_gs_tc.png'
font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
TURN_BASED = False

STRIPE_CHARS = {
  td.STRAIGHT: '|',
  td.LEFT: '\\',
  td.RIGHT: '/'
}





def print_track(con, track_shape_set, distance_traveled):
  lane_count = len(race.teams)
  lane_size = race.lane_size
  NUM_ROWS_TO_DISPLAY = 30
  track_width = ((lane_size + 1) * lane_count) + 1

  for track_row in range(distance_traveled, distance_traveled + NUM_ROWS_TO_DISPLAY):
    offset = track_shape_set[track_row][1]
    left_edge = 0 + offset
    if offset != 0:
      print("offset")
      print(offset)
      print("left edge")
      print(left_edge)
    for col in range(left_edge, track_width + left_edge + 1):

      # Print barricades
      if col == left_edge or col == left_edge + track_width - 1:
        tcod.console_put_char(con, col, distance + NUM_ROWS_TO_DISPLAY - track_row, race.barricade, tcod.BKGND_NONE)
      
      # Print lane stripes
      else:
        lane = int(col / (lane_size + 1))
        col_within_lane = col - (lane * (lane_size + 1))

        if col_within_lane == 0:
          tcod.console_put_char(con, col + offset, distance + NUM_ROWS_TO_DISPLAY - track_row, str(track_shape_set[track_row][0]), tcod.BKGND_NONE)








def print_vehicles(con, race):
  # Print all vehicles
  for n in range(0, len(race.teams)):
    for row in range(0, len(race.teams[n].vehicle.body.rows)):
      for col in range(0, len(race.teams[n].vehicle.body.rows[row])):
        x = race.teams[n].vehicle.x + col
        y = race.teams[n].vehicle.y + row
        tcod.console_put_char(con, x, y, race.teams[n].vehicle.body.rows[row][col], tcod.BKGND_NONE)


def print_race(con, race, distance):
  print_track(con, race.circuit.track_shape, distance)
  print_vehicles(con, race)









tcod.console_set_custom_font(font_path, font_flags)
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, fullscreen)
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
tcod.sys_set_fps(LIMIT_FPS)




teams = [
  Team('Kasvot Vaxt', Vehicle(vehicle_bodies.v_bod_1)),
  Team('ViscDuds', Vehicle(vehicle_bodies.v_bod_1)),
  Team('The Jack Straw Band', Vehicle(vehicle_bodies.v_bod_1), True),
  Team('The Billiards', Vehicle(vehicle_bodies.v_bod_1)),
  Team('Strange Dan Gustafvist', Vehicle(vehicle_bodies.v_bod_1)),
]

race = Race(teams, circuits.circuit1)

# Figure out which team index is the player's team and reset their distance_traveled
player_team_index = 0
for x in range(0, len(race.teams)):
  race.teams[x].vehicle.distance_traveled = 0
  race.teams[x].vehicle.speed = 0
  if (race.teams[x].isPlayer):
    player_team_index = x




distance = 0
ticks = 0
key = tcod.Key()
mouse = tcod.Mouse()
exit_game = False
tcod.console_set_default_foreground(con, tcod.pink)
### GAME LOOP #################################################################
while not tcod.console_is_window_closed() and not exit_game:
  tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)         

  action = handle_keys(key)
  steer = action.get('steer')
  exit = action.get('exit')

  if steer:
    teams[player_team_index].vehicle.x += steer
  
  if exit:
    exit_game = True


  tcod.console_clear(con)
  print_race(con, race, distance)
  tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,)
  tcod.console_flush()



  #sleep(0.1)
  distance += 1
  ticks += 1

quit()