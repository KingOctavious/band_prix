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
import teams as t
import time
from vehicle import Vehicle
import vehicle_bodies


###############################################################################
# Context handlers
###############################################################################
# These are the major functions of the game (and their helper functions) that
# cause the game to run.
###############################################################################


# Helper functions
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


def get_distance_traveled(team):
  return team.vehicle.distance_traveled


# get_race_intro
#
# Returns list of tuples containing the line of text that should be displayed,
# coupled with the time (in seconds) to display each.
def get_race_intro(song_title, lexicon, circuit):
  announcement = [
    ('Welcome to the {}!'.format(circuit.name), 2),
    ('Today you will be playing the hit {} song'.format(lexicon.name), 1),
    ('Today you will be playing the hit {} song'.format(lexicon.name) + '\n' + '\n' + '\n' + '"{}"'.format(song_title), 2.5),
    ('Get ready!', 1),
    ('Get ready!' + '\n' + '\n' + '\n' + '\n' + '%c%c%c%c*%c'%(tcod.COLCTRL_FORE_RGB, tcod.red.r + 256, tcod.red.g + 256, tcod.red.b + 256, tcod.COLCTRL_STOP), 1),
    ('Get ready!' + '\n' + '\n' + '\n' + '\n' + '%c%c%c%c* * *%c'%(tcod.COLCTRL_FORE_RGB, tcod.red.r + 256, tcod.red.g + 256, tcod.red.b + 256, tcod.COLCTRL_STOP), 1),
    ('Get ready!' + '\n' + '\n' + '\n' + '\n' + '%c%c%c%c* * * * *%c'%(tcod.COLCTRL_FORE_RGB, tcod.red.r + 256, tcod.red.g + 256, tcod.red.b + 256, tcod.COLCTRL_STOP), 1),
  ]

  return announcement


# Returns dictionary in following format:
# {
#   'value': program-usable value of response,
#   'string': string representation of response,
#   'confirmed': bool describing whether input is complete
# } 
def handle_option_selection(key, options):
  confirmed = False
  action = handle_keys(key)
  pressed_key_char = action.get('key_char')
  if pressed_key_char != None:
    pressed_key_char = pressed_key_char.lower()
  response = None
  response_text = ''
  if pressed_key_char in g.ALPHABET:
    index = g.ALPHABET.index(pressed_key_char)
    if index < len(options):
      response = options[index][0]
      response_text = options[index][1]
      confirmed = True

  return {
    'value': response,
    'string' : response_text,
    'confirmed': confirmed
  }


# handle_questions
#
# Takes a dict of questions:options, prints them to the screen, and returns
# the responses in list form. Options should be provided as lists of
# value:string tuples. If the question requires a text-input response,
# provide an empty list argument for the options.
def handle_questions(con, key, mouse, questions_options, con_y_pos=0):
  static_text_to_print = []
  responses = []
  for question, options in questions_options.items():
    response = ''
    confirmed = False
    static_text_to_print.append(question)

    while not confirmed:
      tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)       
      tcod.console_clear(con)
      tcod.console_set_default_foreground(con, tcod.sea)
      tcod.console_set_default_background(con, tcod.black)

      # For open text input
      if len(options) == 0:     
        response_data = handle_text_input(key, response)
        response = response_data['value']
        response_line = '> ' + response_data['string']
        confirmed = response_data['confirmed']
        tcod.console_print_rect_ex(con, 0, len(static_text_to_print), g.screen_width, g.screen_height, tcod.BKGND_SET, tcod.LEFT, response_line)
      # For input with discreet options
      else:
        response_data = handle_option_selection(key, options)
        response = response_data['value']
        response_text = response_data['string']
        response_line = '> ' + response_text
        confirmed = response_data['confirmed']
        # Display options
        for x in range(0, len(options)):
          option_text = g.ALPHABET[x] + '. ' + options[x][1]
          tcod.console_print_rect_ex(con, 0, len(static_text_to_print) + x, g.screen_width, g.screen_height, tcod.BKGND_SET, tcod.LEFT, option_text)

      # Once we get a response, do this stuff:
      if confirmed:
        if len(options) > 0:
          # Clear to remove list of options
          tcod.console_clear(con)
        static_text_to_print.append(response_line)
        responses.append(response)

      # Do this stuff every time no matter what
      for x in range(0, len(static_text_to_print)):
        tcod.console_print_rect_ex(con, 0, x, g.screen_width, g.screen_height, tcod.BKGND_SET, tcod.LEFT, static_text_to_print[x])
      tcod.console_blit(con, 0, 0, g.screen_height, g.screen_height, 0, 0, con_y_pos)
      tcod.console_flush()


  time.sleep(0.2)
  return responses


