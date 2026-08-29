class JSONable:
    """
    implemented by all classes that can write themselves down as JSON objects
    """
    def __tojson__(self):
        return {'type':self.typename()}

    def __fromjson__(self,d:dict):
        raise NotImplementedError()

    def typename(self):
        return type(self).__name__
