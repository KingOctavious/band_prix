import libtcodpy as tcod

def handle_keys(key):
  # Steer
  if key.vk == tcod.KEY_LEFT:
    return {'steer': -1}
  elif key.vk == tcod.KEY_RIGHT:
    return {'steer': 1}

  # Exit game
  elif key.vk == tcod.KEY_ESCAPE:
    return {'exit': True}

  else:
    return {}