# Returns dictionary in following format:
# {
#   'value': program-usable value of response,
#   'string': string representation of response,
#   'confirmed': bool describing whether input is complete
# } 
def handle_text_input(key, response):
  confirmed = False
  action = handle_keys(key)
  pressed_key_char = action.get('key_char')
  pressed_backspace = action.get('backspace')
  pressed_enter = action.get('confirm')

  RESPONSE_MAX = 30
  if pressed_key_char and len(response) < RESPONSE_MAX:
    response += pressed_key_char
  elif pressed_backspace:
    response = response[:-1]
  elif pressed_enter:
    confirmed = True

  return {
    'value': response,
    'string': response,
    'confirmed': confirmed
  }


# Handler functions
###############################################################################

def do_main_menu(key, mouse):
  title_panel_h = 28
  title_panel = tcod.console_new(g.screen_width, title_panel_h)
  tcod.console_set_alignment(title_panel, tcod.LEFT)
  tcod.console_set_default_foreground(title_panel, tcod.blue)
  for x in range(0, len(g.TITLE_GRAPHIC_TOP)):
    tcod.console_print_ex(title_panel, 1, x + 1, tcod.BKGND_SET, tcod.LEFT, g.TITLE_GRAPHIC_TOP[x][0])

  for x in range(0, len(g.TITLE_GRAPHIC_BOTTOM)):
    tcod.console_print_ex(title_panel, 1, x + 4 + len(g.TITLE_GRAPHIC_TOP), tcod.BKGND_SET, tcod.LEFT, g.TITLE_GRAPHIC_BOTTOM[x][0])

  selection_panel = tcod.console_new(g.screen_width, g.screen_height - title_panel_h)
  tcod.console_set_alignment(selection_panel, tcod.LEFT)
  tcod.console_set_default_foreground(selection_panel, tcod.sea)

  title_colors = [
    tcod.azure,
    tcod.cyan,
    tcod.dark_purple,
    tcod.dark_violet,
    tcod.fuchsia,
    tcod.light_gray,
    tcod.purple,
    tcod.sea,
    tcod.turquoise,
  ]

  questions_options = {
    '': [
      ('start', 'Start'),
      ('exit', 'Exit game')
    ]
  }

  waiting_for_response = True
  while waiting_for_response:
    for y in range(1, 1 + len(g.TITLE_GRAPHIC_TOP)):
      color_index = random.randint(0, len(title_colors) - 1)
      for x in range(0, g.screen_width):
        tcod.console_set_char_foreground(title_panel, x, y, title_colors[color_index])
    
    tcod.console_blit(title_panel, 0, 0, g.screen_width, title_panel_h, 0, 0, 0)

    tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
    selection = handle_questions(selection_panel, key, mouse, questions_options, 24)
    if len(selection) > 0:
      if selection[0] == 'start':
        g.context = Context.TEAM_CREATION
        waiting_for_response = False
      elif selection[0] == 'exit':
        g.context = Context.EXIT
        waiting_for_response = False

  tcod.console_clear(title_panel)
  tcod.console_blit(title_panel, 0, 0, g.screen_width, title_panel_h, 0, 0, 0)
  tcod.console_clear(selection_panel)
  tcod.console_blit(selection_panel, 0, 0, g.screen_width, title_panel_h, 0, 0, 0)
  tcod.console_flush()


