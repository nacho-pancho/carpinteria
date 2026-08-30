class JSONable:
    """
    implemented by all classes that can write themselves down as JSON objects
    """
    def __tojson__(self):
        raise NotImplementedError()


