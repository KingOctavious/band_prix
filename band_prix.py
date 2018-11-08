import libtcodpy as tcod

import circuits
import global_data as g
from input_handlers import handle_keys
from race import Race
from team import Team
from time import sleep
from track_direction import Track_Direction as td
from vehicle import Vehicle
from vehicle_body import Vehicle_Body
import vehicle_bodies
import visuals


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
FPS_CAP = 30
#frame_render_time = 1 / FPS_CAP
#print("RENDER TIME:")
#print(frame_render_time)
fullscreen = False
GAME_TITLE = 'Band Prix'
#font_path = 'arial10x10.png'
#font_path = 'arial12x12.png'
#font_path = 'consolas10x10_gs_tc.png'
#font_path  = 'lucida12x12_gs_tc.png'
#font_path  = 'terminal10x10_gs_tc.png'

#layout = tcod.FONT_LAYOUT_TCOD

font_path  = 'terminal16x16_gs_ro.png'
layout = tcod.FONT_LAYOUT_ASCII_INROW

font_flags = tcod.FONT_TYPE_GREYSCALE | layout
TURN_BASED = False



def apply_collision(vehicle_body, collision_points):
  for veh_part in collision_points:
    veh_part_row = veh_part[1]
    current_body_row = vehicle_body.rows[veh_part_row]
    new_body_row = ''
    for index in range(0, len(current_body_row)):
      if index != veh_part[0]:
        new_body_row += current_body_row[index]
      else:
        new_body_row += visuals.COLLISION_EFFECT

    vehicle_body.rows[veh_part_row] = new_body_row


def handle_post_collision(vehicle):
  # Figure out which side of the car got hit
  collided_sides = {
    'front': 0,
    'left': 0,
    'right': 0,
    'rear': 0
  }

  # Count the colliding vehicle parts on each side to see where the collision
  # is coming from primarily. At the same time, we also rebuild the row strings
  # by replacing the collision effect with the damage effect.
  for row in range(0, len(vehicle.body.rows)):
    new_row_string = ''
    for col in range(0, len(vehicle.body.rows[row])):
      if vehicle.body.rows[row][col] == visuals.COLLISION_EFFECT:
        if col == 0:
          collided_sides['left'] += 1
        elif col == vehicle.body.width - 1:
          collided_sides['right'] += 1
        if row == 0:
          collided_sides['front'] += 1
        elif row == len(vehicle.body.rows) - 1:
          collided_sides['rear'] += 1

        new_row_string += visuals.DAMAGE_EFFECT
      
      else:
        new_row_string += vehicle.body.rows[row][col]

    vehicle.body.rows[row] = new_row_string

  # Now figure out which direction the car should bounce back
  # (based on which side(s) have the most)
  bounce_directions = [] # Because might go back/left, forward/right, etc.
  max_collided_count = 0
  for side, count in collided_sides.items():
    if count > 0:
      if len(bounce_directions) == 0:
        bounce_directions.append(g.SIDE_OPPOSITES[side])
        max_collided_count = count
      elif count == max_collided_count:
        bounce_directions.append(g.SIDE_OPPOSITES[side])
      elif count > max_collided_count:
        # Clear `bounce_directions` and add this one if it is dominant.
        bounce_directions = [g.SIDE_OPPOSITES[side]]
        max_collided_count = count

  # Bounceback happens here
  if 'front' in bounce_directions:
    vehicle.y -= 1
  if 'rear' in bounce_directions:
    vehicle.y += 1
  if 'left' in bounce_directions:
    vehicle.x -= 1
  if 'right' in bounce_directions:
    vehicle.x += 1
      

def handle_collisions(race, colliding_vehicles_holder, barricade_locations_holder):
  # Compare every vehicle position to every other vehicle position
  team_count = (len(race.teams))
  for index in range(0, team_count):
    base_vehicle = race.teams[index].vehicle
    base_x = base_vehicle.x
    base_y = base_vehicle.y
    base_w = base_vehicle.body.width
    base_h = base_vehicle.body.length
    base_veh_collision_pts = [] # Holds x, y tuples

    if index < team_count - 1:
      # Check for collisions with barricades
      for y in range(base_y, base_y + base_h - 1):
        for x in range(base_x, base_x + base_w - 1):
          if (x, y) in barricade_locations_holder:
            base_veh_collision_pts.append((x - base_x, y - base_y))
            colliding_vehicles_holder.add(base_vehicle)
            apply_collision(base_vehicle.body, base_veh_collision_pts)
      # Done checking barricade collisions

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

        # Quicker initial check to see if collision occurred
        if base_x < opp_x + opp_w and base_x + base_w > opp_x and base_y < opp_y + opp_h and base_y + base_h > opp_y:
          # COLLISION DETECTED! Now we need to figure out which specific parts of the vehicles collided.
          colliding_vehicles_holder.add(base_vehicle)
          colliding_vehicles_holder.add(opp_vehicle)
         
          # This will be a list of lists of tuples (real coordinates of collision locations)
          base_veh_grid = []
          for row in range(0, base_h):
            current_col_pts = []
            for col in range(0, base_w):
              current_col_pts.append((col + base_x, row + base_y))

            base_veh_grid.append(current_col_pts)


          # Now do mostly the same for opp, but instead of adding them to an
          # `opp_veh_grid` list, we check them on the fly. If any of the opp
          # vehicle's body part coordinate tuples match one of those in
          # `base_veh_grid`, then that's where a collision occured. In those
          # cases, we add the relative body coordinates to each vehicle's list
          # of collision locations
          opp_veh_collision_pts = []
          for row in range(0, opp_h):
            for col in range(0, opp_w):        
              opp_coords = (col + opp_x, row + opp_y)

              for base_row in range(0, len(base_veh_grid)):
                for base_col in range(0, len(base_veh_grid[base_row])):
                  if base_veh_grid[base_row][base_col] == opp_coords:
                    # This is where a collision occurred
                    opp_veh_collision_pts.append((col, row))
                    base_veh_collision_pts.append((base_col, base_row))

          # Once the actual collision locations are determined, we apply
          # the collision events to those parts of the vehicles.
          apply_collision(base_vehicle.body, base_veh_collision_pts)
          apply_collision(opp_vehicle.body, opp_veh_collision_pts)