# do_post_race
#
# Store points for this race in the season data, and print post-race display
def do_post_race(key, mouse):
  finished_race = g.season.races[g.season.current_race]

  full_panel = tcod.console_new(g.screen_width, g.screen_height)
  tcod.console_set_alignment(full_panel, tcod.CENTER)
  tcod.console_set_default_foreground(full_panel, tcod.sea)

  tcod.console_clear(full_panel)

  title = finished_race.circuit.name + ' Results'
  tcod.console_print_frame(full_panel, 1, 1, g.screen_width - 2, g.screen_height - 2, False, tcod.BKGND_DEFAULT, title)

  LINE_LENGTH = 50
  header = 'Team' + (' ' * (LINE_LENGTH - 10)) + 'Points'
  underline = '=' * LINE_LENGTH
  tcod.console_print_ex(full_panel, 30, 20, tcod.BKGND_SET, tcod.LEFT, header)
  tcod.console_print_ex(full_panel, 30, 21, tcod.BKGND_SET, tcod.LEFT, underline)
  for place, team in finished_race.places.items():
    # Record point data
    points = g.POINTS[place]
    g.season.standings[team] += points

    # Print info
    place_name = str(place) + '. ' + team.name
    point_string = str(points)
    space_count = LINE_LENGTH - (len(place_name) + len(point_string))
    line = place_name + (' ' * space_count) + point_string

    tcod.console_print_ex(full_panel, 30, 21 + place, tcod.BKGND_SET, tcod.LEFT, line)

  tcod.console_blit(full_panel, 0, 0, g.screen_width, g.screen_height, 0, 0, 0)
  tcod.console_flush()

  # Wait for `tcod.Enter` to continue
  confirm = False
  while not confirm:
    tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
    action = handle_keys(key)
    confirm = action.get('confirm')
  
  if confirm:
    g.season.current_race += 1
    g.context = Context.SEASON_OVERVIEW


