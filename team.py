import random
from track_direction import Track_Direction as td

class Team:
  def __init__(self, name, color, vehicle, isPlayer=False):
    self.name = name
    self.color = color
    self.vehicle = vehicle
    self.isPlayer = isPlayer
    self.finished_current_race = False

    self.vehicle.color = color
    self.vehicle.is_player = isPlayer

    # For AI purposes. Holds 2-len lists in form of:
    # [CURVE_DIRECTION, NUM_OF_FRAMES_AGO_THIS_CURVE_WAS_ENCOUNTERED]
    self.curves_observed = []
    
    # For AI purposes. A queue of turns to take based on observed curves and
    # `ai_determine_direction`.
    self.turns_to_take = []


  def set_color(self, color):
    self.color = color
    self.vehicle.color = color


  # AI functions ##############################################################

  # ai_observe_curves
  #
  # Sees if there are any curves that need to be queued into 
  # `self.curves_observed` to handle soon.
  def ai_observe_curves(self, track_layout, rows_since_last_check):
    rows_since_last_check = int(rows_since_last_check)
    for track_row in range(int(self.vehicle.distance_traveled) - rows_since_last_check, int(self.vehicle.distance_traveled)):
      if track_row < len(track_layout):
        # if self.vehicle.distance_traveled >= 100:
        #   n = 1
        direction = track_layout[track_row]
        if direction != td.STRAIGHT:
          self.curves_observed.append([direction, 0])


  # ai_determine_direction
  #
  # Emulate reflexes by turning according to the `self.curves_observed` list
  # with increasing probability of executing the oldest observed curve.
  # Returns the direction to steer this frame.
  def ai_determine_direction(self):
    # % chance to turn immediately when curve is observed
    BASE_REFLEX = 88
    # Additional % point chance each frame to execute turns for observed curves
    REFLEX_INCREMENTER = 4
    # Remember `curves_observed` are direction:age tuples
    oldest_curve_age = 0
    curves_to_consider = [] # holds directions
    if len(self.curves_observed) > 0 and random.uniform(0, 99) < BASE_REFLEX + (self.curves_observed[0][1] * REFLEX_INCREMENTER):
      for curve in self.curves_observed:
        # We generally only care about the oldest curves
        if curve[1] == oldest_curve_age:
          curves_to_consider.append(curve[0])
        elif curve[1] > oldest_curve_age:
          curves_to_consider = [curve[0]]
          oldest_curve_age = curve[1]
        # Now that we've determine which curves we're going to act on, we
        # remove those from `self.curves_observed`.
        new_curves_observed = []
        for curve in self.curves_observed:
          curve_age = curve[1]
          if curve_age != oldest_curve_age:
            new_curves_observed.append(curve)
        self.curves_observed = new_curves_observed

      net_curvature = 0
      for curve in curves_to_consider:
        if curve == td.LEFT:
          net_curvature -= 1
        elif curve == td.RIGHT:
          net_curvature += 1

      # Queue up steering actions
      if net_curvature > 0:
        #print (net_curvature)
        for x in range(0, net_curvature):
          self.turns_to_take.append(td.RIGHT)
      elif net_curvature < 0:
        for x in range(0, abs(net_curvature)):
          self.turns_to_take.append(td.LEFT)


    # Return the direction that AI will steer this frame
    direction = td.STRAIGHT
    if len(self.turns_to_take) > 0:
      direction = self.turns_to_take[0]
      self.turns_to_take.pop(0)

    return direction

    
  # ai_run_counters
  #
  # Increments or decrements any counters that need to be adjusted on a per-
  # frame basis.
  def ai_run_counters(self):
    for curve_age in self.curves_observed:
      curve_age[1] += 1
    