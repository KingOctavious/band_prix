from track_direction import Track_Direction as td

import visuals

class Circuit:
  def __init__(self, name, track_layout):
    self.name = name
    # Simple list of Track_Direction per row
    self.track_layout = track_layout
    # List of tuples in form of (STRIPE_CHAR, track_offset)
    self.track_shape = []

    offset = 0
    for distance in range(0, len(track_layout)):
      if track_layout[distance] == td.LEFT:
        offset -= 1
      elif track_layout[distance] == td.RIGHT:
        offset += 1

      self.track_shape.append((visuals.STRIPE_CHARS[track_layout[distance]], offset))