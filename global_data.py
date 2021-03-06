import collections
from context import Context

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
context = None
lexicon_counter = 0
MAIN_VIEWPORT_WIDTH = 80
screen_height = 50
screen_width = 100
season = None
POINTS = {
  1: 25,
  2: 18,
  3: 13,
  4: 10,
  5: 0
}
TITLE_GRAPHIC_TOP = [
  ['#######        ##      #       #  ######          #######   #######    #  #       #'],
  ['#      #      #  #     ##      #  #     #         #      #  #      #   #   #     # '],
  ['#      #      #  #     # #     #  #      #        #      #  #      #   #    #   #  '],
  ['#      #     #    #    #  #    #  #      #        #      #  #      #   #     # #   '],
  ['#########    ######    #   #   #  #      #        #######   #######    #      #    '],
  ['#       #   #      #   #    #  #  #      #        #         #      #   #     # #   '],
  ['#       #   #      #   #     # #  #      #        #         #       #  #    #   #  '], 
  ['#       #  #        #  #      ##  #     #         #         #       #  #   #     # '],
  ['#########  #        #  #       #  ######          #         #       #  #  #       #'],
]
TITLE_GRAPHIC_BOTTOM = [
  [' ######    ######    ######   #      #'],
  ['#      #  #      #  #      #  #      #'],
  ['#      #  #      #  #      #  #      #'],
  ['      #   #      #  #      #  #      #'],
  ['     #    #      #   #######  ########'],
  ['    #     #      #         #         #'],
  ['   #      #      #         #         #'],
  [' ##       #      #         #         #'],
  ['########   ######          #         #'],
]
TRACK_ROWS_TO_DISPLAY = 50
TRACK_ROWS_DISPLAYED_ABOVE_PLAYER = round(TRACK_ROWS_TO_DISPLAY / 2)
TRACK_ROWS_DISPLAYED_DOWN_FROM_PLAYER_TOP = TRACK_ROWS_TO_DISPLAY - TRACK_ROWS_DISPLAYED_ABOVE_PLAYER

SIDE_OPPOSITES = {
  'front': 'rear',
  'right': 'left',
  'rear': 'front',
  'left': 'right'
}

# KEYSPEED_POWERPCT
# The percentage of the vehicle's power that is applied when keyspeed
# registers at or below the given key. This power applies to both the
# accleration and the highest possible speed.
KEYSPEED_POWERPCT = collections.OrderedDict({
  0.09: 1.00,
  0.15: 0.66,
  0.22: 0.33
})

def get_powerpct_from_keyspeed(keyspeed):
  determined_powerpct = 0
  for time, pwr in KEYSPEED_POWERPCT.items():
    if keyspeed <= time:
      determined_powerpct = pwr
      break
  return determined_powerpct


