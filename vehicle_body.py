class Vehicle_Body:
  COLLISION_EFFECT = '*'
  DAMAGE_EFFECT = 'x'

  def __init__(self, rows):
    self.rows = rows.copy()

    # Every car body should be uniform width all the way down.
    self.width = len(rows[0])
    self.length = len(rows)