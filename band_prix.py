import libtcodpy as tcod

import circuits
from context import Context
import global_data as g
from input_handlers import handle_keys
from interval_stat import Interval_Stat
import lexicons as lex
from physics import *
from race import Race
import random
from render import *
from song_generator import build_song
from team import Team
from time import sleep
from track_direction import Track_Direction as td
from vehicle import Vehicle
from vehicle_body import Vehicle_Body
import vehicle_bodies
import visuals


def get_distance_traveled(team):
  return team.vehicle.distance_traveled

# build_race_stats
#
# returns list of Interval_Stat objects in proper order
def build_race_stats(race):  
  ordered_race_stats = []

  # Teams that have finished are locked in place based on finishing info
  already_finished = [] # This will make things simpler later in the function
  for place_team in race.finished_teams:
    place = place_team[0]
    team = place_team[1]
    time = str(format(round((race.finish_times[team]), 2), '.2f'))
    ordered_race_stats.append(Interval_Stat(place_team[0], place_team[1], time))
    already_finished.append(team)

  sorted_teams = sorted(race.teams, key=get_distance_traveled, reverse=True)

  # Now list non-finished teams
  counter = 1
  for team in sorted_teams:
    place = counter
    if team not in already_finished:
      dist_to_first = sorted_teams[0].vehicle.distance_traveled - team.vehicle.distance_traveled

      # Check for tie with most recently checked vehicle
      if len(ordered_race_stats) > 0:
        if team.vehicle.distance_traveled == ordered_race_stats[len(ordered_race_stats) - 1].team.vehicle.distance_traveled:
          place = ordered_race_stats[len(ordered_race_stats) - 1].place

      interval = '----'
      if (team.vehicle.speed >= 1):
        interval = '+' + str(format(round((dist_to_first / team.vehicle.speed), 2), '.2f'))
      ordered_race_stats.append(Interval_Stat(place, team, interval))
    counter += 1

  return ordered_race_stats



def check_key_char_input(pressed_key_char, lyrics, active_lyrics_character):
  target_char = lyrics[active_lyrics_character].lower()
  correct = pressed_key_char.lower() == target_char
  
  if correct:
    return True
  else:
    return False


def finish_race(race, team, time):
  # Update race finishing places and times ####################################

  finished_teams_count = len(race.finished_teams)

  # First check and see if this team ties with another
  tie_occurred = False
  if finished_teams_count > 0:
    latest_place = race.finished_teams[finished_teams_count - 1][0]
    latest_team = race.finished_teams[finished_teams_count - 1][1]
    latest_time = race.finish_times[latest_team]

    # If this team ties with the previously finished team
    if latest_time == time:
      tie_occurred = True
      # Update pertinent info
      race.finished_teams.append((latest_place, team))

  if not tie_occurred:
    finishing_place = finished_teams_count + 1
    race.finished_teams.append((finishing_place, team))

  # This happens the same way regardless of a tie
  race.finish_times[team] = time


  # Misc other things to take care of #########################################
  team.finished_current_race = True
  team.vehicle.acceleration = 0



FPS_CAP = 60
#frame_render_time = 1 / FPS_CAP
fullscreen = False
GAME_TITLE = 'Band Prix'
#font_path = 'arial10x10.png'
#font_path = 'arial12x12.png'
#font_path = 'consolas10x10_gs_tc.png'
#font_path  = 'lucida12x12_gs_tc.png'
#font_path  = 'terminal10x10_gs_tc.png'

#layout = tcod.FONT_LAYOUT_TCOD

font_path = 'terminal16x16_gs_ro.png'
layout = tcod.FONT_LAYOUT_ASCII_INROW

font_flags = tcod.FONT_TYPE_GREYSCALE | layout
TURN_BASED = False



main_viewport_height = 50
main_viewport_width = 80
panel_height = 7
panel_side_width = 30

screen_width = main_viewport_width + panel_side_width
screen_height = main_viewport_height + panel_height

# Viewports ###################################################################
tcod.console_set_custom_font(font_path, font_flags)
tcod.console_init_root(screen_width, screen_height, GAME_TITLE, fullscreen)

con = tcod.console_new(main_viewport_width, main_viewport_height)

panel_y = screen_height - panel_height
panel = tcod.console_new(main_viewport_width, panel_height)
tcod.console_set_alignment(panel, tcod.LEFT)

panel_side_x = screen_width - panel_side_width
panel_side = tcod.console_new(panel_side_width, screen_height)

full_panel = tcod.console_new(screen_width, screen_height)
tcod.console_set_alignment(full_panel, tcod.LEFT)
# End viewports ###############################################################



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
teams[2].vehicle.max_speed = 30
teams[2].vehicle.max_acceleration = 4
teams[3].vehicle.max_acceleration = 4
teams[3].vehicle.max_speed = 30

