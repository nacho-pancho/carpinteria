from  dataclasses import dataclass
"""
Define properties of materials, including their name, specifications and textures
"""

type ColorSpec = tuple[float,float,float]

@dataclass 
class Material():
    name:str
    interior_color:ColorSpec
    surface_color:ColorSpec
    texture:str # optional name of image for texture mapping

    def get_colormap(self):
        return [self.interior_color,self.surface_color]

BROWN_COLOR = (0.6,0.4,0.1)
WHITE_COLOR = (1.0,0.9,0.8)

WHITE_MDF = Material('MDF',BROWN_COLOR,WHITE_COLOR)

