from OpenGL.GL import *
import math

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