lyrics = [
  'My thoughts are frozen',
  'Like everyone else',
  'You will always be remembered',
  'Even life itself',
  'Say it to me SANTOS',
  'And try to make it rhyme',
  'Say it to me SANTOS',
  'In normal moving time',
  'Say it to me SANTOS',
  'It\'s off to work we go',
  'Say it to me SANTOS',
  'HI HO HI HO HI HO',
  'This is what space smells like',
  'You will always remember where you were',
  'This is what space smells like',
  'You will always remember where you were'
]

race = Race(teams, circuits.circuit1, lyrics)

# Figure out which team index is the player's team; also reset all vehciles' distance_traveled
player_team_index = 0
for x in range(0, len(race.teams)):
  race.teams[x].vehicle.distance_traveled = 0
  race.teams[x].vehicle.speed = 0
  race.teams[x].finished_current_race = False
  if (race.teams[x].isPlayer):
    player_team_index = x



verse = 0
song_completed = False
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
keypress_timer = 99999
### GAME LOOP #################################################################
race_start_time = tcod.sys_elapsed_seconds()

# debug
all_time_recorded = []

#context = Context.RACE
context = Context.TEAM_CREATION
while not tcod.console_is_window_closed() and not exit_game:
  if context == Context.RACE:
    tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)       
    active_key_char = race.lyrics[verse][active_lyrics_character]


    keypress_timer += tcod.sys_get_last_frame_length()
    total_time_elapsed = tcod.sys_elapsed_seconds()
    time_elapsed_last_frame = tcod.sys_get_last_frame_length()


    for team in teams:
      # Apply collision physics if needed
      if team.vehicle in vehicles_collided:
        handle_post_collision(team.vehicle)

      else:
        if team.vehicle.distance_traveled >= len(race.circuit.track_shape) and not team.finished_current_race:
          finish_race(race, team, total_time_elapsed)

        # Control player vehicle
        if team.isPlayer:
          action = handle_keys(key)
          pressed_key_char = action.get('key_char')
          steer = action.get('steer')
          exit = action.get('exit')
          powerpct = g.get_powerpct_from_keyspeed(keypress_timer)
          team.vehicle.apply_power(powerpct)
          # debug
          #team.vehicle.apply_power(.9)


          if pressed_key_char:
            correct = check_key_char_input(pressed_key_char, lyrics[verse], active_lyrics_character)
            if correct:
              keypress_timer = 0.0
              active_lyrics_character += 1
              if (active_lyrics_character >= len(lyrics[verse])):
                active_lyrics_character = 0
                verse += 1
                if verse >= len(lyrics):
                  song_completed = True

            else:
              pass

          if steer:
            teams[player_team_index].vehicle.x += steer
          
          if exit:
            exit_game = True

        # If team is not player
        else:
          # debug
          team.vehicle.apply_power(random.uniform(0.33, 1.00))
          #team.vehicle.apply_power(1)

      # Apply acceleration, determine speed
      speed_to_add = time_elapsed_last_frame * team.vehicle.acceleration
      team.vehicle.speed += speed_to_add
      if team.vehicle.speed > team.vehicle.current_max_speed_from_power:
        team.vehicle.speed -= 0.1
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
    print_race(con, race, int(teams[player_team_index].vehicle.y), int(teams[player_team_index].vehicle.distance_traveled), barricade_locations)
    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0,)

    tcod.console_clear(panel)
    print_lyrics(panel, race.lyrics[verse], active_lyrics_character)
    tcod.console_blit(panel, 0, 0, main_viewport_width, panel_height, 0, 0, panel_y)

    tcod.console_clear(panel_side)
    print_panel_side(panel_side, build_race_stats(race), panel_side_width)
    tcod.console_blit(panel_side, 0, 0, panel_side_width, screen_height, 0, panel_side_x, 0)

    tcod.console_flush()

  elif context == Context.TEAM_CREATION:
    question = 'What is the name of your team?'
    answer = ''
    name_confirmed = False
    while not name_confirmed:
      tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)       
      answer_line = '> ' + answer.title()

      action = handle_keys(key)
      pressed_key_char = action.get('key_char')
      pressed_backspace = action.get('backspace')
      if pressed_key_char:
        answer += pressed_key_char

      elif pressed_backspace:
        answer = answer[:-1]

      tcod.console_clear(full_panel)
      
      tcod.console_set_default_foreground(full_panel, tcod.sea)
      tcod.console_set_default_background(full_panel, tcod.black)

      tcod.console_print_rect_ex(full_panel, 0, 0, screen_width, screen_height, tcod.BKGND_SET, tcod.LEFT, question)
      tcod.console_print_rect_ex(full_panel, 0, 1, screen_width, screen_height, tcod.BKGND_SET, tcod.LEFT, answer_line)
      tcod.console_blit(full_panel, 0, 0, screen_height, screen_height, 0, 0, 0)

      tcod.console_flush()

  


  #sleep(0.1)
 
quit()