from track_direction import Track_Direction as td

BARRICADE = '8'
COLLISION_EFFECT = '*'
DAMAGE_EFFECT = 'x'
DAMAGED_TIRE = '0'
FINISH_LINE = '#'
START_LINE = '-'
STRIPE_CHARS = {
  td.STRAIGHT: '|',
  td.LEFT: '\\',
  td.RIGHT: '/'
}