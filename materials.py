from jsonable import JSONable
from  dataclasses import dataclass
"""
Define properties of materials, including their name, specifications and textures
"""

#==========================================================

type ColorSpec = tuple[float,float,float]

#==========================================================

BROWN_COLOR = (0.6,0.4,0.1)
WHITE_COLOR = (1.0,0.9,0.8)
EUCALYPTUS_COLOR = (0.8,0.7,0.5)
STEEL_COLOR = (0.8,0.9,1.0)
BRONZE_COLOR = (0.8,0.6,0.4)
LIGHT_WOOD_COLOR = (0.9,0.75,0.6)

#==========================================================

@dataclass 
class Texture(JSONable):
    color:list[float]=None,
    opacity:float=1
    texture_map:str=None # optional name of image for texture mapping
    ambient:float=None # see pyvista.add_mesh
    diffuse:float=None # see pyvista.add_mesh
    roughness:float=None # see pyvista.add_mesh
    specular:float=None # see pyvista.add_mesh
    specular_power:float=None # see pyvista.add_mesh
    metallic:float=None # see pyvista.add_mesh

    def to_dict(self):
        return {
            'color': self.color,
            'opacity': self.opacity,
            'texture_map': self.texture_map,
            'ambient': self.ambient,
            'diffuse': self.diffuse,
            'roughness': self.roughness,
            'specular': self.specular,
            'specular_power': self.specular_power,
            'metallic': self.metallic
        }

    def from_dict(d:dict):
        return Texture(
            color=d['color'],
            opacity=d['opacity'],
            texture_map=d['texture_map'],
            ambient=d['ambient'],
            diffuse = d['diffuse'],
            roughness=d['roughness'],
            specular=d['specular'],
            specular_power=d['specular_power'],
            metallic=d['metallic']
        )

#==========================================================

@dataclass 
class Material(JSONable):
    name:str
    interior:Texture
    exterior:Texture

    def to_dict(self):
        return { 
            'name': self.name,
            'interior': self.interior.to_dict(),
            'exterior': self.exterior.to_dict()
        }

    def from_dict(d:dict):
        return Material(name=d['name'],
                        interior=Texture.from_dict(d['interior']),
                        exterior=Texture.from_dict(d['exterior']))


#==========================================================

FINGER_TEXTURE = Texture(color=EUCALYPTUS_COLOR,texture_map='textures/finger.jpg',specular=0.2)
MDF_INT_TEXTURE = Texture(color=BROWN_COLOR)
MDF_EXT_TEXTURE = Texture(color=WHITE_COLOR)
STEEL_TEXTURE   = Texture(color=STEEL_COLOR,metallic=1,roughness=0.5)
BRONZE_TEXTURE   = Texture(color=BRONZE_COLOR,metallic=1,roughness=0.25)
LIGHT_WOOD_TEXTURE = Texture(color=LIGHT_WOOD_COLOR)
WHITE_PLASTIC_TEXTURE = Texture(color=WHITE_COLOR)

#==========================================================

MDF_MATERIAL    = Material('MDF',interior=MDF_INT_TEXTURE,exterior=MDF_EXT_TEXTURE)
FINGER_MATERIAL = Material('FINGER',interior=FINGER_TEXTURE,exterior=FINGER_TEXTURE)
GUIDE_MATERIAL  = Material('SCREW',interior=STEEL_TEXTURE,exterior=STEEL_TEXTURE)
FLAT_SCREW_MATERIAL  = Material('FLAT_SCREW',interior=STEEL_TEXTURE,exterior=STEEL_TEXTURE)
WOOD_SCREW_MATERIAL  = Material('WOOD_SCREW',interior=BRONZE_TEXTURE,exterior=BRONZE_TEXTURE)
NAIL_MATERIAL  = Material('NAIL',interior=STEEL_TEXTURE,exterior=STEEL_TEXTURE)
DOWEL_MATERIAL  = Material('DOWEL',interior=LIGHT_WOOD_TEXTURE,exterior=LIGHT_WOOD_TEXTURE)
CORNER_MATERIAL  = Material('CORNER',interior=WHITE_PLASTIC_TEXTURE,exterior=WHITE_PLASTIC_TEXTURE)
