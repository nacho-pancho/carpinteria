
import json

from jsonable import *
from geometry import *
from pieces import *
from materials import *
from layout import *


class PieceEncoder(json.JSONEncoder):
    """
    custom class for using JSONable objects
    """
    def default(self,obj):
        if isinstance(obj,JSONable):
            return obj.__json__()
        else:
            return super().default(obj)

"""
custom function to decode objects from JSON
"""
def jsonable_object_hook(d:dict):
    if 'type' in d:
        t = globals(d['type'])
    return t.__fromjson__(d)


if __name__ == '__main__':
    print(globals())