import copy, curses
import collection, waveform


class Curse:
    def __init__(self):
        # --- Setup ---
        self.setup_curse()

        # --- Internal ---
        # index of [] is the root
        self.index = []
        self.container = collection.Collection("■", [collection.Collection()])
        return

    # ==== Setup and Graphics ====
    def setup_curse(self):
        # Initialize windoow
        self.stdscr = curses.initscr()
        # Setup color
        curses.start_color()
        # Don't just type inputs
        curses.noecho()
        # Inputs without pressing enter
        curses.cbreak()
        # Enable keypad mode
        self.stdscr.keypad(True)
        # Turn off blinking cursor
        # !!! WHEN DOING TEXT ENTRY RETURN THIS PROBABLY !!!
        curses.curs_set(False)
        return

    def kill(self):
        """
        This ideally attempts to return the terminal to a useable state when the program finishes.
        We are using a wrapper so this is handled curses for us. During development the program 
        ends through a crash a large portion of the time so this wouldn't be called anyway leading
        to an unuseable terminal even though we made this.

        It is being left in more for personal documentation for curses than usability.
        """
        # Turn enter back on for inputs
        curses.nocbreak()
        # Disable keypad
        self.stdscr.keypad(False)
        # Return echo
        curses.echo()
        # Go back to normal?
        curses.endwin()
        return

    def write_row(self, y, depth, indexes, text=None):
        # Don't crash
        if y >= curses.LINES:
            return y
        
        # If text is None, just write an empty row
        x = 1
        for i, d in enumerate(depth):
            # Depth of value
            if i == len(depth)-1 and text is not None:
                self.stdscr.addstr(y, x, "├" if d else "└")
            # Bars underneath
            else:
                self.stdscr.addstr(y, x, "|" if d else "")
            # Step size between depths (leaves room for arrow at least)
            x += 2
        # Ignore writing things for a spacer
        if text is not None:
            # If selected
            if self.index == indexes:
                self.stdscr.addch(y, x-1, curses.ACS_RARROW, curses.A_BOLD)
            self.stdscr.addstr(y, x, text)
        y += 1
        return y

    def draw(self, node=None, depth=[], y=0, indexes=[]):
        # Don't crash
        if y >= curses.LINES:
            return y

        # First call starts at root
        if node is None:
            node = self.container

        # Draw name
        y = self.write_row(y, depth, indexes, str(node))
        # y = self.write_row(y, depth, indexes)

        # Draw children
        children = node.get_children()
        max_child_name = max([len(str(c)) for c in children])
        for i, child in enumerate(children):
            # Preven aliasing
            new_depth = copy.deepcopy(depth)
            new_index = copy.deepcopy(indexes)
            # Update
            new_depth.append(i != len(children)-1)
            new_index.append(i)

            if not isinstance(child, str):
                # Draw recurssive child
                y = self.draw(child, new_depth, y, new_index)
                # Add spacing between kids
                if i != len(children)-1 and len(children):
                    y = self.write_row(y, new_depth, indexes)
            else:
                val = f"{child.capitalize():<{max_child_name}}: {node[i]}"
                y = self.write_row(y, new_depth, new_index, val)
        return y

    # ==== Get Information ====
    def get_selected(self, ind=None):
        # Get selected item at the index
        if ind is None:
            ind = self.index

        # Fetch into container, checking if you bottomed out on a value rather than another container of some kind
        bottom = False
        obj = self.container
        parent = obj
        for i in ind:
            if type(obj[i]) not in [int, float]:
                parent = obj
                obj = obj[i]
            else:
                bottom = True
        return obj, parent, bottom

    # ==== Modification
    def add_to_selected(self, add, ind=None):
        # Adds new item to selected 
        if ind is None:
            ind = self.index

        selected, parent, bottom = self.get_selected(ind)
        if isinstance(selected, collection.Collection):
            selected.add(add)
        elif len(ind) > 1:
            self.add_to_selected(add, ind[:-1])
        return

    def toggle_selected(self):
        # Toggles selected. Handled internally
        selected, parent, bottom = self.get_selected()
        selected.toggle()
        return

    def edit_value(self):
        curses.curs_set(True)
        
        # Let the user type a number and assign it to the value
        # Center input 
        # Add dynamic name instead of enter new val
        self.stdscr.addstr(1, 15, "+-------------------------------+")
        self.stdscr.addstr(2, 15, "| Enter new value:              |")
        self.stdscr.addstr(3, 15, "+-------------------------------+")
        self.stdscr.clrtoeol()
        curses.echo()
        input_str = self.stdscr.getstr(2, 35).decode()
        curses.noecho()
        try:
            value = float(input_str) if '.' in input_str else int(input_str)
            selected, parent, bottom = self.get_selected()
            selected[self.index[-1]] = value
        except ValueError:
            pass  # Ignore invalid input
        

        curses.curs_set(False)
        return

    # ==== Main Loop ====
    def run(self):
        while True:
            # --- Run loop ---
            self.stdscr.clear()
            self.draw()
            # This calls refresh |
            # for us             V
            c = self.stdscr.getch()
            

            # ===== KEYSTROKES ====
            # --- Navigation --- 
            selected, parent, bottom = self.get_selected(self.index)
            # Move selection
            if self.index != [] and c in [curses.KEY_UP, curses.KEY_DOWN] and (len(parent) > 1 or (bottom and len(selected) > 1)):
                # Index direction
                key = ([curses.KEY_UP, curses.KEY_DOWN].index(c) * 2) - 1
                
                scroll_len = len(parent) if not bottom else len(selected)

                self.index[-1] = (self.index[-1]+key)%scroll_len
            # --- Depth
            # Travel up the tree
            elif c == curses.KEY_LEFT:
                if len(self.index) > 0:
                    self.index.pop()
            # Travel down the tree
            elif c == curses.KEY_RIGHT:
                # Ensure the selected thing is a collection, and if we are indexing that we are
                # Attempting to travel into content not into a setting
                if not bottom:
                    self.index.append(0)
            # ---
            # Jump to root
            elif c == ord('r'):
                self.index = []

            # --- Creation ---
            # Add new container
            elif c == ord('a'):
                self.add_to_selected(collection.Collection())
            elif c == ord('w'):
                self.add_to_selected(waveform.Waveform())
            
            # --- Modification ---
            # TODO get curses KEY for tab since KEY_STAB and such doesn't work??
            elif c == 9:
                self.toggle_selected()
            # --- Quit ---
            elif c == ord('q'):
                break
            # elif c == curses.KEY_ENTER:
            elif c == ord('\n') and bottom:
                self.edit_value()
        # We have a wrapper so we don't actually need to call this.
        # self.kill()
        return


def main(stdscr):
    app = Curse()
    app.stdscr = stdscr
    app.run()


# Wrapper ensures the terminal is restored to a useable state after exiting or crashing
curses.wrapper(main)
