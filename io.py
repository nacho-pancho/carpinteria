from geometry import *
from core import *
from pieces import *

import json

class PieceEncoder(json.JSONEncoder):

    def default(self,obj):
        if isinstance(obj,Piece):
            return obj.__json__()
        else:
            return super().decode(obj)


def piece_object_hook(d:dict):
    if 'material' in d:
        t = d['type']
    return None