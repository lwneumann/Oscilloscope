from enum import Enum
import shapes


# This is similar to a collection though just holds variables to be bound to things
class VariableBox(shapes.ParamShape):
    def __init__(self, name, collapsed=False):
        super().__init__(
            index_map=[],
            parameter_names=[],
            collapsed=collapsed
            )
        self.name = name
        self.variables = {}
        return
    
    # ==== Magic Methods ====
    def __getitem__(self, i):
        if isinstance(i, str):
            return self.variables.get(i)
        else:
            return self.variables.get(self.parameter_names[i])

    def __setitem__(self, i, v):
        if isinstance(i, str):
            self.variables[i] = v
        else:
            self.variables[self.parameter_names[i]] = v
        return
    
    def __len__(self):
        return len(self.variables)

    def __str__(self):
        return self.name

    # === Functionality ===
    def add(self, name, val):
        # Add name
        self.parameter_names.append(name)
        self._index_map.append(name)

        # Add value
        self.variables[name] = val
        return
    
    def get_children(self):
        return list(self.variables.values())
