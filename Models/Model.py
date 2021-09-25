class Model:
    
    def __init__(self, name=None, attributes=[], is_abstract=True):
        self.attributes = attributes
        self.name = name
        self.is_abstract = is_abstract
