from track_direction import Track_Direction as td

class Circuit:
  STRIPE_CHARS = {
    td.STRAIGHT: '|',
    td.LEFT: '\\',
    td.RIGHT: '/'
  }

  FINISH_LINE = '#'
  START_LINE = '-'

  def __init__(self, name, track_layout):
    self.name = name

    # track_shape stores tuples in form of (STRIPE_CHAR, track_offset)
    self.track_shape = []

    offset = 0
    for distance in range(0, len(track_layout)):
      if track_layout[distance] == td.LEFT:
        offset -= 1
      elif track_layout[distance] == td.RIGHT:
        offset += 1

      self.track_shape.append((self.STRIPE_CHARS[track_layout[distance]], offset))