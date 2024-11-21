import math
import pygame
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image
import utils
import camera

FLOOR_WIDTH = 30
FLOOR_LENGTH = 30
WALL_HEIGHT = 10
WALL_LENGTH = 30
CEILING_WIDTH = FLOOR_WIDTH
CEILING_LENGTH = FLOOR_LENGTH
X_BOUND = 29
Y_BOUND = None
Z_BOUND = 29
FLASH_ANGLE = 0
FPS = 30.0

ceiling_name = "textures/ceiling.jpeg"
wall_name = "textures/wall.jpeg"
pool_name = "textures/poolfelt.jpg"

ceiling_tex_name = None
wall_tex_name = None
pool_tex_name = None
floor_tex_name = None

running = True
clock = 0
animate = 0
window_dimensions = (900, 600)

CAM_ANGLE = 60.0
CAM_NEAR = 0.01
CAM_FAR = 500.0
INITIAL_EYE = utils.Point(2, 3, 15)
INITIAL_LOOK_ANGLE = 45
camera = camera.Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR, INITIAL_EYE, INITIAL_LOOK_ANGLE)

def main():
    init()
    main_loop()
    return


def init():
    global ceiling_tex_name, wall_tex_name, clock, floor_tex_name, pool_tex_name
    pygame.init()
    screen = pygame.display.set_mode(window_dimensions, pygame.DOUBLEBUF|pygame.OPENGL)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(300, 50)  # Key repeat rate
    running = True
    clock = pygame.time.Clock()

    textArr = glGenTextures(3)  # Texture names for all three textures to create
    ceiling_tex_name = textArr[0]
    wall_tex_name = textArr[1]
    pool_tex_name = textArr[2]
    createTexture(ceiling_tex_name, ceiling_name)
    createTexture(wall_tex_name, wall_name)
    createTexture(pool_tex_name, pool_name)
    floor_tex_name = generate_checkerboard_texture(9, 9, 30, [[0, 0, 0, 1], [255,255,255, 1]])

def keyboard(event):
    global running, camera
    key = event.key
    if(key == 27):
        running = False
    elif(key == ord("a")):
        camera.turn(3)
    elif(key == ord("d")):
        camera.turn(-3)
    elif(key == ord("s")):
        camera.slide(0, 0, 1)
    elif(key == ord("w")):
        camera.slide(0, 0, -1)
    elif(key == ord("q")):
        camera.slide(0, 1, 0)
    elif(key == ord("e")):
        camera.slide(0, -1, 0)
    elif(key == ord("i")):
        camera.upAngle += 3
    elif(key == ord("k")):
        camera.upAngle -= 3
    elif(key == ord("h")):
        print(camera.eye.x)
        print(camera.eye.y)
        print(camera.eye.z)

    if(camera.eye.z < 0):
        camera.eye.z = 0
    elif(camera.eye.z > Z_BOUND):
        camera.eye.z = Z_BOUND

    if(camera.eye.x < -X_BOUND/2.0):
        camera.eye.x = -X_BOUND/2.0
    elif(camera.eye.x > X_BOUND/2.0):
        camera.eye.x = X_BOUND/2.0

def main_loop():
    global running, clock, animate
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keyboard(event)

        display()

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

def display():
    width = window_dimensions[0]
    height = window_dimensions[1]

    glViewport(0, 0, width, height)
    camera.setProjection()
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glFlush()
    
    drawScene()
    glFlush()


def drawScene():
    glEnable(GL_LIGHTING)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    
    camera.placeCamera()

    flashlight(GL_LIGHT0)

    createWalls()

    glPushMatrix()
    glTranslate(0, 10, 0)
    glRotate(90, 90, 0, 0)
    createCeiling()
    glPopMatrix()
    createFloor()

