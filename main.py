
import pygame
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image
import camera

FLOOR_WIDTH = 20
FLOOR_LENGTH = 20
WALL_HEIGHT = 10
WALL_LENGTH = 10
CEILING_WIDTH = FLOOR_WIDTH
CEILING_LENGTH = FLOOR_LENGTH

ceiling_name = "ceiling.png"
wall_name = "wall.png"
ceiling_tex_name = None
wall_tex_name = None

running = True
clock = 0
animate = 0
window_dimensions = (900, 600)

def main():
    init()
    main_loop()


def init():
    pygame.init()
    screen = pygame.display.set_mode(window_dimensions, pygame.DOUBLEBUF|pygame.OPENGL)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(300, 50)  # Key repeat rate
    running = True
    textArr = glGenTextures(2)  # Texture names for all three textures to create
    ceiling_tex_name = textArr[0]
    wall_tex_name = textArr[1]
    createTexture(ceiling_tex_name, ceiling_name)
    createTexture(wall_tex_name, wall_name)

def main_loop():
    global running, clock, animate
    while running:
        createWalls()
        createCeiling()
        createFloor()
    pass

def display():
    width = window_dimensions[0]
    height = window_dimensions[1]

    glViewport(0, 0, width, height)
    camera.SetProjection()
    glClearColor(0, 0, 0, 0)

    glFlush()
    
    drawScene()
    glFlush()


def drawScene():
    glEnable(GL_LIGHTING)

    camera.placeCamera()


    createWalls()
    createCeiling()
    createFloor()


#TODO create four walls around floor
def createWalls():
    gluBeginSurface()
    
    gluEndSurface()

#TODO Create checkerboard floor
def createFloor(width, length, texture1, texture2):
    glBindTexture(GL_TEXTURE_2D, texture1)


#TODO Create any textured ceiling
def createCeiling():
    pass

def createTexture(tName, fName):
    img = Image.open(fName)
    x = img.size[0]
    y = img.size[1]
    text = img.tobytes("raw")
    glBindTexture(GL_TEXTURE_2D, tName)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, x, y, 0, GL_RGB, GL_UNSIGNED_BYTE, text)


def draw_plane(width, height, texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


    glEnable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)
    


if __name__ == "__main__" : main()