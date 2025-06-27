import shape


class Constant(shape.ParamShape):
    def __init__(self, value=1, driver=None):
        super().__init__(
            parameter_names=['Value'],
            index_map=['value'],
            driver=driver
        )

        self.value = value
        return

    def __len__(self):
        base_len = 1
        if not self.collapsed:
            base_len += (self.drive is not None)
        return base_len

    def compute_buffer(self, t):
        # 
        return self.value