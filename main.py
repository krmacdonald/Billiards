
import pygame
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image
import utils
import camera

FLOOR_WIDTH = 20
FLOOR_LENGTH = 20
WALL_HEIGHT = 10
WALL_LENGTH = 10
CEILING_WIDTH = FLOOR_WIDTH
CEILING_LENGTH = FLOOR_LENGTH
FPS = 30.0

ceiling_name = "BilliardTable/textures/ceiling.png"
wall_name = "BilliardTable/textures/wall.png"
ceiling_tex_name = None
wall_tex_name = None

running = True
clock = 0
animate = 0
window_dimensions = (900, 600)

CAM_ANGLE = 60.0
CAM_NEAR = 0.01
CAM_FAR = 500.0
INITIAL_EYE = utils.Point(0, 3, 0)
INITIAL_LOOK_ANGLE = 45
camera = camera.Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR, INITIAL_EYE, INITIAL_LOOK_ANGLE)

def main():
    init()
    main_loop()
    return


def init():
    global ceiling_tex_name, wall_tex_name, clock
    pygame.init()
    screen = pygame.display.set_mode(window_dimensions, pygame.DOUBLEBUF|pygame.OPENGL)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(300, 50)  # Key repeat rate
    running = True
    clock = pygame.time.Clock()

    textArr = glGenTextures(2)  # Texture names for all three textures to create
    ceiling_tex_name = textArr[0]
    wall_tex_name = textArr[1]
    createTexture(ceiling_tex_name, ceiling_name)
    createTexture(wall_tex_name, wall_name)

def keyboard(event):
    global running, camera
    key = event.key
    if(key == 27):
        running = False

def main_loop():
    global running, clock, animate
    while running:
        display()

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

def display():
    width = window_dimensions[0]
    height = window_dimensions[1]

    glViewport(0, 0, width, height)
    camera.setProjection()
    glClearColor(0, 0, 0, 0)

    glFlush()
    
    drawScene()
    glFlush()


def drawScene():
    glEnable(GL_LIGHTING)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    
    camera.placeCamera()


    #createWalls()

    glPushMatrix()
    glRotate(90, 90, 0, 0)
    glTranslate(0, 3, 0)
    createCeiling()
    glPopMatrix()
    #createFloor()


#TODO create four walls around floor
def createWalls():
    pass

#TODO Create checkerboard floor
def createFloor(width, length, texture1, texture2):
    glBindTexture(GL_TEXTURE_2D, texture1)


#TODO Create any textured ceiling
def createCeiling():
    draw_plane(5, 5, ceiling_tex_name)

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

    x1 = width/2.0
    y1 = height
    x2 = -x1
    y2 = 0

    glTexCoord2f(0, 0)
    glVertex3f(x2, y2, 0)
    glTexCoord2f(4, 0)
    glVertex3f(x1, y2, 0)
    glTexCoord2f(4, 4)
    glVertex3f(x1, y1, 0)
    glTexCoord2f(0, 4)
    glVertex3f(x2, y1, 0)

    glEnd()
    glDisable(GL_TEXTURE_2D)

    


if __name__ == "__main__" : main()