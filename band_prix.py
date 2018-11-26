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

tcod.console_set_custom_font(font_path, font_flags)
tcod.console_init_root(g.screen_width, g.screen_height, GAME_TITLE, fullscreen)
tcod.sys_set_fps(FPS_CAP)
key = tcod.Key()
mouse = tcod.Mouse()
exit_game = False


### GAME LOOP #################################################################

while not tcod.console_is_window_closed() and not exit_game:
  if g.context == Context.RACE:
    do_race(key, mouse)
  elif g.context == Context.TEAM_CREATION: 
    do_team_creation(key, mouse)
  elif g.context == Context.SEASON_OVERVIEW:
    do_season_overview(key, mouse)
  elif g.context == Context.POST_RACE:
    do_post_race(key, mouse)





  #sleep(0.1)
 
quit()