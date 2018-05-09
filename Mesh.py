from OpenGL.GL import *
import math

materials = [
    [  # Silver
        (0.192250, 0.192250, 0.192250, 1.000000),  # ambient
        (0.507540, 0.507540, 0.507540, 1.000000),  # diffuse
        (0.508273, 0.508273, 0.508273, 1.000000),  # specular
        51.200001  # shininess
    ],
    [  # Gold
        (0.247250, 0.199500, 0.074500, 1.000000),  # ambient
        (0.751640, 0.606480, 0.226480, 1.000000),  # diffuse
        (0.628281, 0.555802, 0.366065, 1.000000),  # specular
        51.200001  # shininess
    ],
    [  # Pewter
        (0.105882, 0.058824, 0.113725, 1.000000),  # ambient
        (0.427451, 0.470588, 0.541176, 1.000000),  # diffuse
        (0.333333, 0.333333, 0.521569, 1.000000),  # specular
        9.846150  # shininess
    ],
    [  # Emerald
        (0.021500, 0.174500, 0.021500, 0.550000),  # ambient
        (0.075680, 0.614240, 0.075680, 0.550000),  # diffuse
        (0.633000, 0.727811, 0.633000, 0.550000),  # specular
        76.800003  # shininess
    ],
    [  # Black Plastic
        (0.053750, 0.050000, 0.066250, 0.820000),  # ambient
        (0.182750, 0.170000, 0.225250, 0.820000),  # diffuse
        (0.332741, 0.328634, 0.346435, 0.820000),  # specular
        38.400002  # shininess
    ]
]


class Vertex(object):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_z(self, z):
        self.z = z

    def get_z(self):
        return self.z

    def coords(self):
        return self.x, self.y, self.z


class Face(object):
    def __init__(self):
        self._vertices = []

    def set(self, l):
        self._vertices = l

    def vertices(self):
        return self._vertices

    def vertex(self, i):
        return self._vertices[i]


class Mesh(object):
    primitiva = [GL_TRIANGLES, GL_LINE_LOOP]

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.numVertices = 0
        self.numFaces = 0
        self.max_x = 0.0
        self.min_x = 0.0
        self.min_y = 0.0
        self.max_y = 0.0

    def addVertex(self, v):
        self.vertices.append(v)

    def getVertex(self, vi):
        return self.vertices[vi]

    def addFace(self, f):
        self.faces.append(f)

    def setNumVertices(self, n):
        self.numVertices = n

    def setNumFaces(self, f):
        self.numFaces = f

    def check_x(self, x):
        if self.max_x < x:
            self.max_x = x
        if self.min_x > x:
            self.min_x = x

    def check_y(self, y):
        if self.max_y < y:
            self.max_y = y
        if self.min_y > y:
            self.min_y = y

    def get_center(self):
        x_center = (self.min_x + self.max_x) / 2
        y_center = (self.min_y + self.max_y) / 2

        return x_center, y_center

    def dist(self):
        if (abs(self.min_x) + abs(self.max_x)) > (abs(self.min_y) + abs(self.max_y)):
            return abs(self.min_x) + abs(self.max_x)
        else:
            return abs(self.min_y) + abs(self.max_y)

    def draw(self, isWireframe=False):
        mode = None
        for face in self.faces:
            numvertices = len(face.vertices())
            if isWireframe:
                glBegin(GL_LINE_LOOP)
                mode = GL_LINE_LOOP
            else:
                if numvertices == 3 and mode != GL_TRIANGLES:
                    if mode:
                        glEnd()
                    glBegin(GL_TRIANGLES)
                    mode = GL_TRIANGLES
                elif numvertices == 4 and mode != GL_QUADS:
                    if mode:
                        glEnd()
                    glBegin(GL_QUADS)
                    mode = GL_QUADS
                elif numvertices > 4:
                    if mode:
                        glEnd()
                    glBegin(GL_POLYGON)
                    mode = GL_POLYGON
                elif numvertices < 3:
                    raise RuntimeError('Face has less then 3 vertices')
            vn = self.calculateNormal(face)
            glNormal3d(vn.x, vn.y, vn.z)
            for vertex in [self.getVertex(i) for i in face.vertices()]:
                glVertex3f(*(vertex.coords()))
            if mode == GL_POLYGON or GL_LINE_LOOP:
                glEnd()
                mode = None
        if mode:
            glEnd()

    def calculateNormal(self, face):
        v1 = Vertex()
        v2 = Vertex()
        vn = Vertex()

        a1 = self.getVertex(face.vertex(0))
        a2 = self.getVertex(face.vertex(1))
        a3 = self.getVertex(face.vertex(2))

        v1.set_x(a2.x - a1.x)
        v1.set_y(a2.y - a1.y)
        v1.set_z(a2.z - a1.z)

        v2.set_x(a3.x - a1.x)
        v2.set_y(a3.y - a1.y)
        v2.set_z(a3.z - a1.z)

        vn.set_x((v1.y * v2.z) - (v1.z * v2.y))
        vn.set_y((v1.z * v2.x) - (v1.x * v2.z))
        vn.set_z((v1.x * v2.y) - (v1.y * v2.x))

        len = math.sqrt(math.pow(vn.x, 2) + math.pow(vn.y, 2) + math.pow(vn.z, 2))

        vn.set_x(vn.x / len)
        vn.set_y(vn.y / len)
        vn.set_z(vn.z / len)

        return vn


class Material:
    def __init__(self, *args):
        self.ambient = args[0][0]
        self.diffuse = args[0][1]
        self.specular = args[0][2]
        self.shininess = args[0][3]

class Materials:
    def __init__(self):
        self.component_materials = Materials.set_materials()

    @staticmethod
    def set_materials():
        aux = []
        for i in materials:
            aux.append(Material(i))
        return aux


if __name__ == '__main__':
    m = Materials()
    print(m.component_materials)