def print_track(con, track_shape_set, distance_traveled, barricade_locations_holder):
  barricade_locations_holder.clear()
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
        barricade_locations_holder.append((col, distance_traveled + NUM_ROWS_TO_DISPLAY - track_row))
        tcod.console_put_char(con, col, distance_traveled + NUM_ROWS_TO_DISPLAY - track_row, visuals.BARRICADE, tcod.BKGND_NONE)
      
      # Print lane stripes
      else:
        lane = int(col / (lane_size + 1))
        col_within_lane = col - (lane * (lane_size + 1))

        if col_within_lane == 0:
          tcod.console_put_char(con, col + offset, distance_traveled + NUM_ROWS_TO_DISPLAY - track_row, str(track_shape_set[track_row][0]), tcod.BKGND_NONE)


def print_vehicles(con, race):
  # Print all vehicles
  for n in range(0, len(race.teams)):
    for row in range(0, len(race.teams[n].vehicle.body.rows)):
      for col in range(0, len(race.teams[n].vehicle.body.rows[row])):
        x = race.teams[n].vehicle.x + col
        y = race.teams[n].vehicle.y + row
        tcod.console_put_char(con, x, y, race.teams[n].vehicle.body.rows[row][col], tcod.BKGND_NONE)
        tcod.console_set_char_foreground(con, x, y, race.teams[n].vehicle.color)


def print_race(con, race, distance, barricade_locations_holder):
  print_track(con, race.circuit.track_shape, distance, barricade_locations_holder)
  print_vehicles(con, race)









tcod.console_set_custom_font(font_path, font_flags)
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, fullscreen)
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
tcod.sys_set_fps(FPS_CAP)




teams = [
  Team('Kasvot Vaxt', Vehicle(vehicle_bodies.v_bod_1, tcod.yellow)),
  Team('ViscDuds', Vehicle(vehicle_bodies.v_bod_1, tcod.green)),
  Team('The Jack Straw Band', Vehicle(vehicle_bodies.v_bod_1, tcod.pink), True),
  Team('The Billiards', Vehicle(vehicle_bodies.v_bod_1, tcod.orange)),
  Team('Strange Dan Gustafvist', Vehicle(vehicle_bodies.v_bod_1, tcod.light_cyan)),
]

race = Race(teams, circuits.circuit1)

# Figure out which team index is the player's team and reset their distance_traveled
player_team_index = 0
for x in range(0, len(race.teams)):
  race.teams[x].vehicle.distance_traveled = 0
  race.teams[x].vehicle.speed = 0
  if (race.teams[x].isPlayer):
    player_team_index = x




barricade_locations = [] # holds tuples of x, y barricade locations
ticks = 0
key = tcod.Key()
mouse = tcod.Mouse()
exit_game = False
tcod.console_set_default_foreground(con, tcod.white)
vehicles_collided = set([])

tiles_per_second = 5
seconds_per_tile = 1 / tiles_per_second
# so move forward once every `seconds_per_tile`
# constantly update veh.distance_traveled as int(speed / TOTAL time of race)

### GAME LOOP #################################################################
race_start_time = tcod.sys_elapsed_seconds()
distance_traveled = 0

for team in teams:
  team.vehicle.speed = team.vehicle.max_speed
while not tcod.console_is_window_closed() and not exit_game:
  tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)         

  time_elapsed_since_start = tcod.sys_elapsed_seconds() - race_start_time
  for team in teams:
    if team.vehicle in vehicles_collided:
      handle_post_collision(team.vehicle)

    elif team.isPlayer:
      action = handle_keys(key)
      steer = action.get('steer')
      exit = action.get('exit')

      if steer:
        teams[player_team_index].vehicle.x += steer
      
      if exit:
        exit_game = True
    distance_traveled = time_elapsed_since_start * team.vehicle.speed
    team.vehicle.advance(int(distance_traveled))

  # Check for collisions
  vehicles_collided.clear()
  handle_collisions(race, vehicles_collided, barricade_locations)

  tcod.console_clear(con)
  print_race(con, race, int(distance_traveled), barricade_locations)
  tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,)
  tcod.console_flush()

  #sleep(0.1)


quit()