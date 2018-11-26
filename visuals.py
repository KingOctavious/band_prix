from track_direction import Track_Direction as td

BARRICADE = '0'
COLLISION_EFFECT = '*'
DAMAGE_EFFECT = 'x'
FINISH_LINE = '#'
START_LINE = '-'
STRIPE_CHARS = {
  td.STRAIGHT: '|',
  td.LEFT: '\\',
  td.RIGHT: '/'
}