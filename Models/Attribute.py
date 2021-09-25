class Attribute:

    def __init__(self, name=None, is_getter=True, is_setter=True, type=None, privacy=None):
        self.name = name
        self.type = type
        self.is_getter = is_getter
        self.is_setter =  is_setter
        self.privacy = privacy

    def atr_string(self):
        getset = "{"
        if self.is_getter:
            getset = getset + "get; "
        if self.is_setter:
            getset = getset + "set; "
        getset = getset + "}"

        return str(self.privacy + " " + self.type + " " + self.name + " " + getset)