def flashlight(light):
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    posArr = [camera.eye.x, camera.eye.y, camera.eye.z, 3]
    light_position = posArr
    rad = math.radians(FLASH_ANGLE)
    light_direction = [ math.sin(rad), 0.0, -math.cos(rad), 0.0]
    light_ambient = [ 1.0, 1.0, 1.0, 1.0 ]
    light_diffuse = [ 1.0, 1.0, 1.0, 1.0 ]
    light_specular = [ 0.0, 1.0, 1.0, 1.0 ]

    # For Light 0, set position, ambient, diffuse, and specular values
    glLightfv(light, GL_POSITION, light_position)
    glLightfv(light, GL_AMBIENT, light_ambient)
    glLightfv(light, GL_DIFFUSE, light_diffuse)
    glLightfv(light, GL_SPECULAR, light_specular)

    glLightfv(light, GL_SPOT_DIRECTION, light_direction)
    glLightf(light, GL_SPOT_CUTOFF, 30.0)
    glLightf(light, GL_SPOT_EXPONENT, 5.0)

    # Distance attenuation
    glLightf(light, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(light, GL_LINEAR_ATTENUATION, 0.02)
    glLightf(light, GL_QUADRATIC_ATTENUATION, 0.005)
    glEnable(light)
    glPopMatrix()

#Creates four walls around the floor using the constants defined at the top
def createWalls():
    glPushMatrix()
    draw_plane(WALL_LENGTH, WALL_HEIGHT, wall_tex_name)
    glRotate(90, 0, 90, 0)
    glTranslate(-WALL_LENGTH/2.0, 0, -WALL_LENGTH/2.0)
    draw_plane(WALL_LENGTH, WALL_HEIGHT, wall_tex_name)
    glTranslate(0, 0, WALL_LENGTH)
    draw_plane(WALL_LENGTH, WALL_HEIGHT, wall_tex_name)
    glRotate(90, 0, 90, 0)
    glTranslate(WALL_LENGTH/2.0, 0, -WALL_LENGTH/2.0)
    draw_plane(WALL_LENGTH, WALL_HEIGHT, wall_tex_name)
    glPopMatrix()

def createTable():
    gluQuadricNormals


#TODO Create checkerboard floor
def createFloor():
    glPushMatrix()
    glRotate(90, 90, 0, 0)
    draw_plane(FLOOR_LENGTH, FLOOR_WIDTH, floor_tex_name)
    glPopMatrix()

def generate_checkerboard_texture(nrows, ncols, block_size, block_colors):
    color_size = len(block_colors[0])

    texture = [0]*(nrows*ncols*block_size*block_size*color_size)
    idx = 0
    for i in range(nrows):
        for ib in range(block_size):
            for j in range(ncols):
                color = block_colors[(i+j)%len(block_colors)]
                for jb in range(block_size):
                    for c in color:
                        texture[idx] = c
                        idx += 1

    # Generate a "name" for the texture.  
    # Bind this texture as current active texture
    # and sets the parameters for this texture.
    texture_array = [ 0 ] 
    glGenTextures(1, texture_array)
    texture_name = texture_array[0]
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 ncols*block_size, 
                 nrows*block_size, 
                 0, GL_RGBA, 
                 GL_UNSIGNED_BYTE, texture)
    return texture_name


#TODO Create any textured ceiling
def createCeiling():
    draw_plane(CEILING_WIDTH, CEILING_LENGTH, ceiling_tex_name)

#Generates the texture based on the provided filename and the desired storage
def createTexture(tName, fName):
    img = Image.open(fName)
    x = img.size[0]
    y = img.size[1]
    text = img.tobytes("raw")
    glBindTexture(GL_TEXTURE_2D, tName)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, x, y, 0, GL_RGB, GL_UNSIGNED_BYTE, text)


#Creates a plane based on the provided width, height, and texture
def draw_plane(width, height, texture, divisions_x=10, divisions_y=10):
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)

    step_x = width / divisions_x
    step_y = height / divisions_y
    tex_step_x = 4.0 / divisions_x
    tex_step_y = 4.0 / divisions_y

    for i in range(divisions_x):
        for j in range(divisions_y):
            x1 = -width / 2.0 + i * step_x
            x2 = x1 + step_x
            y1 = j * step_y
            y2 = y1 + step_y

            u1 = i * tex_step_x
            u2 = u1 + tex_step_x
            v1 = j * tex_step_y
            v2 = v1 + tex_step_y

            glTexCoord2f(u1, v1)
            glVertex3f(x1, y1, 0)
            glTexCoord2f(u2, v1)
            glVertex3f(x2, y1, 0)
            glTexCoord2f(u2, v2)
            glVertex3f(x2, y2, 0)
            glTexCoord2f(u1, v2)
            glVertex3f(x1, y2, 0)

    glEnd()
    glDisable(GL_TEXTURE_2D)


    


if __name__ == "__main__" : main()