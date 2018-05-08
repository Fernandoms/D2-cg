import ReadPly
import Matrix as matrices

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

global mesh
global meshes
g_width = 640
g_height = 480

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


# Gets called by glutMainLoop() many times per second
def doIdle():
    pass  # Remove if we actually use this function


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
    global mesh
    global file_showing
    global cameraMatrix
    if args[0] == b'+':
        cameraMatrix = cameraMatrix * matrices.scale(1 / scaleFactor, 1 / scaleFactor, 1 / scaleFactor)
    elif args[0] == b'-':
        cameraMatrix = cameraMatrix * matrices.scale(scaleFactor, scaleFactor, scaleFactor)
    elif args[0] == b'd':
        file_showing = (file_showing + 1) % 5
        mesh = meshes[file_showing]
    elif args[0] == b'a':
        file_showing = (file_showing - 1) % 5
        mesh = meshes[file_showing]
    else:
        return
    doRedraw()


def doSpecial(*args):
    global cameraMatrix
    if glutGetModifiers() & GLUT_ACTIVE_SHIFT:
        if args[0] == GLUT_KEY_UP:
            cameraMatrix = cameraMatrix * matrices.translate(0, -translateFactor, 0)  # up
        if args[0] == GLUT_KEY_DOWN:
            cameraMatrix = cameraMatrix * matrices.translate(0, translateFactor, 0)  # down
        if args[0] == GLUT_KEY_LEFT:
            cameraMatrix = cameraMatrix * matrices.translate(translateFactor, 0, 0)  # left
        if args[0] == GLUT_KEY_RIGHT:
            cameraMatrix = cameraMatrix * matrices.translate(-translateFactor, 0, 0)  # right
    else:
        if args[0] == GLUT_KEY_UP:
            cameraMatrix = cameraMatrix * matrices.rotateX(-rotateFactor)  # up
        if args[0] == GLUT_KEY_DOWN:
            cameraMatrix = cameraMatrix * matrices.rotateX(rotateFactor)  # down
        if args[0] == GLUT_KEY_LEFT:
            cameraMatrix = cameraMatrix * matrices.rotateY(-rotateFactor)  # left
        if args[0] == GLUT_KEY_RIGHT:
            cameraMatrix = cameraMatrix * matrices.rotateY(rotateFactor)  # right
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


# Called by glutMainLoop() when screen needs to be redrawn
def doRedraw():
    doCamera()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (.25, .25, .25, 1.0))
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, .5))
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, (128.0,))
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    glRotatef(rotationY, 1.0, 0.0, 0.0)
    glRotatef(rotationX, 0.0, 1.0, 0.0)

    mesh.draw()
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

    # Set up two lights
    glEnable(GL_LIGHTING)
    BRIGHT4f = (1.0, 1.0, 1.0, 1.0)  # Color for Bright light
    glLightfv(GL_LIGHT0, GL_AMBIENT, BRIGHT4f)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, BRIGHT4f)
    glLightfv(GL_LIGHT0, GL_POSITION, (10, 10, 10, 0))
    glEnable(GL_LIGHT0)

    # Callback functions for loop
    glutDisplayFunc(doRedraw)  # Runs when the screen must be redrawn
    glutIdleFunc(doIdle)  # Runs in a loop when the screen is not redrawn
    glutReshapeFunc(doReshape)  # Runs when the window is resized
    glutSpecialFunc(doSpecial)  # Runs when directional key is pressed
    glutKeyboardFunc(doKeyboard)  # Runs when key is pressed
    glutMouseFunc(doMouse)
    glutMotionFunc(doMotion)

    # Runs the GUI - never exits
    # Repeatedly calls doRedraw(), doIdle(), & doReshape()
    glutMainLoop()
