import libtcodpy as tcod
from race import Race
import visuals

def print_lyrics(panel, lyrics, active_character):
  # primary_color = tcod.cyan
  # primary_color_dark = tcod.darkest_cyan
  # primary_color = tcod.turquoise
  # primary_color_dark = tcod.darkest_turquoise
  primary_color = tcod.sea
  primary_color_dark = tcod.darkest_sea

  tcod.console_set_default_foreground(panel, primary_color)
  tcod.console_set_default_background(panel, tcod.black)
  
  tcod.console_set_color_control(tcod.COLCTRL_1, primary_color_dark, tcod.black)
  tcod.console_set_color_control(tcod.COLCTRL_2, tcod.black, primary_color)

  lyrics_pre_active = '%c{}%c'.format(lyrics[:active_character])%(tcod.COLCTRL_1, tcod.COLCTRL_STOP)
  lyrics_active = '%c{}%c'.format(lyrics[active_character])%(tcod.COLCTRL_2, tcod.COLCTRL_STOP)
  lyrics_post_active = lyrics[active_character + 1:]
  formatted_lyrics = lyrics_pre_active + lyrics_active + lyrics_post_active

  x = int(tcod.console_get_width(panel) / 2)
  y = 0
  w = tcod.console_get_width(panel)
  h = tcod.console_get_height(panel)
  
  tcod.console_print_rect_ex(panel, x, y, w, h, tcod.BKGND_SET, tcod.CENTER, formatted_lyrics)


def print_track(con, race, distance_traveled_by_player, barricade_locations_holder):
  barricade_locations_holder.clear()
  lane_count = len(race.teams)
  lane_size = race.lane_size
  NUM_ROWS_TO_DISPLAY = 30
  track_width = ((lane_size + 1) * lane_count) + 1

  for track_row in range(int(distance_traveled_by_player), int(distance_traveled_by_player) + NUM_ROWS_TO_DISPLAY):
    offset = race.circuit.track_shape[track_row][1]
    left_edge = 0 + offset

    for col in range(left_edge, track_width + left_edge + 1):
      # Print barricades
      if col == left_edge or col == left_edge + track_width - 1:
        barricade_locations_holder.append((col, int(distance_traveled_by_player) + NUM_ROWS_TO_DISPLAY - track_row))
        tcod.console_put_char(con, col, int(distance_traveled_by_player) + NUM_ROWS_TO_DISPLAY - track_row, visuals.BARRICADE, tcod.BKGND_NONE)
      
      # Print lane stripes
      else:
        lane = int(col / (lane_size + 1))
        col_within_lane = col - (lane * (lane_size + 1))

        if col_within_lane == 0:
          tcod.console_put_char(con, col + offset, int(distance_traveled_by_player) + NUM_ROWS_TO_DISPLAY - track_row, str(race.circuit.track_shape[track_row][0]), tcod.BKGND_NONE)


def print_vehicles(con, race, distance_traveled_by_player):
  # Print all vehicles
  for n in range(0, len(race.teams)):
    # All vehicles are displayed vertically relative to player
    new_y = distance_traveled_by_player - race.teams[n].vehicle.distance_traveled
    race.teams[n].vehicle.y += int(new_y)
    for row in range(0, len(race.teams[n].vehicle.body.rows)):
      for col in range(0, len(race.teams[n].vehicle.body.rows[row])):
        x = race.teams[n].vehicle.x + col
        y = race.teams[n].vehicle.y + row
        tcod.console_put_char(con, x, int(y), race.teams[n].vehicle.body.rows[row][col], tcod.BKGND_NONE)
        tcod.console_set_char_foreground(con, x, int(y), race.teams[n].vehicle.color)


def print_race(con, race, distance_traveled_by_player, barricade_locations_holder):
  print_track(con, race, distance_traveled_by_player, barricade_locations_holder)
  print_vehicles(con, race, distance_traveled_by_player)
