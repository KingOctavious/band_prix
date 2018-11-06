from track_direction import Track_Direction as td


track_layout_1 = []

for x in range(0, 100):
  track_layout_1.append(td.STRAIGHT)

track_layout_1.append(td.RIGHT)

for x in range(0, 50):
  track_layout_1.append(td.STRAIGHT)

track_layout_1.append(td.RIGHT)
track_layout_1.append(td.RIGHT)

for x in range(0, 50):
  track_layout_1.append(td.STRAIGHT)

