"""
This is the base class for everything else.

It has some general methods used by its children;
set_mode - This sets the internal mode explicitly
toggle   - This cycles the internal mode

get_children - In case the object gets called by draw on accident this catches that.
"""


# A shape is anything that has an Enum mode selector
# WITHOUT generic internal parameters.
class Shape:
    def __init__(self, modes=None, start_mode=None):
        if modes is not None:
            self.enumModes = modes
            self.set_mode(start_mode or 1)
        return
    
    # ==== Magic Methods ====
    def __str__(self):
        if hasattr(self, 'mode'):
            return self.mode.name
        else:
            return self.__class__.__name__

    def __repr__(self):
        return str(self)

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


# This is an extended shape class with internal parameters.
class ParamShape(Shape):
    def __init__(self, modes=None, parameter_names=[], index_map=[], start_mode=None):
        super().__init__(modes, start_mode)
        self.parameter_names = parameter_names
        self._index_map = index_map
        return

    # ==== Magic Methods
    def __getitem__(self, i):
        # Indexing from main and recurrsive indexing from collection is dicey so clear this just in case
        if isinstance(i, list) and len(i) == 1:
            i = i[0]

        if i >= len(self) or i < 0:
            raise IndexError(f"{self.__class__.__name__} index {i} is out of range")
        
        return getattr(self, self._index_map[i])

    def __setitem__(self, i, v):
        # Indexing from main and recurrsive indexing from collection is dicey so clear this just in case
        if isinstance(i, list) and len(i) == 1:
            i = i[0]

        if i >= len(self) or i < 0:
            raise IndexError(f"{self.__class__.__name__} index {i} is out of range")
        
        setattr(self, self._index_map[i], v)
        return

    def __len__(self):
        return len(self._index_map)
    
    # ==== Graphics ====
    def get_children(self):
        return self.parameter_names
