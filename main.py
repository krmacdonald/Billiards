
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

def main():
    init()
    main_loop()


def init():
    pass

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

def draw_plane(width, height):
    pass

if __name__ == "__main__" : main()