from  dataclasses import dataclass
"""
Define properties of materials, including their name, specifications and textures
"""

type ColorSpec = tuple[float,float,float]


BROWN_COLOR = (0.6,0.4,0.1)
WHITE_COLOR = (1.0,0.9,0.8)
EUCALYPTUS_COLOR = (0.8,0.7,0.5)
STEEL_COLOR = (0.8,0.9,1.0)
BRONZE_COLOR = (0.8,0.6,0.4)

@dataclass 
class Texture():
    color:list[float]=None,
    opacity:float=1
    texture_map:str=None # optional name of image for texture mapping
    ambient:float=None # see pyvista.add_mesh
    diffuse:float=None # see pyvista.add_mesh
    roughness:float=None # see pyvista.add_mesh
    specular:float=None # see pyvista.add_mesh
    specular_power:float=None # see pyvista.add_mesh
    metallic:float=None # see pyvista.add_mesh

@dataclass 
class Material():
    name:str
    interior:Texture
    exterior:Texture

FINGER_TEXTURE = Texture(color=EUCALYPTUS_COLOR,texture_map='textures/finger.jpg',specular=0.2)
MDF_INT_TEXTURE = Texture(color=BROWN_COLOR)
MDF_EXT_TEXTURE = Texture(color=WHITE_COLOR)
STEEL_TEXTURE   = Texture(color=STEEL_COLOR,metallic=1,roughness=0.5)
BRONZE_TEXTURE   = Texture(color=BRONZE_COLOR,metallic=1,roughness=0.25)

MDF_MATERIAL    = Material('MDF',interior=MDF_INT_TEXTURE,exterior=MDF_EXT_TEXTURE)
FINGER_MATERIAL = Material('FINGER',interior=FINGER_TEXTURE,exterior=FINGER_TEXTURE)
GUIDE_MATERIAL  = Material('SCREW',interior=STEEL_TEXTURE,exterior=STEEL_TEXTURE)
FLAT_SCREW_MATERIAL  = Material('FLAT_SCREW',interior=STEEL_TEXTURE,exterior=STEEL_TEXTURE)
WOOD_SCREW_MATERIAL  = Material('WOOD_SCREW',interior=BRONZE_TEXTURE,exterior=BRONZE_TEXTURE)