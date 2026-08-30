"""
the idea is that projects can be fully specified as a JSON file
a project has a list of parts, a name, a date and an author
"""

import json

from jsonable import *
from util import *
from geometry import *
from core import *
from layout import *
from pieces import *
from materials import *


class PieceEncoder(json.JSONEncoder):
    """
    custom class for using JSONable objects
    """
    def default(self,obj):
        if isinstance(obj,JSONable):
            return obj.__tojson__()
        else:
            return super().default(obj)

"""
custom function to decode objects from JSON
"""
def jsonable_object_hook(d:dict):
    if 'type' in d:
        t = globals(d['type'])
    return t.__fromjson__(d)


def load_project(fname):
    """
    load project from file
    """
    with open(fname,'r',encoding='utf-8') as f:
        d = json.load(f)
        return dict_to_project(d) 

def save_project(fname:str,p:Project):
    """
    save project to file
    """
    with open(fname,'w',encoding='utf8') as f:
        d = p.__tojson__()
        json.dump(d,f)


def dict_to_layout(d:dict):
    type = d['type']



def dict_to_part(d:dict):
    return Part(dict_to_piece(d['piece']),constraints=LayoutConstraints.from_dict(d['constraints']))


def dict_to_composite(d:dict):
    name = d['name']
    min_size = Size(d['min_size'])
    max_size = Size(d['max_size'])
    layout = dict_to_layout(d['layout'])
    piece = CompositePiece(name=name,min_size=min_size,max_size=max_size,layout=layout)
    parts = d['parts']
    for p in parts:
        piece.add_part(dict_to_part(p))



def dict_to_piece(d:dict):
    type = d['type'] # very important field
    if type == 'composite': # the only special one that needs to be treated differently
        return dict_to_composite(d)
    else:
        # the rest (non composite) have their own way of decoding themselves
        piece_type = PIECE_TYPES[type]
        return piece_type.from_dict(d)


def dict_to_project(d:dict):
    project = Project(d['name'],
                      version=d['version'],
                      date=d['date'],
                      author=d['author'],
                      description=d['description']
                      )
    pieces = d['pieces'] # a list
    for p in pieces: # p should be a dict
        project.add_piece(dict_to_piece(p))
    return project

if __name__ == '__main__':
    print(globals())