def do_race(key, mouse):
  bottom_viewport_height = 7  
  main_viewport_height = g.screen_height - bottom_viewport_height
  main_viewport_width = g.MAIN_VIEWPORT_WIDTH
  side_viewport_width = g.screen_width - main_viewport_width
  main_viewport = tcod.console_new(main_viewport_width, main_viewport_height)

  bottom_viewport_y = g.screen_height - bottom_viewport_height
  bottom_viewport = tcod.console_new(main_viewport_width, bottom_viewport_height)
  tcod.console_set_alignment(bottom_viewport, tcod.LEFT)

  side_viewport_x = g.screen_width - side_viewport_width  
  side_viewport = tcod.console_new(side_viewport_width, g.screen_height)

  intro_w = int(g.screen_width * .35)
  intro_h = int(g.screen_height * .20)
  intro_x = int(g.screen_width * 0.5 - intro_w * 0.5)
  intro_y = int(g.screen_height * 0.5 - intro_h * 0.5)
  intro_window = tcod.console_new(intro_w, intro_h)
  tcod.console_set_alignment(intro_window, tcod.CENTER)
  tcod.console_set_default_foreground(intro_window, tcod.sea)

  lexicon = lex.genres_lexicons[random.randint(0, len(lex.genres_lexicons) - 1)][0]
  title_and_song = build_song(lexicon)
  race = Race(g.season.teams, g.season.circuits[g.season.current_race], title_and_song[1], title_and_song[0])

  # Reset stuff
  for x in range(0, len(race.teams)):
    race.teams[x].reset()

  teams = race.teams
  player_team_index = 0
  lane_count = len(race.teams)
  track_width = ((race.lane_size + 1) * lane_count) + 1
  BASE_OFFSET_TO_CENTER = int((g.MAIN_VIEWPORT_WIDTH - track_width) / 2)
  for x in range(0, len(teams)):
    if (teams[x].isPlayer):
      player_team_index = x
    teams[x].vehicle.x = BASE_OFFSET_TO_CENTER + (x * (race.lane_size + 1)) + 2


  lyrics = race.lyrics
  vehicles_collided = set([])
  active_lyrics_character = 0
  keypress_timer = 99999
  race_finished = False
  race_started = False
  verse = 0
  song_completed = False
  barricade_locations = [] # holds tuples of x, y barricade locations
  intro_lines = get_race_intro(title_and_song[0], lexicon, race.circuit)
  current_intro_line = 0
  first_frame = True
  time_elapsed_last_frame = 0
  race_start_time = tcod.sys_elapsed_seconds()
  while not race_finished:
    tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
    keypress_timer += tcod.sys_get_last_frame_length()
    total_time_elapsed = tcod.sys_elapsed_seconds()
        
    if race_started:
      if not first_frame:
        time_elapsed_last_frame = tcod.sys_get_last_frame_length()
      for team in teams:
        team.ai_run_counters()
        # Apply collision physics if needed
        if team.vehicle in vehicles_collided:
          handle_post_collision(team)

        else:
          if team.vehicle.distance_traveled >= len(race.circuit.track_shape) and not team.finished_current_race:
            finish_race(race, team, total_time_elapsed - race_start_time)

          # Control player vehicle
          if team.isPlayer and not team.finished_current_race:
            action = handle_keys(key)
            pressed_key_char = action.get('key_char')
            steer = action.get('steer')
            exit = action.get('exit')
            if not song_completed:
              powerpct = g.get_powerpct_from_keyspeed(keypress_timer)
            else:
              powerpct = 1
            team.vehicle.apply_power(powerpct)

            if pressed_key_char and not song_completed:
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
                # TODO: mis-steer
                pass

            if steer and team.vehicle.speed > 0: # Can only steer if moving
              teams[player_team_index].vehicle.x += steer
            
            if exit:
              exit_game = True

          # If team is not player
          elif not team.finished_current_race:
            direction = team.ai_determine_direction()
            if direction == td.LEFT:
              team.vehicle.x += -1
            elif direction == td.RIGHT:
              team.vehicle.x += 1
            team.ai_apply_power()

          # If team has reached the finish line
          else:
            team.vehicle.apply_power(0)
            # Don't have time to do proper checks to wait for all teams to
            # finsh race. For now, just wait until the player team's vehicle
            # has coasted to a stop, and then take everyone's place from that
            # moment.
            if team.isPlayer and team.vehicle.speed == 0:
              race_finished = True

        # Apply acceleration, determine speed
        speed_to_add = time_elapsed_last_frame * team.vehicle.acceleration
        team.vehicle.speed += speed_to_add
        if team.vehicle.speed > team.vehicle.current_max_speed_from_power:
          team.vehicle.speed -= 0.1
        if team.vehicle.speed > team.vehicle.max_speed:
          team.vehicle.speed = team.vehicle.max_speed
        elif team.vehicle.speed < 0:
          team.vehicle.speed = 0
        distance_traveled_this_frame = time_elapsed_last_frame * team.vehicle.speed

        team.ai_observe_curves(race.circuit.track_layout, int(team.vehicle.distance_traveled + distance_traveled_this_frame) - int(team.vehicle.distance_traveled)) # This HAS to come first
        team.vehicle.distance_traveled += distance_traveled_this_frame
        

      # Check for collisions
      vehicles_collided.clear()
      handle_collisions(race, vehicles_collided, barricade_locations)

      first_frame = False

    # Render
    tcod.console_clear(main_viewport)
    print_race(main_viewport, race, int(teams[player_team_index].vehicle.y), int(teams[player_team_index].vehicle.distance_traveled), barricade_locations)
    tcod.console_blit(main_viewport, 0, 0, g.screen_width, g.screen_height, 0, 0, 0,)

    tcod.console_clear(bottom_viewport)
    if not song_completed:
      print_lyrics(bottom_viewport, race.lyrics[verse], active_lyrics_character)
    tcod.console_blit(bottom_viewport, 0, 0, main_viewport_width, bottom_viewport_height, 0, 0, bottom_viewport_y)

    tcod.console_clear(side_viewport)
    print_panel_side(side_viewport, build_race_stats(race), side_viewport_width)
    tcod.console_blit(side_viewport, 0, 0, side_viewport_width, g.screen_height - bottom_viewport_height, 0, side_viewport_x, 0)

    if not race_started:
      # This structure is pretty ugly, but no time to clean it up
      if current_intro_line == len(intro_lines):
        time.sleep(intro_lines[current_intro_line - 1][1])
      elif current_intro_line >= len(intro_lines):
        race_started = True
      else:
        tcod.console_clear(intro_window)
        tcod.console_hline(intro_window, 0, 0, intro_w)
        tcod.console_hline(intro_window, 0, intro_h - 1, intro_w)
        tcod.console_vline(intro_window, 0, 0, intro_h)
        tcod.console_vline(intro_window, intro_w - 1, 0, intro_h)
        tcod.console_print_rect_ex(intro_window, int(intro_w/2), 1, intro_w - 3, intro_h - 2, tcod.BKGND_SET, tcod.CENTER, intro_lines[current_intro_line][0])
        tcod.console_blit(intro_window, 0, 0, intro_w, intro_h, 0, intro_x, intro_y)
        if current_intro_line > 0:
          time.sleep(intro_lines[current_intro_line - 1][1])
      current_intro_line += 1

    tcod.console_flush()

  # Race is finished
  final_stats = build_race_stats(race)
  place = 1
  for stat in final_stats:
    race.places[place] = stat.team
    place += 1
  g.season.races.append(race)

  g.context = Context.POST_RACE


