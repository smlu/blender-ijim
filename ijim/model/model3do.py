from enum import IntEnum
from typing import Tuple, List
from ijim.types.vector import *

class GeometryMode(IntEnum):
    NotDrawn   = 0
    VertexOnly = 1
    Wireframe  = 2
    Solid      = 3
    Texture    = 4
    Full       = 5

class LightMode(IntEnum):
    FullyLit  = 0
    NotLit    = 1
    Diffuse   = 2
    Gouraud   = 3
    ############### Not verified
    Bilinear  = 4
    Trilinear = 5

class TextureMode(IntEnum):
    AffineMapping        = 0
    PerspectiveCorrected = 1
    PerspectiveMapping   = 2
    Unknown              = 3 # <- Usually is this (maybe bilinear or mipmap)

class FaceType(IntEnum):
    Normal      = 0
    DoubleSided = 1
    Translucent = 2
    Unknown1    = 3   # inf_cage.3do
    Collision   = 4
    Unknown2    = 5   # anson.3do
    Unknown3    = 64  # 0x0040 in olv_statue_lefty.3do
    Unknown4    = 65  # 0x0041 in tem_bridge_20mholes.3do
    Unknown5    = 512 # 0x0200 in aet_dais_trio.3do

class MeshNodeType(IntEnum):
    Nothing    = 0x00000
    Torso      = 0x00001
    LeftArm    = 0x00002
    RightArm   = 0x00004
    Head       = 0x00008
    Hip        = 0x00010
    LeftLeg    = 0x00020
    RightLeg   = 0x00040
    LeftHand   = 0x00080
    LeftHand2  = 0x00082
    RightHand  = 0x00100
    RightHand2 = 0x00104
    Vehicle    = 0x00400
    BackPart   = 0x00800
    FrontPart  = 0x01000
    BackWheel  = 0x00C00 #Vehicle + BackPart
    FrontWheel = 0x01400 #Vehicle + FrontWheel


class MeshFace:
    def __init__(self):
        self.material_idx: int      = -1
        self.t: FaceType            = FaceType.Normal
        self.geo_mode: GeometryMode = GeometryMode.NotDrawn
        self.light_mode: LightMode  = LightMode.FullyLit
        self.tex_mode: TextureMode  = TextureMode.AffineMapping

        self.c: Vector4f    = (0.000000, 0.000000, 0.000000, 0.000000) # RGBA color
        self.vi: List[int]  = []  # List of indexes to the mesh list of vertices (vertex idx)
        self.tvi: List[int] = []  # List of indexes to the mesh list of texture vertices (tex vertex idx)
        self.n: Vector3f    = (0.000000, 0.000000, 0.000000) # face normal(x, y, z)

    @property
    def materialIdx(self) -> int:
        return self.material_idx

    @materialIdx.setter
    def materialIdx(self, idx: int):
        self.material_idx = idx

    @property
    def type(self) -> FaceType:
        return self.t

    @type.setter
    def type(self, type: FaceType):
        self.t = type

    @property
    def geometryMode(self) -> GeometryMode:
        return self.geo_mode

    @geometryMode.setter
    def geometryMode(self, mode: GeometryMode):
        self.geo_mode = mode

    @property
    def lightMode(self) -> LightMode:
        return self.light_mode

    @lightMode.setter
    def lightMode(self, mode: LightMode):
        self.light_mode = mode

    @property
    def textureMode(self) -> TextureMode:
        return self.tex_mode

    @textureMode.setter
    def textureMode(self, mode: TextureMode):
        self.tex_mode = mode

    @property
    def color(self) -> Vector4f:
        return self.c

    @color.setter
    def color(self, color: Vector4f):
        self.c = color

    @property
    def vertexIdxs(self) -> List[int]:
        return self.vi

    @vertexIdxs.setter
    def vertexIdxs(self, idxs: List[int]):
        self.vi = idxs

    @property
    def texVertexIdxs(self) -> List[int]:
        return self.tvi

    @texVertexIdxs.setter
    def texVertexIdxs(self, idxs: List[int]):
        self.tvi = idxs

    @property
    def normal(self) -> Vector3f:
        return self.n

    @normal.setter
    def normal(self, normal: Vector3f):
        self.n = normal


