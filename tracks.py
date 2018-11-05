from track_direction import Track_Direction as td

track1 = []

for x in range(0, 100):
  track1.append(td.STRAIGHT)

track1.append(td.RIGHT)

for x in range(0, 50):
  track1.append(td.STRAIGHT)

track1.append(td.RIGHT)
track1.append(td.RIGHT)

for x in range(0, 50):
  track1.append(td.STRAIGHT)