def do_season_overview(key, mouse):
  bottom_selector_panel_h = 9
  bottom_selector_panel = tcod.console_new(g.screen_width, bottom_selector_panel_h)
  tcod.console_set_alignment(bottom_selector_panel, tcod.CENTER)
  tcod.console_set_default_foreground(bottom_selector_panel, tcod.lightest_magenta)

  nearly_full_panel = tcod.console_new(g.screen_width, g.screen_height - bottom_selector_panel_h)
  tcod.console_set_alignment(nearly_full_panel, tcod.LEFT)
  tcod.console_set_default_foreground(nearly_full_panel, tcod.sea)

  print_season_overview(nearly_full_panel, g.screen_width, g.season)
  tcod.console_blit(nearly_full_panel, 0, 0, g.screen_width, g.screen_height - bottom_selector_panel_h, 0, 0, 0)

  confirm = False
  selected_option = 1
  while not confirm:
    tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

    spacing = 6

    options = []
    if g.season.current_race >= len(g.season.circuits):
      options = [
        ('exit', 'Retire!'),
        ('start over', 'Play again')
      ]
    else:
      options = [
        ('exit', 'I quit'),
        ('go forward', 'Let\'s rock')
      ]
    selection = options[0][0]
    
    tcod.console_clear(bottom_selector_panel)

    option0_text = options[0][1]
    option1_text = options[1][1]

    # Currently only supports exactly 2 options
    xy0 = (int(g.screen_width / 2) - len(option0_text) - int(spacing / 2), int(bottom_selector_panel_h / 2))
    xy1 = (int(g.screen_width / 2) + int(spacing / 2), int(bottom_selector_panel_h / 2))
    tcod.console_print_ex(bottom_selector_panel, xy0[0], xy0[1], tcod.BKGND_SET, tcod.LEFT, option0_text)
    tcod.console_print_ex(bottom_selector_panel, xy1[0], xy1[1], tcod.BKGND_SET, tcod.LEFT, option1_text)

    if selected_option == 0:
      tcod.console_hline(bottom_selector_panel, xy0[0] - 2, xy0[1] - 1, len(option0_text) + 4)
      tcod.console_hline(bottom_selector_panel, xy0[0] - 2, xy0[1] + 1, len(option0_text) + 4)

    elif selected_option == 1:
      tcod.console_hline(bottom_selector_panel, xy1[0] - 2, xy1[1] - 1, len(option1_text) + 4)
      tcod.console_hline(bottom_selector_panel, xy1[0] - 2, xy1[1] + 1, len(option1_text) + 4)

    action = handle_keys(key, 'simple selection')
    select = action.get('select')
    enter = action.get('enter')
    if select:
      selected_option += select
      if selected_option > len(options) - 1:
        selected_option = 0
      elif selected_option < 0:
        selected_option = len(options) - 1
    if enter:
      selection = options[selected_option][0]
      confirm = True
    
    tcod.console_blit(bottom_selector_panel, 0, 0, g.screen_width, bottom_selector_panel_h, 0, 0, g.screen_height - bottom_selector_panel_h)  
    tcod.console_flush()

  if selection == 'exit':
    g.context = Context.MAIN_MENU
    tcod.console_clear(bottom_selector_panel)
    tcod.console_clear(nearly_full_panel)
    tcod.console_blit(bottom_selector_panel, 0, 0, g.screen_width, bottom_selector_panel_h, 0, 0, g.screen_height - bottom_selector_panel_h)  
    tcod.console_blit(nearly_full_panel, 0, 0, g.screen_width, g.screen_height - bottom_selector_panel_h, 0, 0, 0)
    tcod.console_flush()
  elif selection == 'go forward':
    g.context = Context.RACE
    tcod.console_clear(bottom_selector_panel)
    tcod.console_clear(nearly_full_panel)
    tcod.console_blit(bottom_selector_panel, 0, 0, g.screen_width, bottom_selector_panel_h, 0, 0, g.screen_height - bottom_selector_panel_h)  
    tcod.console_blit(nearly_full_panel, 0, 0, g.screen_width, g.screen_height - bottom_selector_panel_h, 0, 0, 0)
    tcod.console_flush()
  elif selection == 'start over':
    g.context = Context.TEAM_CREATION
    tcod.console_clear(bottom_selector_panel)
    tcod.console_clear(nearly_full_panel)
    tcod.console_blit(bottom_selector_panel, 0, 0, g.screen_width, bottom_selector_panel_h, 0, 0, g.screen_height - bottom_selector_panel_h)  
    tcod.console_blit(nearly_full_panel, 0, 0, g.screen_width, g.screen_height - bottom_selector_panel_h, 0, 0, 0)
    tcod.console_flush()    


