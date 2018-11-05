import libtcodpy as tcod
from input_handlers import handle_keys
from race import Race
from team import Team
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

# def get_key_event(turn_based=None):
#   if turn_based:
#     key = tcod.console_wait_for_keypress(True)
#   else:
#     key = tcod.console_check_for_keypress()

#   return key


# def handle_keys():
#   key = get_key_event(TURN_BASED)

#   # Alt+Enter: toggle fullscreen
#   if key.vk == tcod.KEY_ENTER and key.lalt:
#     tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
#   # Escape: exit game
#   elif key.vk == tcod.KEY_ESCAPE:
#     return True


def print_track(con, race):
  lane_count = len(race.teams)
  lane_size = race.lane_size
  track_width = ((lane_size + 1) * lane_count) + 1

  for row in range(0, 30):
    for col in range(0, track_width):

      # Print barricades
      if col == 0 or col == track_width - 1:
        tcod.console_put_char(con, col, row, race.barricade, tcod.BKGND_NONE)

      else:
        lane = int(col / (lane_size + 1))
        col_within_lane = col - (lane * (lane_size + 1))

        # Print lane stripes
        if col_within_lane == 0 and row % 3 == 0:
          tcod.console_put_char(con, col, row, race.lane_stripe, tcod.BKGND_NONE)


def print_vehicles(con, race):
  # Print all vehicles
  for n in range(0, len(race.teams)):
    for row in range(0, len(race.teams[n].vehicle.body.rows)):
      for col in range(0, len(race.teams[n].vehicle.body.rows[row])):
        x = race.teams[n].vehicle.x + col
        y = race.teams[n].vehicle.y + row
        tcod.console_put_char(con, x, y, race.teams[n].vehicle.body.rows[row][col], tcod.BKGND_NONE)


def print_race(con, race):
  print_track(con, race)
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

race = Race(teams)

# Figure out which team index is the player's team
player_team_index = 0
for x in range(0, len(race.teams)):
  if (race.teams[x].isPlayer):
    player_team_index = x
    break




counter = 0
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
  print_race(con, race)
  tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,)
  tcod.console_flush()




  counter += 1   


quit()