class ModelMesh:
    def __init__(self, idx: int = 0, name: str =""):
        self.i: int                 = idx
        self.mesh_name: str         = name
        self.mesh_radius: float     = 0.0
        self.geo_mode: GeometryMode = GeometryMode.NotDrawn
        self.light_mode: LightMode  = LightMode.FullyLit
        self.tex_mode: TextureMode  = TextureMode.AffineMapping

        self.v:  List[Vector3f] = [] # vertices
        self.vc: List[Vector4f] = [] # vertex colors
        self.vn: List[Vector3f] = [] # vertex normals
        self.tv: List[Vector2f] = [] # texture vertices

        self.face_list: List[MeshFace] = []

    @property
    def idx(self) -> int:
        return self.i

    @idx.setter
    def idx(self, idx: int):
        self.i = idx

    @property
    def name(self) -> str:
        return self.mesh_name

    @name.setter
    def name(self, name: str):
        self.mesh_name = name

    @property
    def radius(self) -> float:
        return self.mesh_radius

    @radius.setter
    def radius(self, radius: float):
        self.mesh_radius = radius

    @property
    def geometryMode(self) -> GeometryMode:
        return self.geo_mode

    @geometryMode.setter
    def geometryMode(self, mode: GeometryMode):
        self.geo_mode = mode

    @property
    def lightMode(self) -> LightMode:
        return self.light_mode

    @lightMode.setter
    def lightMode(self, mode: LightMode):
        self.light_mode = mode

    @property
    def textureMode(self) -> TextureMode:
        return self.tex_mode

    @textureMode.setter
    def textureMode(self, mode: TextureMode):
        self.tex_mode = mode

    @property
    def vertices(self) -> List[Vector3f]:
        return self.v

    @vertices.setter
    def vertices(self, vertices: List[Vector3f]):
        self.v = vertices

    @property
    def verticesColor(self) -> List[Vector4f]:
        return self.vc

    @verticesColor.setter
    def verticesColor(self, colors: List[Vector4f]):
        self.vc = colors

    @property
    def normals(self) -> List[Vector3f]:
        return self.vn

    @normals.setter
    def normals(self, normals: List[Vector3f]):
        self.vn = normals

    @property
    def textureVertices(self) -> List[Vector2f]:
        return self.tv

    @textureVertices.setter
    def textureVertices(self, texVert: List[Vector2f]):
        self.tv = texVert

    @property
    def faces(self) -> List[MeshFace]:
        return self.face_list

    @faces.setter
    def faces(self, faces: List[MeshFace]):
        self.face_list = faces


class ModelGeoSet:
    def __init__(self):
        self.mesh_list: List[ModelMesh] = []

    @property
    def meshes(self) -> List[ModelMesh]:
        return self.mesh_list

    @meshes.setter
    def meshes(self, meshes: List[ModelMesh]):
        self.mesh_list = meshes



class MeshHierarchyNode:
    def __init__(self, name =""):
        self.f: int             = 0x0000
        self.t: MeshNodeType    = MeshNodeType.Nothing
        self.n: str             = name
        self.mesh_i: int        = -1
        self.parent_i: int      = -1
        self.first_child_i: int = -1
        self.sibling_i: int     = -1
        self.num_children: int  = -1

        self.pos: Vector3f = [] # x,y,z
        self.rot: Vector3f = [] # pitch, yaw, roll:
        self.piv: Vector3f = [] # pivotx, pivoty, pivotz

    @property
    def flags(self) -> int:
        return self.f

    @flags.setter
    def flags(self, flags: int):
        self.f = flags

    @property
    def type(self) -> MeshNodeType:
        return self.t

    @type.setter
    def type(self, type: MeshNodeType):
        self.t = type

    @property
    def name(self) -> str:
        return self.n

    @name.setter
    def name(self, name: str):
        self.n = name

    @property
    def meshIdx(self) -> int:
        return self.mesh_i

    @meshIdx.setter
    def meshIdx(self, idx: int):
        self.mesh_i = idx

    @property
    def parentIdx(self) -> int:
        return self.parent_i

    @parentIdx.setter
    def parentIdx(self, idx: int):
        self.parent_i = idx

    @property
    def firstChildIdx(self) -> int:
        return self.first_child_i

    @firstChildIdx.setter
    def firstChildIdx(self, idx: int):
        self.first_child_i = idx

    @property
    def siblingIdx(self) -> int:
        return self.sibling_i

    @siblingIdx.setter
    def siblingIdx(self, idx: int):
        self.sibling_i = idx

    @property
    def numChildren(self) -> int:
        return self.num_children

    @numChildren.setter
    def numChildren(self, num: int):
        self.num_children = num

    @property
    def position(self) -> Vector3f:
        return self.pos

    @position.setter
    def position(self, pos: Vector3f):
        self.pos = pos

    @property
    def rotation(self) -> Vector3f:
        return self.rot

    @rotation.setter
    def rotation(self, rot: Vector3f):
        self.rot = rot

    @property
    def pivot(self) -> Vector3f:
        return self.piv

    @pivot.setter
    def pivot(self, piv: Vector3f):
        self.piv = piv



class Model:
    def __init__(self, name: str = ""):
        self.model_name: str          = name
        self.material_list: List[str] = []
        self.col_radius: float        = 0.0
        self.insert_offset: Vector3f  = [] # x,y, z

        self.geoset_list: List[ModelGeoSet]           = []
        self.hierarchy_nodes: List[MeshHierarchyNode] = []

    @property
    def name(self) -> str:
        return self.model_name

    @name.setter
    def name(self, name: str):
        self.model_name = name

    @property
    def materials(self) -> [str]:
        return self.material_list

    @materials.setter
    def materials(self, materials: [str]):
        self.material_list = materials

    @property
    def radius(self) -> float :
        return self.col_radius

    @radius.setter
    def radius(self, radius: float):
        self.col_radius = radius

    @property
    def insertOffset(self) -> Vector3f:
        return self.insert_offset

    @insertOffset.setter
    def insertOffset(self, offset: Vector3f):
        self.insert_offset = offset

    @property
    def geosets(self) -> List[ModelGeoSet]:
        return self.geoset_list

    @geosets.setter
    def geosets(self, geosets: List[ModelGeoSet]):
        self.geoset_list = geosets

    @property
    def hierarchyNodes(self) -> List[MeshHierarchyNode]:
        return self.hierarchy_nodes

    @hierarchyNodes.setter
    def hierarchyNodes(self, nodes: List[MeshHierarchyNode]):
        self.hierarchy_nodes = nodes
