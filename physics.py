import global_data as g
import visuals

def apply_collision(vehicle_body, collision_points):
  for veh_part in collision_points:
    veh_part_row = veh_part[1]
    current_body_row = vehicle_body.rows[veh_part_row]
    new_body_row = ''
    for index in range(0, len(current_body_row)):
      if index != veh_part[0]:
        new_body_row += current_body_row[index]
      else:
        new_body_row += visuals.COLLISION_EFFECT

    vehicle_body.rows[veh_part_row] = new_body_row


def handle_post_collision(vehicle):
  # Figure out which side of the car got hit
  collided_sides = {
    'front': 0,
    'left': 0,
    'right': 0,
    'rear': 0
  }

  # Count the colliding vehicle parts on each side to see where the collision
  # is coming from primarily. At the same time, we also rebuild the row strings
  # by replacing the collision effect with the damage effect.
  for row in range(0, len(vehicle.body.rows)):
    new_row_string = ''
    for col in range(0, len(vehicle.body.rows[row])):
      if vehicle.body.rows[row][col] == visuals.COLLISION_EFFECT:
        if col == 0:
          collided_sides['left'] += 1
        elif col == vehicle.body.width - 1:
          collided_sides['right'] += 1
        if row == 0:
          collided_sides['front'] += 1
        elif row == len(vehicle.body.rows) - 1:
          collided_sides['rear'] += 1

        new_row_string += visuals.DAMAGE_EFFECT
      
      else:
        new_row_string += vehicle.body.rows[row][col]

    vehicle.body.rows[row] = new_row_string

  # Now figure out which direction the car should bounce back
  # (based on which side(s) have the most)
  bounce_directions = [] # Because might go back/left, forward/right, etc.
  max_collided_count = 0
  for side, count in collided_sides.items():
    if count > 0:
      if len(bounce_directions) == 0:
        bounce_directions.append(g.SIDE_OPPOSITES[side])
        max_collided_count = count
      elif count == max_collided_count:
        bounce_directions.append(g.SIDE_OPPOSITES[side])
      elif count > max_collided_count:
        # Clear `bounce_directions` and add this one if it is dominant.
        bounce_directions = [g.SIDE_OPPOSITES[side]]
        max_collided_count = count

  # Bounceback happens here
  if 'front' in bounce_directions:
    vehicle.distance_traveled += 2
    if not vehicle.is_player:
      vehicle.y -= 2
  if 'rear' in bounce_directions:
    vehicle.distance_traveled -= 2
    if not vehicle.is_player:
      vehicle.y += 2
  if 'left' in bounce_directions:
    vehicle.x -= 1
  if 'right' in bounce_directions:
    vehicle.x += 1
      

def handle_collisions(race, colliding_vehicles_holder, barricade_locations_holder):
  # Compare every vehicle position to every other vehicle position
  team_count = (len(race.teams))
  for index in range(0, team_count):
    base_vehicle = race.teams[index].vehicle
    base_x = base_vehicle.x
    base_y = base_vehicle.y
    base_w = base_vehicle.body.width
    base_h = base_vehicle.body.length
    base_veh_collision_pts = [] # Holds (x, y) tuples

    if index < team_count - 1:
      # Check for collisions with barricades
      for y in range(base_y, base_y + base_h - 1):
        for x in range(base_x, base_x + base_w - 1):
          if (x, y) in barricade_locations_holder:
            # COLLISION DETECTED!
            base_veh_collision_pts.append((x - base_x, y - base_y))
            colliding_vehicles_holder.add(base_vehicle)
            apply_collision(base_vehicle.body, base_veh_collision_pts)
      # Done checking barricade collisions

      # We only have to check the opponents indexed higher than the currently
      # checked index, because as we move up in the base index being checked,
      # it has already been checked against those below it. So, we start
      # checking at `index + 1`.
      for opponent_index in range(index + 1, team_count):
        opp_vehicle = race.teams[opponent_index].vehicle
        opp_x = opp_vehicle.x
        opp_y = opp_vehicle.y
        opp_w = opp_vehicle.body.width
        opp_h = opp_vehicle.body.length

        # Quicker initial check to see if collision occurred
        if base_x < opp_x + opp_w and base_x + base_w > opp_x and base_y < opp_y + opp_h and base_y + base_h > opp_y:
          # COLLISION DETECTED! Now we need to figure out which specific parts of the vehicles collided.
          colliding_vehicles_holder.add(base_vehicle)
          colliding_vehicles_holder.add(opp_vehicle)
         
          # This will be a list of lists of tuples (real coordinates of collision locations)
          base_veh_grid = []
          for row in range(0, base_h):
            current_col_pts = []
            for col in range(0, base_w):
              current_col_pts.append((col + base_x, row + base_y))

            base_veh_grid.append(current_col_pts)


          # Now do mostly the same for opp, but instead of adding them to an
          # `opp_veh_grid` list, we check them on the fly. If any of the opp
          # vehicle's body part coordinate tuples match one of those in
          # `base_veh_grid`, then that's where a collision occured. In those
          # cases, we add the relative body coordinates to each vehicle's list
          # of collision locations
          opp_veh_collision_pts = []
          for row in range(0, opp_h):
            for col in range(0, opp_w):        
              opp_coords = (col + opp_x, row + opp_y)

              for base_row in range(0, len(base_veh_grid)):
                for base_col in range(0, len(base_veh_grid[base_row])):
                  if base_veh_grid[base_row][base_col] == opp_coords:
                    # This is where a collision occurred
                    opp_veh_collision_pts.append((col, row))
                    base_veh_collision_pts.append((base_col, base_row))

          # Once the actual collision locations are determined, we apply
          # the collision events to those parts of the vehicles.
          apply_collision(base_vehicle.body, base_veh_collision_pts)
          apply_collision(opp_vehicle.body, opp_veh_collision_pts)