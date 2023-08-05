def handle_keys(key):
    key_char = key

    if key_char == ord('k'):
        return {'move' : (0, -1)}
    elif key_char == ord('j'):
        return {'move' : (0, 1)}
    elif key_char == ord('h'):
        return {'move' : (-1, 0)}
    elif key_char == ord('l'):
        return {'move' : (1, 0)}
    elif key_char == ord('y'):
        return {'move': (-1, -1)}
    elif key_char == ord('u'):
        return {'move': (1, -1)}
    elif key_char == ord('b'):
        return {'move': (-1, 1)}
    elif key_char == ord('n'):
        return {'move': (1, 1)}

    if key == 27:
        return {'exit' : True}

    return {}
