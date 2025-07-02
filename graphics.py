import copy, curses
import numpy as np
import point_cloud, collection, waveform, variable_box


# === Keystrokes detection ===
# Curses don't detect multiple presses but you can check for something like this
def ctrl(ch):
    return ord(ch) & 0x1f

def shift(key):
    """
    Detect if the key code corresponds to a shifted letter (A-Z).
    In curses, uppercase letters (shifted) have ASCII codes 65-90.
    """
    return 65 <= key <= 90


# ==== UI ====
# This handles the graphics and interfacing with the collective data
class Curse:
    def __init__(self, sound_buffer):
        # --- Setup ---
        self.setup_curse()

        # --- Sound Buffer ---
        # This is the shared buffer between objects that allows the buffer from the contained values to
        # pass to the sounddevice in sound_output.py
        self.sound_buffer = sound_buffer
        self.sound_buffer.compute_buffer = self.update_buffer

        # --- Visual Settings ---
        # Standout is also good. Maybe switch back if visibility is bad on blink
        # self.selected_display_mode = curses.A_BLINK
        self.selected_display_mode = curses.A_STANDOUT
        self.collapsed_text = '[...]'
        # Title settings
        self.selected_title_mode = curses.A_STANDOUT
        self.tree_title = 'Data'
        self.starting_tree_y = 1
        self.variable_title = 'Variables'
        self.starting_variable_y = 1
        self.variable_offset = curses.COLS - 20
        self.input_width = 31

        # --- Internal ---
        # index of [] is the root
        self.index = []
        # If selecting variable or not
        self.in_variable_menu = False
        self.variable_index = []
        # This is the core data tree of the whole everything
        # Maybe it shouldn't live in graphics but thats ok :)
        self.container = point_cloud.PointCloud(
            name="■"
            )
        self.variables = variable_box.VariableBox(
            name="Global Variables"
            )

        # This is the size of the window to be used for placing some graphics
        # y, x to be consistent with curses
        self.size = [curses.LINES, curses.COLS]
        # Highlights for selecting terms
        self.highlights = []
        # Copied item
        self.copied = None
        # Total Runtime (from sound output)
        self.runtime = 0

        # --- Interface ---
        # All inputs are mapped below, being made like this allows multiple and different remappings
        self.hotkey_map = {
            # Movement
            'UP': [curses.KEY_UP],
            'DOWN': [curses.KEY_DOWN],
            'LEFT': [curses.KEY_LEFT],
            'RIGHT': [curses.KEY_RIGHT],
            # Bigger nav jumps
            # These are the arrow keys with shift held
            'STRONGUP': [547],
            'STRONGDOWN': [548],
            'STRONGLEFT': [391],
            'STRONGRIGHT': [400],
            # CRUD
            'ADDPOINTCLOUD': [],
            'ADDCOLLECTION': [ord('a')],
            'ADDWAVEFORM': [ord('w')],
            'EDIT': [ord('\n')],
            'SELECT': [ord('S')],
            # 27 is escape
            'DESELECT': [27],
            'CUT': [],
            'COPY': [ord('C')],
            'PASTE': [ord('V')],
            'DELETE': [],
            'MOVE': [],
            'DUPLICATE': [],
            # Visuals
            'COLLAPSE': [ord('/')],
            'COLLAPSEALL': [ord('?')],
            'JUMPROOT': [ord('r')],
            'TOGGLE': [ord('\t')],
            # Controls
            # 27 is escape. Needs to be pressed twice in a row
            'QUIT': [27],
            # --- Variables
            # shift tab
            'TOGGLEVARIABLE': [351],
            'ADDVARIABLE': [ord('a')],
            'BINDVARIABLE': [ord('x')]
        }
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
        curses.curs_set(False)
        return

    def write_row(self, y_pos, ind, depth=[], indexes=[], text=None, title=False, selected_title=False, x_offset=0):
        """
        This writes a full row of the tree with branches, selection, highlighting, and text.
        See draw for y, depth, indexes.
        Text is the text written at that row.
        """
        # Don't crash from offscreen :)
        # Eventually scrolling will be added.
        if y_pos >= curses.LINES:
            return y_pos
        
        # Ensure that the index is at least as deep as the highlight and that the current index is highlighted
        highlighted = len(indexes) >= len(self.highlights) > 0 and indexes[:len(self.highlights)] == self.highlights

        # If text is None, just write an empty row
        x = 1 + x_offset
        for i, d in enumerate(depth):
            # Depth of value
            if i == len(depth)-1 and text is not None:
                if highlighted and i > len(self.highlights)-1:
                    self.stdscr.addstr(y_pos, x, "├" if d else "└", self.selected_display_mode)
                else:
                    self.stdscr.addstr(y_pos, x, "├" if d else "└")
            # Bars underneath
            else:
                if highlighted and i > len(self.highlights)-1:
                    self.stdscr.addstr(y_pos, x, "|" if d else "", self.selected_display_mode)
                else:
                    self.stdscr.addstr(y_pos, x, "|" if d else "")
            # Step size between depths (leaves room for arrow at least)
            x += 2
        # Ignore writing things for a spacer
        if text is not None:
            # If selected
            if ind == indexes and not title:
                self.stdscr.addch(y_pos, x-1, curses.ACS_RARROW, curses.A_BOLD)
            if highlighted:
                self.stdscr.addstr(y_pos, x, text, self.selected_display_mode)
            elif title:
                if selected_title:
                    self.stdscr.addstr(y_pos, x, text, self.selected_title_mode)
                else:
                    self.stdscr.addstr(y_pos, x, text)
            else:
                self.stdscr.addstr(y_pos, x, text)
        y_pos += 1
        return y_pos
    
    def draw(self):
        """
        This draws everything
        - titles
        - trees
        - runtime
        """
        # Titles
        self.write_row(
            y_pos=self.starting_tree_y-1,
            ind=self.index,
            text=self.tree_title,
            title=True,
            selected_title=not self.in_variable_menu
        )
        self.write_row(
            y_pos=self.starting_variable_y-1,
            ind=self.variable_index,
            text=self.variable_title,
            title=True,
            selected_title=self.in_variable_menu,
            x_offset=self.variable_offset
        )
        # Draw trees
        self.draw_tree(ind=self.index)
        self.draw_tree(
            ind=self.variable_index,
            node=self.variables,
            x_offset=self.variable_offset,
            y=self.starting_variable_y,
            variable_menu=True)
        # Runtime
        runtime_text = f"Total Runtime: {round(self.runtime, 2)}"
        self.stdscr.addstr(curses.LINES-2, curses.COLS-len(runtime_text), runtime_text)
        return

    def draw_tree(self, ind, node=None, depth=[], y=None, indexes=[], x_offset=0, variable_menu=False):
        """
        node:
            - The element of the tree you are selecting
        depth:
            - This indicates the horizontal depth in the tree.
            - The values are bools showing if that depth is the last child to draw ├ or └ for the tree
        y:
            - This passes along the actual y coord on the terminal we are drawing.
            - This gets passed along each time something is called.
        indexes:
            - This is the current _i_ndex of each respective branch of the tree.
        """
        if y is None:
            y = self.starting_tree_y

        # Don't crash
        if y >= curses.LINES or (node is not None and len(node) == 0):
            return y

        # First call starts at root
        if node is None:
            node = self.container

        # Draw name
        y = self.write_row(y, ind, depth, indexes, str(node), x_offset=x_offset)

        # Draw children
        children = node.get_children()
        # If collapsed only draw a collapsed indicator
        if node.collapsed:
            # -- Create new depth and indexes
            children = [self.collapsed_text]
        # Otherwise draw the rest of the tree
        # else:
        max_child_name = max([len(str(c)) for c in children])
        for i, child in enumerate(children):
            # -- Create new depth and indexes
            # Preven aliasing
            new_depth = copy.deepcopy(depth)
            new_index = copy.deepcopy(indexes)
            # Update
            new_depth.append(i != len(children)-1)
            new_index.append(i)

            if not isinstance(child, str):
                # Draw recurssive child
                y = self.draw_tree(
                    ind=ind,
                    node=child,
                    depth=new_depth,
                    y=y,
                    indexes=new_index,
                    x_offset=x_offset)
                # Add spacing between kids
                if i != len(children)-1 and len(children):
                    y = self.write_row(y, ind, new_depth, indexes, x_offset=x_offset)
            else:
                # If collapsed only draw the collapsed text
                if child == self.collapsed_text:
                    val = child
                # otherwise draw children as usual
                else:
                    val = node[i]
                    text = child if variable_menu else child.capitalize()
                    val = f"{text:<{max_child_name}}: {val}"
                y = self.write_row(y, ind, new_depth, new_index, val, x_offset=x_offset)
        return y

    # ==== Get Information ====
    def get_index(self, is_variable):
        if is_variable:
            return self.variable_index
        else:
            return self.index

    def get_selected(self, is_varaible, ind=None):
        # Get selected item at the index
        if ind is None:
            ind = self.get_index(is_varaible)

        # Fetch into container, checking if you bottomed out on a value rather than another container of some kind
        bottom = False
        obj = self.variables if is_varaible else self.container
        parent = obj
        for i in ind:
            # Bottomed out or collapsed
            if type(obj[i]) in [int, float] or obj.collapsed:
                bottom = True
            # If not keep going in
            else:
                parent = obj
                obj = obj[i]

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
        selected, parent, bottom = self.get_selected(self.in_variable_menu)
        selected.toggle()
        return

    def user_input(self, message):
        # Prompt for variable name
        x_pos = 15
        y_pos = curses.LINES - 7

        self.stdscr.addstr(y_pos, x_pos, f"+{'-'*self.input_width}+")
        self.stdscr.addstr(y_pos+1, x_pos, f"| {message:<{self.input_width-1}}|")
        self.stdscr.addstr(y_pos+2, x_pos, f"+{'-'*self.input_width}+")
        self.stdscr.clrtoeol()
        curses.echo()
        input_str = self.stdscr.getstr(y_pos+1, x_pos+len('| '+ message)).decode()
        curses.noecho()
        return input_str

    def edit_value(self):
        curses.curs_set(True)
        
        # User input
        # Center input 
        # Add dynamic name instead of enter new val
        # TODO allow pi.

        input_str = self.user_input('Enter new value:')
        try:
            value = float(input_str) if '.' in input_str else int(input_str)
            selected, parent, bottom = self.get_selected(self.in_variable_menu)
            if self.in_variable_menu:
                print(self.variable_index)
                self.variables[self.variable_index[-1]] = value
                print(self.variables.variables)
            else:
                selected[self.index[-1]] = value
        except ValueError:
            # Ignore invalid input
            pass

        curses.curs_set(False)
        return

    def add_variable(self):
        curses.curs_set(True)

        var_name = self.user_input('Enter variable name:')
        var_value_str = self.user_input('Enter variable value:')

        try:
            var_value = float(var_value_str) if '.' in var_value_str else int(var_value_str)
            # Add a collection with a constant of the inputed value
            self.variables.add(
                var_name,
                collection.Collection(
                    name=var_name,
                    content=[
                        waveform.Waveform(
                            mode='CONSTANT',
                            amplitude=var_value
                            )])
            )
        except ValueError:
            # Ignore invalid input
            pass

        curses.curs_set(False)
        return

    def bind_variable(self):
        # Discard other returns                      |
        #                                            V
        param = self.get_selected(is_varaible=False)[0]
        variable = self.variables[self.variable_index[0]]

        try:
            param[self.index[-1]] = variable
        except ValueError:
            pass

        return

    def soft_reset_index(self, bottom):
        # Often when something is reset the index needs to be saftely reset to the top so you aren't indexing something non existant.
        if len(self.index) > 0 and bottom:
            self.index[-1] = 0

        # TODO this resets index even if the old index is allowed within the new
        # selection
        return

    # ==== Keystrokes ====
    def run(self):
        running = True
        last_key = None

        while running:
            # === Run loop ===
            self.stdscr.clear()
            self.draw()
            # This calls refresh | to display new updates
            # for us             V
            c = self.stdscr.getch()
            # Some inputs want you to deselect such as adding things, deselecting, etc
            deselect = False

            # === Global Hotkeys ===
            selected_index = self.get_index(self.in_variable_menu)
            selected, parent, bottom = self.get_selected(self.in_variable_menu)
            # Switch menus
            if c in self.hotkey_map['TOGGLEVARIABLE']:
                self.in_variable_menu = not self.in_variable_menu
            # --- Quit ---
            elif c in self.hotkey_map['QUIT'] and last_key in self.hotkey_map['QUIT']:
                running = False
            # === Navigation ===
            # Move selection
            elif selected_index != [] and c in self.hotkey_map['UP']+self.hotkey_map["DOWN"] and (len(parent) > 1 or (bottom and len(selected) > 1)):
                # Index direction
                key = (int(c in self.hotkey_map['DOWN']) * 2) - 1
                
                scroll_len = len(parent) if not bottom else len(selected)

                selected_index[-1] = (selected_index[-1]+key)%scroll_len
            # --- Depth
            # Travel up the tree
            elif c in self.hotkey_map['LEFT']:
                if len(selected_index) > 0:
                    selected_index.pop()
            # Travel down the tree
            elif c in self.hotkey_map['RIGHT']:
                # Ensure the selected thing is a collection, and if we are indexing that we are
                # Attempting to travel into content not into a setting
                if not bottom:
                    selected_index.append(0)
            # ---
            # Jump to root
            elif c in self.hotkey_map['JUMPROOT']:
                selected_index = []
            # === Modification ===
            elif c in self.hotkey_map['EDIT'] and bottom:
                    self.edit_value()

            # === Variable Menu ===
            if self.in_variable_menu:
                if c in self.hotkey_map['ADDVARIABLE']:
                    self.add_variable()

                last_key = c
            # === Main Data Tree ===
            else:
                # === Creation ===
                # Add new container
                if c in self.hotkey_map['ADDCOLLECTION']:
                    deselect = True
                    self.add_to_selected(collection.Collection())
                elif c in self.hotkey_map['ADDWAVEFORM']:
                    deselect = True
                    self.add_to_selected(waveform.Waveform())
                
                # === General Controls ===
                # Highlight selected
                elif c in self.hotkey_map['SELECT']:
                    if self.highlights is None or self.highlights != self.index:
                        self.highlights = copy.deepcopy(self.index)
                    else:
                        self.highlights = []
                # Copy  
                # elif c in self.hotkey_map['COPY'] and len(self.highlights) > 0:
                #     self.copied = copy.deepcopy(self.get_selected(self.highlights))[0]
                # # Paste
                # elif c in self.hotkey_map['PASTE'] and self.copied is not None:
                #     self.add_to_selected(self.copied)
                # --- Collapsing
                # Single collapse
                elif c in self.hotkey_map['COLLAPSE']:
                    selected.toggle_collapse()
                    self.soft_reset_index(bottom)
                # Collapse all
                elif c in self.hotkey_map['COLLAPSEALL']:
                    if hasattr(selected, "set_all_collapse"):
                        selected.set_all_collapse(not selected.collapsed)
                    else:
                        selected.toggle_collapse()
                    self.soft_reset_index(bottom)
                # ---

                # === Modification ===
                # TODO get curses KEY for tab since KEY_STAB and such doesn't work?
                elif c in self.hotkey_map['TOGGLE']:
                    deselect = True
                    self.toggle_selected()
                    self.soft_reset_index(bottom)
                elif c in self.hotkey_map['BINDVARIABLE'] and len(self.variable_index) > 0:
                    self.bind_variable()

                last_key = c
                # --- Deselect ---
                # Unhighlight
                if deselect or c in self.hotkey_map['DESELECT']:
                    # Often esc or a 'quit' key will also be used to deselect in which case you do not want to count it as a quit when you are deselecting
                    if c in self.hotkey_map['QUIT'] and self.highlights != []:
                        last_key = None
                    self.highlights = []

        return

    # =====================
    # === Functionality ===
    # =====================
    def compute_buffer(self, t):
        # return np.cos(2 * np.pi * 440 * t), np.sin(2 * np.pi * 120 * t)
        return self.container.compute_buffer(t)

    def update_buffer(self, t):
        buffer = self.compute_buffer(t)
        self.runtime = t[-1]
        return buffer


def main(stdscr, shared_buffer):
    app = Curse(shared_buffer)
    app.stdscr = stdscr
    app.run()
    return


def run(shared_buffer):
    # Wrapper ensures the terminal is restored to a useable state after exiting or crashing
    # Also pass the shared buffer into the initialization
    curses.wrapper(lambda stdscr: main(stdscr, shared_buffer))
