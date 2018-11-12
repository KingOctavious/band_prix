import collections

SIDE_OPPOSITES = {
  'front': 'rear',
  'right': 'left',
  'rear': 'front',
  'left': 'right'
}

KEYSPEED_ACCEL = collections.OrderedDict({
  0.09: 3,
  0.18: 2,
  0.22: 0,
  0.25: -1,
  0.35: -2,
  0.5: -3
})

def get_accel_from_keyspeed(keyspeed):
  determined_accel = -4
  for time, accel in KEYSPEED_ACCEL.items():
    print(time)
    if keyspeed <= time:
      determined_accel = accel
      break
  return determined_accel

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


