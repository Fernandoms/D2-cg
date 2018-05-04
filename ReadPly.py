from Mesh import Mesh, Vertex, Face


def parse_ply(fname):
    m = Mesh()
    isHeader = True
    countVertex = 0
    countFaces = 0
    for line in open(fname, 'r'):
        line = line.rstrip()
        if "end_header" in line:
            isHeader = False
            continue
        if isHeader:
            if "element" in line:
                if "vertex" in line:
                    m.setNumVertices(int(line.split(" ")[-1]))
                elif "face" in line:
                    m.setNumFaces(int(line.split(" ")[-1]))
        else:
            if countVertex < m.numVertices:
                v = Vertex()
                aux = line.split(" ")
                v.set_x(float(aux[0]))
                v.set_y(float(aux[1]))
                v.set_z(float(aux[2]))
                m.addVertex(v)
                countVertex += 1
            elif countFaces < m.numFaces:
                face = Face()
                aux = line.split(" ")
                aux.pop(0)
                aux = list(map(int, aux))
                face.set(aux)
                m.addFace(face)
                countFaces += 1

    return m


if __name__ == "__main__":
    m = parse_ply('cow.ply')