class Token:
    def __init__(self, name: str, value: str, position: int):
        self.name = name
        self.value = value
        self.position = position

    def __repr__(self):
        return '<Token({}, {}, {})>'.format(self.name, self.value,
                                            self.position)
