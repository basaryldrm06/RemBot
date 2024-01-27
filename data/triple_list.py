class TripleList:
    def __init__(self):
        self.data = [None, None, None]

    def add(self, new_value):
        self.data.pop(0)
        self.data.append(new_value)

    def get_values(self):
        return self.data

    def confirm(self, check_value):
        return self.data[0] == check_value and \
        self.data[1] == check_value and \
        self.data[2] == check_value