def do_team_creation(key, mouse):
  tcod.console_flush()
  full_panel = tcod.console_new(g.screen_width * 2, g.screen_height)
  tcod.console_set_alignment(full_panel, tcod.LEFT)
  tcod.console_set_default_foreground(full_panel, tcod.sea)

  questions_options = {
    'What is the name of your team?': [],
    'What color is your team?': [
      (tcod.red, '%c%c%c%cRed%c'%(tcod.COLCTRL_FORE_RGB, tcod.red.r + 256, tcod.red.g + 256, tcod.red.b + 256, tcod.COLCTRL_STOP)),
      (tcod.orange, '%c%c%c%cOrange%c'%(tcod.COLCTRL_FORE_RGB, tcod.orange.r + 256, tcod.orange.g + 256, tcod.orange.b + 256, tcod.COLCTRL_STOP)),
      (tcod.yellow, '%c%c%c%cYellow%c'%(tcod.COLCTRL_FORE_RGB, tcod.yellow.r + 256, tcod.yellow.g + 256, tcod.yellow.b + 256, tcod.COLCTRL_STOP)),
      (tcod.green, '%c%c%c%cGreen%c'%(tcod.COLCTRL_FORE_RGB, tcod.green.r + 256, tcod.green.g + 256, tcod.green.b + 256, tcod.COLCTRL_STOP)),
      (tcod.sea, '%c%c%c%cSea%c'%(tcod.COLCTRL_FORE_RGB, tcod.sea.r + 256, tcod.sea.g + 256, tcod.sea.b + 256, tcod.COLCTRL_STOP)),
      (tcod.turquoise, '%c%c%c%cTurquoise%c'%(tcod.COLCTRL_FORE_RGB, tcod.turquoise.r + 256, tcod.turquoise.g + 256, tcod.turquoise.b + 256, tcod.COLCTRL_STOP)),
      (tcod.light_cyan, '%c%c%c%cLight cyan%c'%(tcod.COLCTRL_FORE_RGB, tcod.light_cyan.r + 256, tcod.light_cyan.g + 256, tcod.light_cyan.b + 256, tcod.COLCTRL_STOP)),
      (tcod.azure, '%c%c%c%cAzure%c'%(tcod.COLCTRL_FORE_RGB, tcod.azure.r + 256, tcod.azure.g + 256, tcod.azure.b + 256, tcod.COLCTRL_STOP)),
      (tcod.blue, '%c%c%c%cBlue%c'%(tcod.COLCTRL_FORE_RGB, tcod.blue.r + 256, tcod.blue.g + 256, tcod.blue.b + 256, tcod.COLCTRL_STOP)),
      (tcod.purple, '%c%c%c%cPurple%c'%(tcod.COLCTRL_FORE_RGB, tcod.purple.r + 256, tcod.purple.g + 256, tcod.purple.b + 256, tcod.COLCTRL_STOP)),
      (tcod.light_purple, '%c%c%c%cLight purple%c'%(tcod.COLCTRL_FORE_RGB, tcod.light_purple.r + 256, tcod.light_purple.g + 256, tcod.light_purple.b + 256, tcod.COLCTRL_STOP)),
      (tcod.pink, '%c%c%c%cPink%c'%(tcod.COLCTRL_FORE_RGB, tcod.pink.r + 256, tcod.pink.g + 256, tcod.pink.b + 256, tcod.COLCTRL_STOP)),
      (tcod.sepia, '%c%c%c%cSepia%c'%(tcod.COLCTRL_FORE_RGB, tcod.sepia.r + 256, tcod.sepia.g + 256, tcod.sepia.b + 256, tcod.COLCTRL_STOP)),
      (tcod.gray, '%c%c%c%cGray%c'%(tcod.COLCTRL_FORE_RGB, tcod.gray.r + 256, tcod.gray.g + 256, tcod.gray.b + 256, tcod.COLCTRL_STOP)),
      (tcod.white, '%c%c%c%cWhite%c'%(tcod.COLCTRL_FORE_RGB, tcod.white.r + 256, tcod.white.g + 256, tcod.white.b + 256, tcod.COLCTRL_STOP))
    ]
  }

  responses = handle_questions(full_panel, key, mouse, questions_options)
  player_team = Team(responses[0], responses[1], Vehicle(vehicle_bodies.v_bod_1), True)
  teams = t.pick_season_teams(player_team)

  # Build competition
  p_color = player_team.color
  for ai in teams:
    if ai.color == p_color and not ai.isPlayer:
      # TODO: Make this better
      ai.set_color(tcod.peach)

  # Build season
  season_circuits = []
  for circuit in circuits.ALL:
    season_circuits.append(circuit)
  g.season = Season(2094, season_circuits, teams)

  # Move on
  g.context = Context.SEASON_OVERVIEW