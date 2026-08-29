"""
the idea is that projects can be fully specified as a JSON file
a project has a list of parts, a name, a date and an author
"""

import json

from jsonable import *
from core import *
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


def load_project():
    pass

def save_project():
    pass


if __name__ == '__main__':
    print(globals())