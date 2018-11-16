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
from season import Season
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


# handle_questions
#
# Takes a dict of questions:options, prints them to the screen, and returns
# the responses in list form. Options should be provided as lists of
# value:string tuples. If the question requires a text-input response,
# provide an empty list argument for the options.
def handle_questions(con, questions_options):
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
        tcod.console_print_rect_ex(con, 0, len(static_text_to_print), screen_width, screen_height, tcod.BKGND_SET, tcod.LEFT, response_line)
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
          tcod.console_print_rect_ex(con, 0, len(static_text_to_print) + x, screen_width, screen_height, tcod.BKGND_SET, tcod.LEFT, option_text)

      # Once we get a response, do this stuff:
      if confirmed:
        if len(options) > 0:
          # Clear to remove list of options
          tcod.console_clear(con)
        static_text_to_print.append(response_line)
        responses.append(response)

      # Do this stuff every time no matter what
      for x in range(0, len(static_text_to_print)):
        tcod.console_print_rect_ex(con, 0, x, screen_width, screen_height, tcod.BKGND_SET, tcod.LEFT, static_text_to_print[x])
      tcod.console_blit(con, 0, 0, screen_height, screen_height, 0, 0, 0)
      tcod.console_flush()


  sleep(0.2)
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
    

  # End function definitions ##################################################

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
tcod.console_set_default_foreground(full_panel, tcod.sea)

bottom_selector_panel_h = 9
bottom_selector_panel = tcod.console_new(screen_width, bottom_selector_panel_h)
tcod.console_set_alignment(bottom_selector_panel, tcod.CENTER)
tcod.console_set_default_foreground(bottom_selector_panel, tcod.lightest_magenta)

nearly_full_panel = tcod.console_new(screen_width, screen_height - bottom_selector_panel_h)
tcod.console_set_alignment(nearly_full_panel, tcod.LEFT)
tcod.console_set_default_foreground(nearly_full_panel, tcod.sea)
# End viewports ###############################################################


tcod.sys_set_fps(FPS_CAP)

key = tcod.Key()
mouse = tcod.Mouse()
exit_game = False

### GAME LOOP #################################################################

#context = Context.RACE
context = Context.TEAM_CREATION

