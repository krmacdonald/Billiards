
import pygame
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import *
import camera

FLOOR_WIDTH = 20
FLOOR_LENGTH = 20
WALL_HEIGHT = 10
WALL_LENGTH = 10
CEILING_WIDTH = FLOOR_WIDTH
CEILING_LENGTH = FLOOR_LENGTH

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

def main_loop():
    global running, clock, animate
    while running:
        createWalls()
        createCeiling()
        createFloor()
    pass

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

def draw_plane(width, height, texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


    glEnable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)
    


if __name__ == "__main__" : main()