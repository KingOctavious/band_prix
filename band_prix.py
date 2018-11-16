import libtcodpy as tcod

import circuits
from context import Context
from context_handlers import *
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
      tcod.console_blit(con, 0, 0, g.screen_height, g.screen_height, 0, 0, 0)
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





# Viewports ###################################################################
tcod.console_set_custom_font(font_path, font_flags)
tcod.console_init_root(g.screen_width, g.screen_height, GAME_TITLE, fullscreen)

full_panel = tcod.console_new(g.screen_width, g.screen_height)
tcod.console_set_alignment(full_panel, tcod.LEFT)
tcod.console_set_default_foreground(full_panel, tcod.sea)

bottom_selector_panel_h = 9
bottom_selector_panel = tcod.console_new(g.screen_width, bottom_selector_panel_h)
tcod.console_set_alignment(bottom_selector_panel, tcod.CENTER)
tcod.console_set_default_foreground(bottom_selector_panel, tcod.lightest_magenta)

nearly_full_panel = tcod.console_new(g.screen_width, g.screen_height - bottom_selector_panel_h)
tcod.console_set_alignment(nearly_full_panel, tcod.LEFT)
tcod.console_set_default_foreground(nearly_full_panel, tcod.sea)
# End viewports ###############################################################


tcod.sys_set_fps(FPS_CAP)

key = tcod.Key()
mouse = tcod.Mouse()
exit_game = False
season = None
race = None

### GAME LOOP #################################################################

#context = Context.RACE
context = Context.TEAM_CREATION

while not tcod.console_is_window_closed() and not exit_game:

  if context == Context.RACE:


    do_race(race, key, mouse)

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
      print_season_overview(full_panel, g.screen_width, season)

      tcod.console_clear(nearly_full_panel)
      print_season_overview(nearly_full_panel, g.screen_width, season)
      tcod.console_blit(nearly_full_panel, 0, 0, g.screen_width, g.screen_height - bottom_selector_panel_h, 0, 0, 0)

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
        

      tcod.console_blit(bottom_selector_panel, 0, 0, g.screen_width, bottom_selector_panel_h, 0, 0, g.screen_height - bottom_selector_panel_h)

      tcod.console_flush()

    if selection == 'exit':
      pass
    if selection == 'go forward':
      # Generate all the race info

      lexicon = lex.country
      title_and_song = build_song(lexicon)
      race = Race(season.teams, season.circuits[season.next_race], title_and_song[1], title_and_song[0])
      for x in range(0, len(race.teams)):
        race.teams[x].vehicle.distance_traveled = 0
        race.teams[x].vehicle.speed = 0
        race.teams[x].finished_current_race = False


      # Move on
      context = Context.RACE





  #sleep(0.1)
 
quit()