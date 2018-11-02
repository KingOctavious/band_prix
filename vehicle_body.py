class Vehicle_Body:
  def __init__(self, rows):
    self.rows = rows
    self.width = len(rows[0])

    # Every car body should be uniform width all the way down, with the 
    # possible exception of the very front, so we check `rows[1]` for what
    # should be a reliable determination of width.
    if len(rows) > 1:
      self.width = len(rows[1])
    self.length = len(rows)

  def printBody(self):
    for row in range(0, len(self.rows)):
      print(self.rows[row])