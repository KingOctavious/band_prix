import libtcodpy as tcod

import global_data as g
from input_handlers import handle_keys
from interval_stat import Interval_Stat
from physics import *
from race import Race
import random
from render import *

###############################################################################
# Context handlers
###############################################################################
# These are the major functions of the game (and their helper functions) that
# cause the game to run.
###############################################################################

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



def do_race(race, key, mouse):
  main_viewport_height = 50
  main_viewport_width = 80
  bottom_viewport_height = 7
  side_viewport_width = 30
  main_viewport = tcod.console_new(main_viewport_width, main_viewport_height)

  bottom_viewport_y = g.screen_height - bottom_viewport_height
  bottom_viewport = tcod.console_new(main_viewport_width, bottom_viewport_height)
  tcod.console_set_alignment(bottom_viewport, tcod.LEFT)

  side_viewport_x = g.screen_width - side_viewport_width  
  side_viewport = tcod.console_new(side_viewport_width, g.screen_height)

  teams = race.teams
  player_team_index = 0
  for x in range(0, len(teams)):
    if (race.teams[x].isPlayer):
      player_team_index = x
      break;
  lyrics = race.lyrics
  last_time_accelerated = 0
  vehicles_collided = set([])
  active_lyrics_character = 0
  keypress_timer = 99999
  race_finished = False
  race_start_time = tcod.sys_elapsed_seconds()
  verse = 0
  speed_increase_this_turn = 0
  song_completed = False
  barricade_locations = [] # holds tuples of x, y barricade locations

  while not race_finished:
    tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)       
    active_key_char = lyrics[verse][active_lyrics_character]

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
            correct = check_key_char_input(pressed_key_char, race.lyrics[verse], active_lyrics_character)
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
    tcod.console_clear(main_viewport)
    print_race(main_viewport, race, int(teams[player_team_index].vehicle.y), int(teams[player_team_index].vehicle.distance_traveled), barricade_locations)
    tcod.console_blit(main_viewport, 0, 0, g.screen_width, g.screen_height, 0, 0, 0,)

    tcod.console_clear(bottom_viewport)
    print_lyrics(bottom_viewport, race.lyrics[verse], active_lyrics_character)
    tcod.console_blit(bottom_viewport, 0, 0, main_viewport_width, bottom_viewport_height, 0, 0, bottom_viewport_y)

    tcod.console_clear(side_viewport)
    print_panel_side(side_viewport, build_race_stats(race), side_viewport_width)
    tcod.console_blit(side_viewport, 0, 0, side_viewport_width, g.screen_height, 0, side_viewport_x, 0)

    tcod.console_flush()


def get_distance_traveled(team):
  return team.vehicle.distance_traveled