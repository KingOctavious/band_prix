class Vehicle_Body:
  def __init__(self, rows):
    self.rows = rows

    # Every car body should be uniform width all the way down.
    self.width = len(rows[0])
    self.length = len(rows)