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
            return self.variables[i]
        elif isinstance(i, list):
            return self.variables[self.parameter_names[i[0]]][1:]
        else:
            return self.variables[self.parameter_names[i]]

    def __setitem__(self, i, v):
        # Set variable by name
        if isinstance(i, str):
            self.variables[i] = v
        # Set subobject
        elif isinstance(i, list):
            obj = self.variables[self.parameter_names[i[0]]]
            if len(i) == 1:
                obj = v
                self.variables[self.parameter_names[i[0]]] = v
            else:
                # Traverse down to the last object
                current = obj
                for idx in i[1:-1]:
                    current = current[idx]
                current[i[-1]] = v
        # Set via indexing number
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
        self.index_map.append(name)

        # Add value
        self.variables[name] = val
        # Mark as a variable
        self.variables[name].is_a_variable = True
        return
    
    def get_children(self):
        return list(self.variables.values())
