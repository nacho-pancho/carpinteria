class JSONable:
    """
    implemented by all classes that can write themselves down as JSON objects
    """
    def to_dict(self):
        raise NotImplementedError()


