import collections

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
screen_height = 57
screen_width = 110
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


