import libtcodpy as tcod

def handle_keys(key):
  # Steer
  if key.vk == tcod.KEY_LEFT:
    return {'steer': -1}
  elif key.vk == tcod.KEY_RIGHT:
    return {'steer': 1}

  # Type characters
  elif key.vk == tcod.KEY_TEXT:
    return {'key_char': chr(key.text[0])}

  # elif key.vk == tcod.KEY_CHAR:
  #   #return {'key_char': chr(key.c)}




  # elif key.vk == tcod.KEY_0:
  #   return {'key_char': chr(key.c)}

  # elif key.vk == tcod.KEY_1:
  #   return {'key_char': chr(key.c)}

  # elif key.vk == tcod.KEY_2:
  #   return {'key_char': chr(key.c)}

  # elif key.vk == tcod.KEY_3:
  #   return {'key_char': chr(key.c)}

  # elif key.vk == tcod.KEY_4:
  #   return {'key_char': chr(key.c)}

  # elif key.vk == tcod.KEY_5:
  #   return {'key_char': chr(key.c)}

  # elif key.vk == tcod.KEY_6:
  #   return {'key_char': chr(key.c)}

  # elif key.vk == tcod.KEY_7:
  #   return {'key_char': chr(key.c)}

  # elif key.vk == tcod.KEY_8:
  #   return {'key_char': chr(key.c)}

  # elif key.vk == tcod.KEY_9:
  #   return {'key_char': chr(key.c)}

  # elif key.vk == tcod.KEY_SPACE:
  #   return {'key_char': chr(key.c)}

  # Backspace
  elif key.vk == tcod.KEY_BACKSPACE:
    return {'backspace': True}

  # Exit game
  elif key.vk == tcod.KEY_ESCAPE:
    return {'exit': True}

  else:
    return {}