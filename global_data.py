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
