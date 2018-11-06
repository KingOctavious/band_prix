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




def handle_collisions(race):
  # Compare every vehicle position to every other vehicle position
  team_count = (len(race.teams))
  for index in range(0, team_count):
    base_vehicle = race.teams[index].vehicle
    base_x = base_vehicle.x
    base_y = base_vehicle.y
    base_w = base_vehicle.body.width
    base_h = base_vehicle.body.length

    if index < team_count - 1:
      # We only have to check the opponents indexed higher than the currently
      # checked index, because as we move up in the base index being checked,
      # it has already been checked against those below it. So, we start
      # checking at `index + 1`.
      for opponent_index in range(index + 1, team_count):
        opp_vehicle = race.teams[opponent_index].vehicle
        opp_x = opp_vehicle.x
        opp_y = opp_vehicle.y
        opp_w = opp_vehicle.body.width
        opp_h = opp_vehicle.body.length

        if base_vehicle.x < opp_vehicle.x + opp_vehicle.body.width and base_vehicle.x + base_vehicle.body.width > opp_vehicle.x and base_vehicle.y < opp_vehicle.y + opp_vehicle.body.length and base_vehicle.y + base_vehicle.body.length > opp_vehicle.y:
          # COLLISION DETECTED!
          # Now we need to figure out which specific parts of the vehicles collided.
         
          # This will be a list of lists of tuples
          base_veh_grid = []
          for row in range(0, base_h):
            current_col_pts = []
            for col in range(0, base_w):
              current_col_pts.append((col + base_x, row + base_y))

            base_veh_grid.append(current_col_pts)


          # Now do mostly the same for opp
          opp_veh_collision_pts = []
          base_veh_collision_pts = []
          for row in range(0, opp_h):
            #current_col_pts = []
            for col in range(0, opp_w):        
              opp_coords = (col + opp_x, row + opp_y)

              for base_row in range(0, len(base_veh_grid)):
                for base_col in range(0, len(base_veh_grid[base_row])):
                  if base_veh_grid[base_row][base_col] == opp_coords:
                    # This is where a collision occurred
                    opp_veh_collision_pts.append((col, row))
                    base_veh_collision_pts.append((base_col, base_row))
                    print('COLLISION!')


              #current_col_pts.append((col + opp_x, row + opp_y))

            #opp_veh_grid.append(current_col_pts)
          for veh_part in base_veh_collision_pts:
            new_body_row = ''
            for index in range(0, base_vehicle.body.width):
              if index != veh_part[1]:
                new_body_row += base_vehicle.body.rows[veh_part[0]][index]
              else:
                new_body_row += '*'

            #base_vehicle.body.rows[veh_part[0]][veh_part[1]] = '*'

            base_vehicle.body.rows[veh_part[0]] = new_body_row
            #print(base_vehicle.body.rows[veh_part[0]][veh_part[1]])

          # !!! NEED TO ADD COLLISION CHECK FOR BARRIERS AS WELL




def print_track(con, track_shape_set, distance_traveled):
  lane_count = len(race.teams)
  lane_size = race.lane_size
  NUM_ROWS_TO_DISPLAY = 30
  track_width = ((lane_size + 1) * lane_count) + 1

  for track_row in range(distance_traveled, distance_traveled + NUM_ROWS_TO_DISPLAY):
    offset = track_shape_set[track_row][1]
    left_edge = 0 + offset

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

  # Check for collisions
  handle_collisions(race)

  tcod.console_clear(con)
  print_race(con, race, distance)
  tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,)
  tcod.console_flush()



  #sleep(0.1)
  distance += 1
  ticks += 1

quit()