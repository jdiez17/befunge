class Cell(object):
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "<Cell (kind '%s'): '%s'>" % (self.kind, self.value)