while not tcod.console_is_window_closed() and not exit_game:

  if context == Context.RACE:
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


      for team in race.teams:
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
        #(tcod.blue, '%c%c%c%cBlue%c'%(tcod.COLCTRL_FORE_RGB, tcod.blue.r + 256, tcod.blue.g + 256, tcod.blue.b + 256, tcod.COLCTRL_STOP)),
        (tcod.purple, '%c%c%c%cPurple%c'%(tcod.COLCTRL_FORE_RGB, tcod.purple.r + 256, tcod.purple.g + 256, tcod.purple.b + 256, tcod.COLCTRL_STOP)),
        (tcod.light_purple, '%c%c%c%cLight purple%c'%(tcod.COLCTRL_FORE_RGB, tcod.light_purple.r + 256, tcod.light_purple.g + 256, tcod.light_purple.b + 256, tcod.COLCTRL_STOP)),
        (tcod.pink, '%c%c%c%cPink%c'%(tcod.COLCTRL_FORE_RGB, tcod.pink.r + 256, tcod.pink.g + 256, tcod.pink.b + 256, tcod.COLCTRL_STOP)),
        (tcod.sepia, '%c%c%c%cSepia%c'%(tcod.COLCTRL_FORE_RGB, tcod.sepia.r + 256, tcod.sepia.g + 256, tcod.sepia.b + 256, tcod.COLCTRL_STOP)),
        (tcod.gray, '%c%c%c%cGray%c'%(tcod.COLCTRL_FORE_RGB, tcod.gray.r + 256, tcod.gray.g + 256, tcod.gray.b + 256, tcod.COLCTRL_STOP)),
        (tcod.white, '%c%c%c%cWhite%c'%(tcod.COLCTRL_FORE_RGB, tcod.white.r + 256, tcod.white.g + 256, tcod.white.b + 256, tcod.COLCTRL_STOP))
      ]
    }

    responses = handle_questions(full_panel, questions_options)
    player_team = Team(responses[0], responses[1], Vehicle(vehicle_bodies.v_bod_1), True)
    teams = [
      Team('Kasvot Vaxt', tcod.azure, Vehicle(vehicle_bodies.v_bod_1)),
      Team('ViscDuds', tcod.azure, Vehicle(vehicle_bodies.v_bod_1)),
      player_team,
      Team('The Billiards', tcod.green, Vehicle(vehicle_bodies.v_bod_1)),
      Team('Strange Dan Gustafvist', tcod.yellow, Vehicle(vehicle_bodies.v_bod_1)),
    ]

    # Build competition
    p_color = player_team.color
    for ai in teams:
      if ai.color == p_color:
        # TODO: Make this better
        ai.set_color(tcod.peach)

    # Build season
    season_circuits = []
    for circuit in circuits.ALL:
      season_circuits.append(circuit)
    season = Season(2094, season_circuits, teams)

    # Move on
    context = Context.SEASON_OVERVIEW
    
  elif context == Context.SEASON_OVERVIEW:
    confirm = False
    selected_option = 1
    while not confirm:
      tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
      tcod.console_clear(full_panel)
      season_title_text = str(season.year)
      print_season_overview(full_panel, screen_width, season)

      tcod.console_clear(nearly_full_panel)
      print_season_overview(nearly_full_panel, screen_width, season)
      tcod.console_blit(nearly_full_panel, 0, 0, screen_width, screen_height - bottom_selector_panel_h, 0, 0, 0)

      spacing = 6
      options = [
        ('exit', 'Let\'s go home'),
        ('go forward', 'Let\'s rock')
      ]
      selection = options[0][0]
      
      tcod.console_clear(bottom_selector_panel)

      option0_text = options[0][1]
      option1_text = options[1][1]

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


      if len(options) == 2:        
        xy0 = (int(screen_width / 2) - len(option0_text) - int(spacing / 2), int(bottom_selector_panel_h / 2))
        xy1 = (int(screen_width / 2) + int(spacing / 2), int(bottom_selector_panel_h / 2))
        tcod.console_print_ex(bottom_selector_panel, xy0[0], xy0[1], tcod.BKGND_SET, tcod.LEFT, option0_text)
        tcod.console_print_ex(bottom_selector_panel, xy1[0], xy1[1], tcod.BKGND_SET, tcod.LEFT, option1_text)

        if selected_option == 0:
          tcod.console_hline(bottom_selector_panel, xy0[0] - 2, xy0[1] - 1, len(option0_text) + 4)
          tcod.console_hline(bottom_selector_panel, xy0[0] - 2, xy0[1] + 1, len(option0_text) + 4)

        elif selected_option == 1:
          tcod.console_hline(bottom_selector_panel, xy1[0] - 2, xy1[1] - 1, len(option1_text) + 4)
          tcod.console_hline(bottom_selector_panel, xy1[0] - 2, xy1[1] + 1, len(option1_text) + 4)
        

      tcod.console_blit(bottom_selector_panel, 0, 0, screen_width, bottom_selector_panel_h, 0, 0, screen_height - bottom_selector_panel_h)

      tcod.console_flush()

    if selection == 'exit':
      pass
    if selection == 'go forward':
      # Generate all the race info

      # Figure out which team index is the player's team; also reset certain vehicle data
      player_team_index = 0
      lexicon = lex.country
      title_and_song = build_song(lexicon)
      race = Race(teams, season.circuits[season.next_race], title_and_song[1], title_and_song[0])
      for x in range(0, len(race.teams)):
        race.teams[x].vehicle.distance_traveled = 0
        race.teams[x].vehicle.speed = 0
        race.teams[x].finished_current_race = False
        if (race.teams[x].isPlayer):
          player_team_index = x

      # Move on
      context = Context.RACE





  #sleep(0.1)
 
quit()