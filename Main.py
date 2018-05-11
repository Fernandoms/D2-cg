import ReadPly
from Mesh import Materials
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

global mesh
global meshes
g_width = 640
g_height = 480
fullScreen = False
isWireframe = False
materials = Materials()

scaleFactor = 1.30
rotateFactor = 0.05
translateFactor = 0.05
rotationX = 0
rotationY = 0
dist = 4.0
last_x = 0.0
last_y = 0.0

file_showing = 0
files = ["cow", "budda", "dragon", "bunny", "snowman"]


def change_title():
    glutSetWindowTitle(files[file_showing] + ' - ' + str(mesh.numFaces) + ' Triangulos')


def doMouse(*args):
    global dist, last_y, last_x
    button = args[0]
    state = args[1]
    x = args[2]
    y = args[3]
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        last_x = x
        last_y = y
    if button == 3:
        if dist > 0.1:
            dist = dist - 0.1
            doRedraw()
    if button == 4:
        if dist < 20:
            dist = dist + 0.1
            doRedraw()


def doMotion(*args):
    global last_x, last_y, rotationY, rotationX
    x = args[0]
    y = args[1]

    rotationY = rotationY + float(y - last_y)
    rotationX = rotationX + float(x - last_x)
    last_x = x
    last_y = y

    doRedraw()


def doKeyboard(*args):
    global mesh, dist, fullScreen, isWireframe
    global file_showing
    if args[0] == b'f':
        fullScreen = not fullScreen
        if fullScreen:
            glutFullScreen()
        else:
            glutReshapeWindow(800, 450)
            glutInitWindowPosition(100, 100)
    if args[0] == b'w':
        isWireframe = not isWireframe

    # doRedraw()


def doSpecial(*args):
    global file_showing, dist, mesh
    if args[0] == GLUT_KEY_LEFT:
        file_showing = (file_showing - 1) % 5
        mesh = meshes[file_showing]
        dist = mesh.dist()
    if args[0] == GLUT_KEY_RIGHT:
        file_showing = (file_showing + 1) % 5
        mesh = meshes[file_showing]
        dist = mesh.dist()

    doRedraw()


# Called by glutMainLoop() when window is resized


def doReshape(width, height):
    global g_width, g_height
    g_width = width
    g_height = height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, width, height)
    gluPerspective(100, ((float)(width)) / height, 1, 20)

    doCamera()


def doCamera():
    global dist
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(100, (float(g_width)) / g_height, .1, 200)
    x, y = mesh.get_center()
    gluLookAt(x, y, dist, x, y, 0.0, 0.0, 1.0, 0.0)

    # Set up light
    glEnable(GL_LIGHTING)
    BRIGHT4f = (1.0, 1.0, 1.0, 1.0)  # Color for Bright light
    glLightfv(GL_LIGHT0, GL_AMBIENT, BRIGHT4f)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, BRIGHT4f)
    glLightfv(GL_LIGHT0, GL_POSITION, (x, y, dist, 0))
    glEnable(GL_LIGHT0)


# Called by glutMainLoop() when screen needs to be redrawn


def doRedraw():
    doCamera()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMaterial(GL_FRONT, GL_AMBIENT, materials.component_materials[file_showing].ambient)
    glMaterial(GL_FRONT, GL_DIFFUSE, materials.component_materials[file_showing].diffuse)
    glMaterial(GL_FRONT, GL_SPECULAR, materials.component_materials[file_showing].specular)
    glMaterial(GL_FRONT, GL_SHININESS, materials.component_materials[file_showing].shininess)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    glRotatef(rotationY, 1.0, 0.0, 0.0)
    glRotatef(rotationX, 0.0, 1.0, 0.0)

    mesh.draw(isWireframe)
    change_title()
    glutSwapBuffers()  # Draws the new image to the screen if using double buffers


def readPlys():
    global meshes
    meshes = []
    for i in range(0, 5):
        meshes.append(ReadPly.parse_ply(files[i] + ".ply"))

    return meshes


if __name__ == '__main__':
    meshes = readPlys()
    mesh = meshes[file_showing]

    # Basic initialization - the same for most apps
    glutInit([])
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(g_width, g_height)
    glutCreateWindow("Simple OpenGL Renderer")
    glClearColor(0.1, 0.1, 0.2, 0.0)  # Color to apply for glClear()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    change_title()
    # Set up light
    glEnable(GL_LIGHTING)
    BRIGHT4f = (1.0, 1.0, 1.0, 1.0)  # Color for Bright light
    glLightfv(GL_LIGHT0, GL_AMBIENT, BRIGHT4f)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, BRIGHT4f)
    glLightfv(GL_LIGHT0, GL_POSITION, (10, 10, 10, 0))
    glEnable(GL_LIGHT0)

    # Callback functions for loop
    glutDisplayFunc(doRedraw)  # Runs when the screen must be redrawn
    # glutIdleFunc(doIdle)  # Runs in a loop when the screen is not redrawn
    glutReshapeFunc(doReshape)  # Runs when the window is resized
    glutSpecialFunc(doSpecial)  # Runs when directional key is pressed
    glutKeyboardFunc(doKeyboard)  # Runs when key is pressed
    glutMouseFunc(doMouse)
    glutMotionFunc(doMotion)

    # Runs the GUI - never exits
    # Repeatedly calls doRedraw(), doIdle(), & doReshape()
    glutMainLoop()
