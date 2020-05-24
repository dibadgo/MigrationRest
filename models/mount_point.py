class MountPoint:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str):
            raise RuntimeError('name should be a string!')

        self._name = new_name

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        if not isinstance(new_size, int):
            raise RuntimeError('size should be an int!')

        self._size = new_size

    def __eq__(self, other):
        return self.name == other.name and self.size == other.size