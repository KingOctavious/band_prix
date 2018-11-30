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

 
FPS_CAP = 60
fullscreen = False
GAME_TITLE = 'Band Prix 2094'
font_path = 'terminal16x16_gs_ro.png'
layout = tcod.FONT_LAYOUT_ASCII_INROW

font_flags = tcod.FONT_TYPE_GREYSCALE | layout
TURN_BASED = False

tcod.console_set_custom_font(font_path, font_flags)
tcod.console_init_root(g.screen_width, g.screen_height, GAME_TITLE, fullscreen)
tcod.sys_set_fps(FPS_CAP)
key = tcod.Key()
mouse = tcod.Mouse()
exit_game = False
g.context = Context.MAIN_MENU


### GAME LOOP #################################################################

while not tcod.console_is_window_closed() and not exit_game:
  if g.context == Context.MAIN_MENU:
    do_main_menu(key, mouse)
  elif g.context == Context.RACE:
    do_race(key, mouse)
  elif g.context == Context.TEAM_CREATION: 
    do_team_creation(key, mouse)
  elif g.context == Context.SEASON_OVERVIEW:
    do_season_overview(key, mouse)
  elif g.context == Context.POST_RACE:
    do_post_race(key, mouse)
  elif g.context == Context.EXIT:
    exit_game = True
 
quit()
