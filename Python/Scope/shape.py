"""
This is the base class for everything else.

It has some general methods used by its children;
set_mode - This sets the internal mode explicitly
toggle   - This cycles the internal mode

get_children - In case the object gets called by draw on accident this catches that.
"""

class Shape:
    def __init__(self, modes=None):
        if modes is not None:
            self.enumModes = modes
            self.set_mode(1)
        return
    
    # ==== Change Settings ====
    def set_mode(self, m):
        # Set mode explicitly
        if m in [mode.name for mode in list(self.enumModes)]:
            self.mode = self.enumModes[m]
        elif m in [mode.value for mode in list(self.enumModes)]:
            self.mode = self.enumModes(m)
        else:
            raise KeyError(f"{m} is not a valid {self.enumModes.__name__} key")
        return
    
    def toggle(self):
        # Cycle through modes
        modes = list(self.enumModes)
        self.mode = modes[(self.mode.value)%len(modes)]
        return

    # ==== Graphics ====
    def get_children(self):
        return []


class ParamShape(Shape):
    def __init__(self, modes=None, parameter_names=[]):
        super().__init__(modes)
        self.parameter_names = parameter_names
        return

    # ==== Magic Methods
    def __str__(self):
        return self.mode.name

    def __repr__(self):
        return str(self)
    
    def __len__(self):
        return len(self.parameter_names)
    
    # ==== Graphics ====
    def get_children(self):
        return self.parameter_names