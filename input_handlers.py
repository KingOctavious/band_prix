import libtcodpy as tcod

def handle_keys(key, input_type=None):
  if input_type == None:

    # Steer
    if key.vk == tcod.KEY_LEFT:
      return {'steer': -1}
    elif key.vk == tcod.KEY_RIGHT:
      return {'steer': 1}

    # Type characters
    elif key.vk == tcod.KEY_TEXT:
      return {'key_char': chr(key.text[0])}

    # Other stuff
    elif key.vk == tcod.KEY_BACKSPACE:
      return {'backspace': True}
    elif key.vk == tcod.KEY_ENTER or key.vk == tcod.KEY_KPENTER:
      return {'confirm': True}

    # Exit game
    elif key.vk == tcod.KEY_ESCAPE:
      return {'exit': True}

    else:
      return {}


  elif input_type == 'simple selection':
    if key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_DOWN:
      return {'select': -1}
    elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_UP:
      return {'select': 1}
    elif key.vk == tcod.KEY_ENTER or key.vk == tcod.KEY_KPENTER:
      return {'enter': True}
    else:
      return {'select': 0}