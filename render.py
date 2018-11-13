import libtcodpy as tcod

import global_data as g
from race import Race
from track_direction import Track_Direction as td
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

# print_panel_side
# 
# panel: libtcod console
# race_stats: list of Interval Stat objects
def print_panel_side(panel, race_stats, panel_width):
  primary_color = tcod.white
  
  tcod.console_set_default_foreground(panel, primary_color)

  MAX_INTERVAL_STRING_SIZE = 7 # ("+" -> hundreds digit -> decimal -> hundredths digit)

  stat_list = []
  for team_stat in race_stats:
    place_str = str(team_stat.place)
    interval_string_size = len(team_stat.interval)
    pre_interval_spaces = ' '
    pre_interval_spaces += ' ' * (MAX_INTERVAL_STRING_SIZE - interval_string_size)
    team_name = team_stat.team.name
    full_string_size = len(place_str) + 1 + len(team_name) + len(pre_interval_spaces) + interval_string_size
    # Add spaces before interval to make it right-align
    if full_string_size <= panel_width:
      additional_spaces = panel_width - full_string_size
      pre_interval_spaces += ' ' * additional_spaces
    # Truncate team name to make it fit
    else:
      exceeded = full_string_size - panel_width
      team_name = team_name[:-exceeded]

    r = 255
    g = 255
    b = 255
    if team_stat.team.isPlayer:
      r = team_stat.team.vehicle.color.r + 256
      g = team_stat.team.vehicle.color.g + 256
      b = team_stat.team.vehicle.color.b + 256

    if not team_stat.team.finished_current_race:
      team_name = '%c%c%c%c{}%c'.format(team_name)%(tcod.COLCTRL_FORE_RGB, r, g, b, tcod.COLCTRL_STOP)
    else:
      team_name = '%c%c%c%c%c%c%c%c{}%c'.format(team_name)%(tcod.COLCTRL_BACK_RGB, r, g, b, tcod.COLCTRL_FORE_RGB, 0+256, 0+256, 0+256, tcod.COLCTRL_STOP)

    
    stat_text = place_str + ' ' + team_name + pre_interval_spaces + team_stat.interval
    stat_list.append(stat_text)

  line_no = 0
  for stat_line in stat_list:
    tcod.console_print_ex(panel, 0, line_no, tcod.BKGND_SET, tcod.LEFT, stat_line)
    line_no += 1


def print_track(con, race, distance_traveled_by_player, barricade_locations_holder):
  barricade_locations_holder.clear()
  lane_count = len(race.teams)
  lane_size = race.lane_size
  track_width = ((lane_size + 1) * lane_count) + 1

  for track_row in range(int(distance_traveled_by_player), int(distance_traveled_by_player) + g.TRACK_ROWS_TO_DISPLAY):
    track_length = len(race.circuit.track_shape)
    if track_row < track_length:
      offset = race.circuit.track_shape[track_row][1]
    else:
      offset = race.circuit.track_shape[track_length - 1][1]
    left_edge = 0 + offset


    for col in range(left_edge, track_width + left_edge + 1):
      # Print barricades
      if col == left_edge or col == left_edge + track_width - 1:
        barricade_locations_holder.append((col, int(distance_traveled_by_player) + g.TRACK_ROWS_TO_DISPLAY - track_row))
        tcod.console_put_char(con, col, int(distance_traveled_by_player) + g.TRACK_ROWS_TO_DISPLAY - track_row, visuals.BARRICADE, tcod.BKGND_NONE)
      
      # Print lane stripes
      else:
        lane = int(col / (lane_size + 1))
        col_within_lane = col - (lane * (lane_size + 1))

        if col_within_lane == 0:
          if track_row < track_length:
            lane_stripe = str(race.circuit.track_shape[track_row][0])
          else:
            lane_stripe = race.circuit.STRIPE_CHARS[td.STRAIGHT]
          tcod.console_put_char(con, col + offset, int(distance_traveled_by_player) + g.TRACK_ROWS_TO_DISPLAY - track_row, lane_stripe, tcod.BKGND_NONE)
          
          

      # Print finish line at end
      if track_row == track_length:
        tcod.console_put_char(con, col + offset, int(distance_traveled_by_player) + g.TRACK_ROWS_TO_DISPLAY - track_row, '-', tcod.BKGND_NONE)


def print_vehicles(con, race, distance_traveled_by_player):
  # Print all vehicles
  for n in range(0, len(race.teams)):
    # All vehicles are displayed vertically relative to player
    new_y = distance_traveled_by_player - race.teams[n].vehicle.distance_traveled
    race.teams[n].vehicle.y = int(new_y)
    for row in range(0, len(race.teams[n].vehicle.body.rows)):
      for col in range(0, len(race.teams[n].vehicle.body.rows[row])):
        x = race.teams[n].vehicle.x + col
        y = race.teams[n].vehicle.y + row + round(g.TRACK_ROWS_TO_DISPLAY / 2)
        tcod.console_put_char(con, x, int(y), race.teams[n].vehicle.body.rows[row][col], tcod.BKGND_NONE)
        tcod.console_set_char_foreground(con, x, int(y), race.teams[n].vehicle.color)


def print_race(con, race, distance_traveled_by_player, barricade_locations_holder):
  print_track(con, race, distance_traveled_by_player, barricade_locations_holder)
  print_vehicles(con, race, distance_traveled_by_player)
