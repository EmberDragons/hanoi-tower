from lists import *

def recursion(ring_list, movements=Queue(), previous_pos=1, depth=1, coming=False):
    """Recursive function that creates the list of movements
    Simple concept:
        1. Recursion until depth = 1 (the first) + send our position + coming = False (going to the other place)
        2. Move our ring
        3. Second recursion until 1 + send our position + coming=True (coming back)"""
    
    # Movement
    next_bar = select_pos(ring_list[depth-1], previous_pos)
    if coming == True:  # If we need to move to the same position as the previous ring
        next_bar = previous_pos

    if depth == 1:  # No more recursion
        movements.add((depth, next_bar))
        ring_list[depth-1] = next_bar
        return movements
    else:
        # 1. Recursion
        movements = recursion(ring_list, movements, next_bar, depth-1)
        # 2. Move the ring
        movements.add((depth, next_bar))
        ring_list[depth-1] = next_bar
        # 3. Recursion with coming=True
        return recursion(ring_list, movements, next_bar, depth-1, True)

def select_pos(pos1, pos2):
    """Function that selects the bar to go to if the other two bars are occupied"""
    our_pos = 1
    if pos1 == 1:
        if pos2 == 2:
            our_pos = 3
        if pos2 == 3:
            our_pos = 2
    if pos1 == 2:
        if pos2 == 1:
            our_pos = 3
        if pos2 == 3:
            our_pos = 1
    if pos1 == 3:
        if pos2 == 1:
            our_pos = 2
        if pos2 == 2:
            our_pos = 1
    return our_pos