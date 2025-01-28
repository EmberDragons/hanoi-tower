def check_pos(mouse_pos, pos, size):
    """Function that takes as parameters the position and size of a ring and the position of the mouse, and returns whether it was clicked"""
    result = False
    if pos[0] - size[0] < mouse_pos[0]:
        if pos[0] + size[0] > mouse_pos[0]:
            if pos[1] - size[1] < mouse_pos[1]:
                if pos[1] + size[1] > mouse_pos[1]:
                    result = True
    return result