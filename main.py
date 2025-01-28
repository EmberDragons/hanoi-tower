import tkinter as tk
from lists import *
from move_set import *
from check_pos import *
#--------------------------------------------------------------CLASSES----------------------------------------------------------------------------

class Bar:
    def __init__(self, nb):
        """Constructor for the class that represents a bar"""
        self.number = nb
        self.list = Stack()
        self.pos = [0, 0]
        self.create_bars()

    def create_bars(self):
        """Function that handles the visual creation of the bars"""
        bar_color = "black"
        # x position
        start_x = width // 6
        one_third_window = width // 3
        thickness = 10
        self.pos[0] = start_x + (self.number - 1) * one_third_window + thickness // 2
        # y position
        start_y = 50
        bar_height = 300
        self.pos[1] = start_y + bar_height
        # creating rectangles
        canvas.create_rectangle(start_x + (self.number - 1) * one_third_window - thickness // 2, start_y,
                                 start_x + (self.number - 1) * one_third_window + thickness // 2,
                                 start_y + bar_height, fill=bar_color)


class Ring:
    def __init__(self, nb):
        """Constructor for the class that represents a ring"""
        self.number = nb
        self.bar_id = 0

        self.body = None
        self.pos = [0, 0]
        self.origin_pos = [0, 0]
        self.size = [0, 0]
        self.create_ring()

        self.moves = False
        self.func = None
        # add the ring to the initial pile:
        bar_list[self.bar_id].list.add(self)

    def create_ring(self):
        """Function that visually creates a ring"""
        base_bar = 220 + (6 - num_rings) * 20
        color_list = ["red", "blue", "green", "purple", "yellow", "brown"]

        ring_color = color_list[self.number - 1]
        # x position and size
        self.pos[0] = width // 6
        self.size[0] = self.number * 10
        # y position and size
        self.pos[1] = base_bar + self.number * 20
        self.size[1] = 10
        self.origin_pos = self.pos
        self.body = canvas.create_rectangle(self.pos[0] - self.size[0], self.pos[1] - self.size[1],
                                            self.pos[0] + self.size[0], self.pos[1] + self.size[1], fill=ring_color)

    def move_ring(self, direction, arrive, bar_id):
        """Function to move the ring along the bar"""
        if bar_id != self.bar_id:  # check if it has already been added to the list
            bar_list[self.bar_id].list.remove()  # always the top one
            self.bar_id = bar_id
            bar_list[self.bar_id].list.add(self)

        # new direction
        x = direction[0]
        y = direction[1]
        self.pos = [self.pos[0] + x, self.pos[1] + y]
        canvas.move(self.body, x, y)
        self.func = canvas.after(17, self.move_ring, direction, arrive, self.bar_id)
        # arrived
        if abs(arrive[0] - self.pos[0]) < 2 and abs(arrive[1] - self.pos[1]) < 1:
            canvas.after_cancel(self.func)
            self.moves = False

    def move_up_ring(self, direction, arrive, bar_id, arrive_next_y):
        """Function that moves the ring up the bar"""
        self.moves = True

        # change pile according to the bars
        if bar_id != self.bar_id:  # check if it has already been added to the list
            bar_list[self.bar_id].list.remove()  # always the top one
            self.bar_id = bar_id
            bar_list[self.bar_id].list.add(self)

        x = direction[0]
        y = direction[1]

        self.pos = [self.pos[0] + x, self.pos[1] + y]
        canvas.move(self.body, x, y)
        self.func = canvas.after(17, self.move_up_ring, direction, arrive, self.bar_id, arrive_next_y)

        # destination reached
        if abs(arrive[0] - self.pos[0]) < 1 and abs(arrive[1] - self.pos[1]) < 1:
            canvas.after_cancel(self.func)
            arrive_next = [arrive[0], arrive_next_y]

            # direction
            n_x = (arrive_next[0] - self.pos[0]) / 50
            n_y = (arrive_next[1] - self.pos[1]) / 50
            dir_next = [n_x, n_y]
            # second part of the journey
            self.move_ring(dir_next, arrive_next, bar_id)

    def reset_pos(self):
        """Function to reset the position and variables of the rings"""
        self.moves = False
        self.pos = self.origin_pos
        canvas.coords(self.body, self.pos[0] - self.size[0], self.pos[1] - self.size[1],
                      self.pos[0] + self.size[0], self.pos[1] + self.size[1])
        bar_list[self.bar_id].list.remove()  # always the top one
        self.bar_id = 0
        self.reset_move()
        bar_list[self.bar_id].list.add(self)

    def reset_move(self):
        """Function to reset all movements"""
        if self.func is not None:
            canvas.after_cancel(self.func)
            self.func = None


#-------------------------------------------------------------FUNCTIONS---------------------------------------------------------------------------

