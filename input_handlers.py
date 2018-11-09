import libtcodpy as tcod

def handle_keys(key):
  # Steer
  if key.vk == tcod.KEY_LEFT:
    return {'steer': -1}
  elif key.vk == tcod.KEY_RIGHT:
    return {'steer': 1}

  # Type lyrics
  elif key.vk == tcod.KEY_CHAR: 
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_0:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_1:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_2:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_3:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_4:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_5:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_6:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_7:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_8:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_9:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  elif key.vk == tcod.KEY_SPACE:
    print(chr(key.c))
    return {'key_char': chr(key.c)}

  # Exit game
  elif key.vk == tcod.KEY_ESCAPE:
    return {'exit': True}

  else:
    return {}