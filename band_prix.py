import libtcodpy as tcod
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

def get_key_event(turn_based=None):
  if turn_based:
    key = tcod.console_wait_for_keypress(True)
  else:
    key = tcod.console_check_for_keypress()

  return key


def handle_keys():
  key = get_key_event(TURN_BASED)

  # Alt+Enter: toggle fullscreen
  if key.vk == tcod.KEY_ENTER and key.lalt:
    tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
  # Escape: exit game
  elif key.vk == tcod.KEY_ESCAPE:
    return True


tcod.console_set_custom_font(font_path, font_flags)
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, fullscreen)
tcod.sys_set_fps(LIMIT_FPS)




teams = [
  Team('Kasvot Vaxt', Vehicle(vehicle_bodies.v_bod_1)),
  Team('ViscDuds', Vehicle(vehicle_bodies.v_bod_1)),
  Team('The Jack Straw Band', Vehicle(vehicle_bodies.v_bod_1)),
  Team('The Billiards', Vehicle(vehicle_bodies.v_bod_1)),
  Team('Strange Dan Gustafvist', Vehicle(vehicle_bodies.v_bod_1)),
]

race = Race(teams)

lane_count = len(race.teams)
lane_size = race.lane_size
track_width = ((lane_size + 1) * lane_count) + 1
vehicle_draw_offset_from_top = 2


exit_game = False
while not tcod.console_is_window_closed() and not exit_game:
  tcod.console_set_default_foreground(0, tcod.pink)

  for row in range(0, 30):
    for col in range(0, track_width):

      if col == 0 or col == track_width - 1:
        tcod.console_put_char(0, col, row, race.barricade, tcod.BKGND_NONE)

      else:
        # Track which lane and which column whithin the lane we're in to keep 
        # things easier later
        lane = int(col / (lane_size + 1))
        col_within_lane = col - (lane * (lane_size + 1))
        vehicle_this_lane = teams[lane].vehicle
        veh_width = vehicle_this_lane.body.width

        # Print lane stripes
        if col_within_lane == 0:
          tcod.console_put_char(0, col, row, race.lane_stripe, tcod.BKGND_NONE)

        else:
          veh_bod_row = row - vehicle_draw_offset_from_top
          veh_bod_col = col_within_lane - race.lane_padding - 1

          # veh_bod_row and ..._col are assigned regardless of whether they are
          # actually parts of the car body. So, here we need to validate.
          if veh_bod_row >= 0 and veh_bod_row < vehicle_this_lane.body.length and veh_bod_col >= 0 and veh_bod_col < len(vehicle_this_lane.body.rows[veh_bod_row]):
            tcod.console_put_char(0, col, row, vehicle_this_lane.body.rows[veh_bod_row][veh_bod_col], tcod.BKGND_NONE)


  tcod.console_flush()

   


  exit_game = handle_keys()

quit()