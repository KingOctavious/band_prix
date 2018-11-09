import libtcodpy as tcod

import circuits
import global_data as g
from input_handlers import handle_keys
from physics import *
from race import Race
from render import print_race, print_lyrics
from team import Team
from time import sleep
from track_direction import Track_Direction as td
from vehicle import Vehicle
from vehicle_body import Vehicle_Body
import vehicle_bodies
import visuals


def check_key_char_input(pressed_key_char, lyrics, active_lyrics_character):
  target_char = lyrics[active_lyrics_character].lower()
  correct = pressed_key_char.lower() == target_char
  
  if correct:
    return True
  else:
    return False



FPS_CAP = 60
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




screen_width = 80
screen_height = 50
panel_height = 7
panel_y = screen_height - panel_height

tcod.console_set_custom_font(font_path, font_flags)
tcod.console_init_root(screen_width, screen_height, GAME_TITLE, fullscreen)

con = tcod.console_new(screen_width, screen_height)

panel = tcod.console_new(screen_width, panel_height)
tcod.console_set_alignment(panel, tcod.LEFT)

tcod.sys_set_fps(FPS_CAP)



teams = [
  Team('Kasvot Vaxt', Vehicle(vehicle_bodies.v_bod_1, tcod.yellow)),
  Team('ViscDuds', Vehicle(vehicle_bodies.v_bod_1, tcod.green)),
  Team('The Jack Straw Band', Vehicle(vehicle_bodies.v_bod_1, tcod.pink), True),
  Team('The Billiards', Vehicle(vehicle_bodies.v_bod_1, tcod.orange)),
  Team('Strange Dan Gustafvist', Vehicle(vehicle_bodies.v_bod_1, tcod.light_cyan)),
]

# debug
teams[0].vehicle.max_speed = 1
teams[2].vehicle.acceleration = 3
teams[3].vehicle.acceleration = 4
teams[3].vehicle.max_speed = 4

lyrics = "This is what space smells like"
race = Race(teams, circuits.circuit1, lyrics)

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
speed_increase_this_turn = 0
tcod.console_set_default_foreground(con, tcod.white)
last_time_accelerated = 0
vehicles_collided = set([])
active_lyrics_character = 0
keypress_timer = 0.0
time_for_this_key = 99999
### GAME LOOP #################################################################
race_start_time = tcod.sys_elapsed_seconds()

# debug
all_time_recorded = []

while not tcod.console_is_window_closed() and not exit_game:
  active_key_char = race.lyrics[active_lyrics_character]
  tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)         

  keypress_timer += tcod.sys_get_last_frame_length()
  total_time_elapsed = tcod.sys_elapsed_seconds()
  time_elapsed_last_frame = tcod.sys_get_last_frame_length()
  # Acceleration is applied once every second.
  time_passed_since_last_reset = int(total_time_elapsed) - int(last_time_accelerated)
  if (time_passed_since_last_reset > 0):
    last_time_accelerated = total_time_elapsed

  for team in teams:
    # Apply collision physics if needed
    if team.vehicle in vehicles_collided:
      handle_post_collision(team.vehicle)

    # Control player vehicle
    elif team.isPlayer:
      action = handle_keys(key)

      pressed_key_char = action.get('key_char')
      steer = action.get('steer')
      exit = action.get('exit')

      if pressed_key_char:
        correct = check_key_char_input(pressed_key_char, lyrics, active_lyrics_character)
        if correct:
          if active_lyrics_character > 0:
            time_for_this_key = keypress_timer
            all_time_recorded.append(time_for_this_key)
            #print('avg time: {}'.format(sum(all_time_recorded) / len(all_time_recorded)))
            print(g.get_accel_from_keyspeed(time_for_this_key))
          active_lyrics_character += 1
          keypress_timer = 0.0
        else:
          pass

      if steer:
        teams[player_team_index].vehicle.x += steer
      
      if exit:
        exit_game = True

    # Apply acceleration, determine speed
    team.vehicle.speed += time_passed_since_last_reset * team.vehicle.acceleration
    if team.vehicle.speed > team.vehicle.max_speed:
      team.vehicle.speed = team.vehicle.max_speed
    elif team.vehicle.speed < 0:
      team.vehicle.speed = 0
    team.vehicle.distance_traveled += time_elapsed_last_frame * team.vehicle.speed

  # Check for collisions
  vehicles_collided.clear()
  handle_collisions(race, vehicles_collided, barricade_locations)

  # Render
  tcod.console_clear(con)
  print_race(con, race, int(teams[player_team_index].vehicle.distance_traveled), barricade_locations)
  tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0,)

  tcod.console_clear(panel)
  print_lyrics(panel, race.lyrics, active_lyrics_character)
  tcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

  tcod.console_flush()


  #sleep(0.1)


quit()