# main code :
def reset():
    """Function that resets the code to prepare for restarting movements"""
    global movements
    movements = initial_movements.copy()
    for ring in ring_list:
        ring.reset_pos()

def update():
    """Function that is called to update the position of the blocks"""
    ring, bar = movements.first.value
    if movements.size() >= 1 and ring_list[movements.check() - 1].moves == False:
        ring, bar = movements.remove()
        # retrieve the correct ids
        ring -= 1
        bar -= 1

        # determine the destination
        pos = bar_list[bar].pos
        x_arrive = pos[0] - 5
        y_arrive = pos[1] - bar_list[bar].list.size() * 20 - 10

        # direction
        x = (x_arrive - ring_list[ring].pos[0]) / 50
        y = (top_bar - ring_list[ring].pos[1]) / 50
        ring_list[ring].move_up_ring((x, y), (x_arrive, top_bar), bar, y_arrive)

def visual_base():
    """Function to create a base at the bottom of the window"""
    # at the bottom of the window
    bar_color = "black"
    start_x = width // 6
    thickness = 10
    start_y = 50
    canvas.create_rectangle(start_x // 2, height - start_y, width - start_x // 2, height - start_y + thickness, fill=bar_color)

# moving rings :
def select_ring():
    """Function that selects the ring based on the cursor"""
    global selected_ring
    already_selected = False
    for ring in ring_list:
        pos = ring.pos
        size = ring.size
        # check if the position of the ring matches the cursor's
        if check_pos(mouse_pos, pos, size):
            if selected_ring is not None:
                unselect_anim(selected_ring)

            already_selected = True
            selected_ring = ring
            select_anim(selected_ring)
        # otherwise, deselect the ring
        elif not already_selected:
            if selected_ring is not None:
                unselect_anim(selected_ring)
            selected_ring = None

def move_ring():
    global selected_ring
    one_third_window = width // 3
    bar = (mouse_pos[0] // one_third_window)
    can_move = False

    # can only move the ring if it's the top one in the pile, the bar it is going to is not the same as where it is,
    # it isn't already moving, and the ring on the next bar is larger than it
    print(bar_list[bar].list)
    if ring_list[movements.check() - 1].moves == False and bar != selected_ring.bar_id and \
            bar_list[selected_ring.bar_id].list.first.value.number == selected_ring.number:
        if bar_list[bar].list.first is not None:
            if bar_list[bar].list.first.value.number > selected_ring.number:
                can_move = True
        else:
            can_move = True

        if can_move:
            # determine destination
            pos = bar_list[bar].pos
            x_arrive = pos[0] - 5
            y_arrive = pos[1] - bar_list[bar].list.size() * 20 - 10

            # direction
            x = (x_arrive - selected_ring.pos[0]) / 50
            y = (top_bar - selected_ring.pos[1]) / 50
            selected_ring.reset_move()
            selected_ring.move_up_ring((x, y), (x_arrive, top_bar), bar, y_arrive)
    unselect_anim(selected_ring)
    selected_ring = None


def select_anim(ring):
    """Animation that enlarges the border of the ring"""
    canvas.itemconfig(ring.body, width=5)

def unselect_anim(ring):
    """Animation that shrinks the border of the ring"""
    canvas.itemconfig(ring.body, width=1)

# key press handlers :
def motion(event):
    """Function that gets the position of the mouse every time it moves"""
    global mouse_pos
    mouse_pos = (event.x, event.y)

def left_click(event):
    """Function that activates when a click happens"""
    global selected_ring

    if selected_ring is None:  # click on a ring
        select_ring()
    else:  # click on the bar
        move_ring()

#---------------------------------------------------------------MAIN------------------------------------------------------------------------------

num_rings = 4

# global variables
width = 600
height = 400

window = tk.Tk()
canvas = tk.Canvas(window, width=width, height=height, bg="white")
canvas.pack()

# manual movements
mouse_pos = (0, 0)
selected_ring = None
top_bar = 40  # corresponds to the height of the bars

# storage for rings on bars
bar_list = [Bar(1), Bar(2), Bar(3)]  # list of all bars

# storage for rings
ring_ids = [1 for i in range(num_rings)]
ring_list = [Ring(i) for i in range(num_rings, 0, -1)]  # add them in the correct order
ring_list.reverse()

# storage for movements
initial_movements = recursion(ring_ids, Queue(), 3, num_rings, True)
movements = initial_movements.copy()
print(movements)

# create other visuals
visual_base()

# buttons
next_button = tk.Button(window, cursor="arrow", width=20, height=1, text="NEXT", command=update)
next_button.pack()
reset_button = tk.Button(window, cursor="arrow", width=20, height=1, text="RESET", command=reset)
reset_button.pack()
quit_button = tk.Button(window, cursor="arrow", width=20, height=1, text="QUIT", command=window.destroy)
quit_button.pack()
window.bind('<Motion>', motion)
window.bind('<Button-1>', left_click)
window.mainloop()