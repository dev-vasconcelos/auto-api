class Attribute:

    def __init__(self, name=None, is_getter=True, is_setter=True, type="", privacy="", notations=[""]):
        self.name = name
        self.type = type
        self.is_getter = is_getter
        self.is_setter =  is_setter
        self.privacy = privacy
        self.notations = notations
    
    def atr_string(self):
        getset = "{"
        if self.is_getter:
            getset = getset + "get; "
        if self.is_setter:
            getset = getset + "set; "
        getset = getset + "}"

        return_string = ""

        for n in self.notations:
            return_string = return_string + str(n) + "\n"

        return_string = return_string + self.privacy + " " + self.type + " " + self.name + " " + getset
        
        return str(return_string)