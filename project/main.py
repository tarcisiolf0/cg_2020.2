from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import glm
import pygame

# tamanho da tela
WINDOW_WIDHT = 1000
WINDOW_HEIGHT = 1000

# camera
cameraPos = glm.vec3(0, 3.5, 30)
cameraFront = glm.vec3(0, 0, -1)
cameraUp = glm.vec3(0, 1, 0)
angle = 0

# mouse
old_mouse_x = 0
old_mouse_y = 0
angle_x = -1.57
angle_y = 1.57
mouse_speed = 0.1
mouse_sensitivity = 0.001

lamp_color = glm.vec3(10, 10, 10)


#textures
textures = {
    'brick': None,
    'ceramica': None,
    'guardaroupa': None,
    'ednaldo': None,
    'gavetas_comoda': None,
    'portas_comoda': None,
    'teto': None,
    'parede': None,
    'quadro1': None,
    'quadro2': None,
    'miro': None,
    'tela_notebook': None,
    'base_notebook': None,
    'porta1':None,
    'porta2': None,
    'wood': None,
    'teclado': None,
    'tomada1': None,
    'tomada2': None
}

fan_rotation = 0
door_angle = 0
window_angle = 0

half_width = WINDOW_WIDHT / 2
half_height = WINDOW_HEIGHT / 2


# Utilizadas
def draw_wall(x0, y0, z0, x1, y1, z1):
    glBegin(GL_QUADS)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y0, z1)
    glVertex3f(x1, y1, z1)
    glVertex3f(x0, y1, z0)
    glEnd()

def draw_textured_wall(x0, y0, z0, x1, y1, z1, texture):

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x0, y0, z0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x1, y0, z1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x1, y1, z1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x0, y1, z0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def draw_floor(x, y, z, width, length):
    glBegin(GL_QUADS)
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + length)
    glVertex3f(x + width, y, z + length)
    glVertex3f(x + width, y, z)
    glEnd()

def draw_textured_floor(x, y, z, width, length, texture):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, y, z + length)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x + width, y, z + length)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x + width, y, z)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def draw_block(x, y, z, width, length, height):
    draw_wall(x, y, z, x, y + height, z+length)
    draw_wall(x, y, z, x+width, y + height, z)
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    draw_floor(x, y, z, width, length)
    draw_floor(x, y+height, z, width, length)

def draw_texturized_block_right(x, y, z, width, length, height, texture):
    #left side
    draw_wall(x, y, z, x, y + height, z+length)
    #back side
    draw_wall(x, y, z, x+width, y + height, z)
    #front side
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    #down side
    draw_floor(x, y, z, width, length)
    #up side
    draw_floor(x, y+height, z, width, length)
    #right side
    # draw_wall(x+width, y, z, x + width, y + height, z + length)
    glColor3f(1, 1, 1)
    draw_textured_wall(x+width, y, z, x + width, y + height, z + length, texture)

def draw_texturized_block_front(x, y, z, width, length, height, texture):
    #left side
    draw_wall(x, y, z, x, y + height, z+length)
    #back side
    draw_wall(x, y, z, x+width, y + height, z)
    #right side
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    #down side
    draw_floor(x, y, z, width, length)
    #up side
    draw_floor(x, y+height, z, width, length)
    # front side
    glColor3f(1, 1, 1)
    draw_textured_wall(x, y, z+length, x + width, y + height, z + length, texture)

def draw_texturized_block_front_and_back(x, y, z, width, length, height, texture_front, texture_back):
    #left side
    draw_wall(x, y, z, x, y + height, z+length)
    #right side
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    #down side
    draw_floor(x, y, z, width, length)
    #up side
    draw_floor(x, y+height, z, width, length)
    # front side
    glColor3f(1, 1, 1)
    draw_textured_wall(x, y, z+length, x + width, y + height, z + length, texture_front)
    #back side
    draw_textured_wall(x, y, z, x+width, y + height, z, texture_back)

def draw_texturized_block_up(x, y, z, width, length, height, texture):
    #left side
    draw_wall(x, y, z, x, y + height, z+length)
    #back side
    draw_wall(x, y, z, x+width, y + height, z)
    #right side
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    #down side
    draw_floor(x, y, z, width, length)
    # front side
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    #up side
    glColor3f(1, 1, 1)
    draw_textured_floor(x, y+height, z, width, length, texture)
    # draw_floor(x, y+height, z, width, length)

def draw_colored_block(x, y, z, width, length, height, front_color, back_color, left_color, right_color, up_color, down_color):
    #left side
    glColor3f(left_color.x, left_color.y, left_color.z)
    draw_wall(x, y, z, x, y + height, z+length)
    #back side
    glColor3f(back_color.x, back_color.y, back_color.z)
    draw_wall(x, y, z, x+width, y + height, z)
    #right side
    glColor3f(right_color.x, right_color.y, right_color.z)
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    #front side
    glColor3f(front_color.x, front_color.y, front_color.z)
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    #down side
    glColor3f(down_color.x, down_color.y, down_color.z)
    draw_floor(x, y, z, width, length)
    #up side
    glColor3f(up_color.x, up_color.y, up_color.z)
    draw_floor(x, y+height, z, width, length)

def draw_colored_block_fixed(x, y, z, width, length, height):
    glColor3f(0.293, 0.211, 0.13)
    draw_wall(x, y, z, x, y + height, z+length)
    glColor3f(0.486, 0.293, 0)
    draw_wall(x, y, z, x+width, y + height, z)
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    glColor3f(0.36, 0.2, 0.09)
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    draw_floor(x, y, z, width, length)
    glColor3f(0.37, 0.15, 0.07)
    draw_floor(x, y+height, z, width, length)

def draw_cylinder(x, y, z, radius, height):
    px = 0
    pz = 0
    c_angle = 0
    angle_stepsize = 0.1

    #desenha cilindro
    glBegin(GL_QUAD_STRIP)
    c_angle = 0
    while c_angle < 2*glm.pi() + 1:
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y + height, z + pz)
        glVertex3f(x + px, y, z + pz)
        c_angle += angle_stepsize
    glEnd()

    #desenha tampa do cilindro
    glBegin(GL_POLYGON)
    c_angle = 0
    while c_angle < 2*glm.pi():
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y + height, z + pz)
        c_angle += angle_stepsize
    glEnd()

    #desenha fundo do cilindro
    glBegin(GL_POLYGON)
    c_angle = 0
    while c_angle < 2 * glm.pi():
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y, z + pz)
        c_angle += angle_stepsize
    glEnd()

    glPushMatrix()
    glTranslatef(x,y,z)
    #cama
    draw_colored_block(0.5, 0.4, 0.1, 4, 8, 0.5,
                       glm.vec3(0.8, 0.8, 0.8), glm.vec3(1, 1, 1),
                       glm.vec3(0.6, 0.6, 0.6), glm.vec3(1, 1, 1),
                       glm.vec3(1, 1, 1), glm.vec3(1, 1, 1))
    #colchão
    glColor3f(0.212, 0.205, 0.205)
    draw_block(0.5, 0.9, 0.1, 4, 8, 0.6)
    #pés da cama
    glColor3f(0.18, 0.16, 0.16)
    draw_cylinder(0.5+0.2, 0, 0.2, 0.1, 0.4)
    draw_cylinder(0.5+0.2, 0, 4, 0.1, 0.4)
    draw_cylinder(0.5+0.2, 0, 7.8, 0.1, 0.4)
    draw_cylinder(0.5+3.8, 0, 0.2, 0.1, 0.4)
    draw_cylinder(0.5+3.8, 0, 7.8, 0.1, 0.4)
    glPopMatrix()

def draw_wardrobe(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    draw_texturized_block_right(0, 0, 0, 2.5, 12, 5, textures['guardaroupa'])
    glPopMatrix()

"""
def draw_fan_table(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    #tampo
    draw_block(0, 1.5, 0, 3, 2, 0.1)
    #pé esquerdo trás
    draw_block(0, 0, 0, 0.3, 0.1, 1.5)
    draw_block(0, 0, 0, 0.1, 0.3, 1.5)
    #pé esquerdo frente
    glPushMatrix()
    glTranslatef(0, 0, 2)
    glRotatef(90, 0, 1, 0)
    draw_block(0, 0, 0, 0.3, 0.1, 1.5)
    draw_block(0, 0, 0, 0.1, 0.3, 1.5)
    glPopMatrix()
    #pé direito trás
    glPushMatrix()
    glTranslatef(3, 0, 0)
    glRotatef(270, 0, 1, 0)
    draw_block(0, 0, 0, 0.3, 0.1, 1.5)
    draw_block(0, 0, 0, 0.1, 0.3, 1.5)
    glPopMatrix()
    #pé direito frente
    glPushMatrix()
    glTranslatef(3, 0, 2)
    glRotatef(180, 0, 1, 0)
    draw_block(0, 0, 0, 0.3, 0.1, 1.5)
    draw_block(0, 0, 0, 0.1, 0.3, 1.5)
    glPopMatrix()

    glPopMatrix() # fim fan_table
"""

def draw_fan(x, y, z, rot):
    glPushMatrix() #begin fan
    glTranslatef(x, y, z)
    glColor3ub(100, 100, 100)
    draw_cylinder(0, 0, 0, 1, 0.2) # base

    glColor3ub(60, 60, 60)
    draw_cylinder(0, 0.2, 0, 0.2, 1.5) #haste

    glPushMatrix() # motor + helices
    glColor3ub(80, 80, 80)
    glTranslatef(0, 1.7, -2)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0, 1.7, 0, 0.4, 0.8) #motor
    glColor3ub(10, 10, 10)
    draw_cylinder(0, 2.5, 0, 0.05, 0.1)  # haste helices

    glRotatef(-rot, 0, 1, 0) #<<<<ISSO AQUI RODA O VENLILADOR
    glPushMatrix() #push helices
    glColor3ub(100, 100, 100)
    draw_cylinder(0, 2.6, 0, 0.3, 0.2)  # centro helices
    glColor3ub(130, 130, 130)
    glPushMatrix()
    glScalef(2, 1, 1)
    draw_cylinder(-0.45, 2.7, 0, 0.3, 0.03)# helice 1
    draw_cylinder(0.45, 2.7, 0, 0.3, 0.03)  # helice 2
    glPopMatrix()
    glScalef(1, 1, 2)
    draw_cylinder(0, 2.7, 0.45, 0.3, 0.03)  # helice 3
    draw_cylinder(0, 2.7, -0.45, 0.3, 0.03)   # helice 4
    glPopMatrix() #pop helices
    glutPostRedisplay()
    glPopMatrix() #pop motor
    # glutPostRedisplay()
    glPopMatrix() #end fan

def draw_table(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    # tampo
    draw_colored_block(0, 2, 0, 4, 2, 0.1,
                       glm.vec3(0.8, 0.8, 0.8), glm.vec3(1, 1, 1),
                       glm.vec3(0.6, 0.6, 0.6), glm.vec3(1, 1, 1),
                       glm.vec3(0.92, 0.92, 0.92), glm.vec3(1, 1, 1))
    #lateral esquerda
    draw_colored_block(0, 0, 0, 0.1, 2, 2,
                       glm.vec3(0.8, 0.8, 0.8), glm.vec3(1, 1, 1),
                       glm.vec3(0.6, 0.6, 0.6), glm.vec3(1, 1, 1),
                       glm.vec3(1, 1, 1), glm.vec3(1, 1, 1))
    #lateral direita
    draw_colored_block(3.9, 0, 0, 0.1, 2, 2,
                       glm.vec3(0.8, 0.8, 0.8), glm.vec3(1, 1, 1),
                       glm.vec3(0.6, 0.6, 0.6), glm.vec3(1, 1, 1),
                       glm.vec3(1, 1, 1), glm.vec3(1, 1, 1))
    #frente
    draw_colored_block(0.1, 1.8, 1.9, 3.8, 0.1, 0.2,
                       glm.vec3(0.8, 0.8, 0.8), glm.vec3(1, 1, 1),
                       glm.vec3(0.6, 0.6, 0.6), glm.vec3(1, 1, 1),
                       glm.vec3(1, 1, 1), glm.vec3(1, 1, 1))

    glPopMatrix()

def draw_chair(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    #assento
    draw_colored_block_fixed(0, 1, 0, 1.2, 1, 0.1)
    #pés
    draw_colored_block_fixed(0, 0, 0, 0.2, 0.2, 1)
    draw_colored_block_fixed(1, 0, 0, 0.2, 0.2, 1)
    draw_colored_block_fixed(0, 0, 0.8, 0.2, 0.2, 1)
    draw_colored_block_fixed(1, 0, 0.8, 0.2, 0.2, 1)
    #encosto
    draw_colored_block_fixed(0, 1.1, 0.9, 1.2, 0.1, 1.5)
    glPopMatrix()

def draw_lamp(x, y, z, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(100, 100, 100)
    draw_cylinder(0, 0, 0, 0.3, 0.1) # base

    glColor3ub(60, 60, 60)
    draw_cylinder(0, 0.1, 0, 0.05, 0.6) #haste

    glPushMatrix()
    glColor3ub(80, 80, 80)
    glTranslatef(0, 0.8, -1.85)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0, 1.7, 0, 0.15, 0.4) # corpo da lampada
    glColor3f(color.x/255, color.y/255, color.z/255)
    draw_cylinder(0, 2.1, 0, 0.1, 0.01)  # frente da lampada
    glPopMatrix()

    glPopMatrix()


# Feitas
def draw_table1(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    #tampo
    draw_block(0, 2, 0, 3, 3, 0.1)
    #pé esquerdo trás
    draw_block(0, 0, 0, 0.3, 0.1, 2)
    draw_block(0, 0, 0, 0.1, 0.3, 2)
    #pé esquerdo frente
    glPushMatrix()
    glTranslatef(0, 0, 3)
    glRotatef(90, 0, 1, 0)
    draw_block(0, 0, 0, 0.3, 0.1, 2)
    draw_block(0, 0, 0, 0.1, 0.3, 2)
    glPopMatrix()
    #pé direito trás
    glPushMatrix()
    glTranslatef(3, 0, 0)
    glRotatef(270, 0, 1, 0)
    draw_block(0, 0, 0, 0.3, 0.1, 2)
    draw_block(0, 0, 0, 0.1, 0.3, 2)
    glPopMatrix()
    #pé direito frente
    glPushMatrix()
    glTranslatef(3, 0, 3)
    glRotatef(180, 0, 1, 0)
    draw_block(0, 0, 0, 0.3, 0.1, 2)
    draw_block(0, 0, 0, 0.1, 0.3, 2)
    glPopMatrix()

    glPopMatrix() # fim fan_table

def draw_refrigerator(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    draw_texturized_block_right(0, 0, 0, 2, 2.5, 5, textures['guardaroupa'])
    glPopMatrix()

def draw_stove(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    draw_texturized_block_right(0, 0, 0, 2, 2, 2.5, textures['guardaroupa'])
    glPopMatrix()

def draw_sink(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    # pia lado esquerdo
    draw_colored_block_fixed(0, 2, 0, 1.25, 2, 0.1)
    # pia baixo
    draw_colored_block_fixed(1.25, 1.50, 0, 1, 1.50, 0.1)
    # pia lado direito
    draw_colored_block_fixed(2.25, 2, 0, 1.25, 2, 0.1)
    # pia baixo lado esquerdo
    draw_colored_block_fixed(1.15, 1.50, 0, 0.1, 1.50, 0.60)
    # pia baixo lado direito
    draw_colored_block_fixed(2.25, 1.50, 0, 0.1, 1.50, 0.60)
    # pia fundo
    draw_colored_block_fixed(1.25, 1.50, 0, 1, 0.10, 0.60)
    # pia frente
    draw_colored_block_fixed(1.25, 1.50, 1.40, 1, 0.10, 0.60)
    # pia frente horizontal
    draw_colored_block_fixed(1.25, 2, 1.40, 1, 0.60, 0.1)
    glPopMatrix()


def display():
    global angle, texture_brick, fan_rotation, door_angle, window_angle
    # limpa cor e buffers de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # reseta transformações
    glLoadIdentity()

    # define camera
    # camx camy camz centerx centery centerz upx upy upz
    gluLookAt(cameraPos.x, cameraPos.y, cameraPos.z,
              cameraPos.x + cameraFront.x, cameraPos.y + cameraFront.y, cameraPos.z + cameraFront.z,
              cameraUp.x, cameraUp.y, cameraUp.z)

    #fixed cam
    # gluLookAt(0, 5, 35,
    #           0, 0, -5,
    #           0, 1, 0)


    glPushMatrix() # push quarto
    # piso
    glColor(1, 1, 1)
    draw_textured_floor(-10, 0, -10, 20, 20, textures['ceramica'])

    # parede de trás
    glColor3ub(255, 255, 255)
    draw_textured_wall(-10, 0, -10, 10, 7, -10, textures['parede'])

    # parede esquerda
    # glColor3ub(181, 177, 163)
    glColor3ub(250, 250, 250)
    draw_textured_wall(-10, 0, -10, -10, 7, 10, textures['parede'])

    # parede da frente com portas e janelas
    glColor3ub(221,217,206)
    # part1 -  parte esquerda parede porta
    draw_block(-10, 0, 10, 2, 0.4, 7)
    # part2 - parte superior parede porta 
    draw_block(-8, 5, 10, 3, 0.4, 2)
    # part3 - parte direita parede porta
    draw_block(-5, 0, 10, 2, 0.4, 7)
    # part4 - parte cima da janela
    # draw_block(-3, 6, 10, 13, 0.4, 1)
    draw_block(-3, 5, 10, 4, 0.4, 2)
    # part5 - parte baixo janela
    #draw_block(-3, 0, 10, 4, 0.4, 5)
    draw_block(-3, 0, 10, 4, 0.4, 2.5)
    # part6 - restante da parede
    #draw_block(1, 0, 10, 3, 0.4, 6)
    draw_block(1, 0, 10, 9, 0.4, 7)

    """
    # part7
    draw_block(4, 5, 10, 6, 0.4, 1)
    # part8
    draw_block(4, 0, 10, 3, 0.4, 4)
    # part9
    draw_block(7, 0, 10, 3, 0.4, 5)
    """
    
    # alisais esquerdo - suporte porta lado esquerdo
    draw_colored_block_fixed(-8, 0, 10, 0.1, 0.4, 5)
    # alisais direito - suporte porta direito
    draw_colored_block_fixed(-5.1, 0, 10, 0.1, 0.4, 5)
    # alisais topo - suporte porta lado topo
    draw_colored_block_fixed(-7.9, 4.9, 10, 2.8, 0.4, 0.1)

    
    # alisais esquerdo - suporte janela lado esquerdo
    draw_colored_block_fixed(-3, 2.5, 10, 0.1, 0.4, 2.5)
    # alisais direito - suporte janela lado direito
    draw_colored_block_fixed(0.9, 2.5, 10, 0.1, 0.4, 2.5)
    # alisais baxio - suporte janela baixo
    draw_colored_block_fixed(-3, 2.5, 10, 4, 0.4, 0.1)
    # alisais cima - suporte janela cima
    draw_colored_block_fixed(-3, 4.9, 10, 4, 0.4, 0.1)

    #porta principal
    # draw_colored_block_fixed(-7.9, 0, 10, 2.8, 0.1, 4.9)
    glPushMatrix()
    glTranslatef(-7.9, 0, 10)
    glRotatef(door_angle, 0, 1, 0)
    draw_texturized_block_front_and_back(0,0,0, 2.8, 0.1, 4.9, textures['porta1'], textures['porta1'])
    glPopMatrix()

    #janela 1
    glPushMatrix()
    #glTranslatef(-3, 5, 10)
    glTranslatef(-2.9, 4.9, 10)
    glRotatef(-window_angle, 1, 0, 0)
    glColor3ub(70, 35, 26)
    # draw_colored_block_fixed(0, 0, 0, 4, 0.1, -1)
    #draw_texturized_block_front_and_back(0, 0, 0, 4, 0.1, -2.5, textures['wood'], textures['wood'])
    draw_texturized_block_front_and_back(0, 0, 0, 3.8, 0.1, -2.3, textures['wood'], textures['wood'])
    glPopMatrix()

    # parede direita
    glColor3ub(245, 245, 245)
    draw_textured_wall(10, 0, -10, 10, 7, 10, textures['parede'])

    # teto
    glColor3ub(250, 250, 250)
    draw_textured_floor(-10, 7, -10, 20, 20, textures['teto'])

    # mesa no centro
    glPushMatrix()
    glTranslatef(1.3, 0, 0)
    glRotatef(180, 0, 1, 0)
    draw_table1(0, 0, 0)
    # cadeira
    glRotatef(90, 0, 1, 0)
    draw_chair(-2, 0, 2.5)
    glPopMatrix()

    # Geladeira
    glPushMatrix()
    glTranslatef(-3, 0, -9.8)
    glRotatef(-90, 0, 1, 0)
    draw_refrigerator(0, 0, 0)
    glPopMatrix()

    # Fogão
    glPushMatrix()
    glTranslatef(4, 0, -9.8)
    glRotatef(-90, 0, 1, 0)
    draw_stove(0, 0, 0)
    glPopMatrix()

    # Pia
    glPushMatrix()
    glTranslatef(-2, 0, -10)
    draw_sink(0, 0, 0)
    glPopMatrix()
    """

    #comoda e tv
    glPushMatrix()
    glTranslatef(4, 0, 9.99)
    glRotatef(180, 0, 1, 0)
    draw_dresser(0, 0, 0)
    glPopMatrix()

    # guarda-roupas pequeno
    glPushMatrix()
    glScalef(0.6, 1, 0.3)
    glTranslatef(16.2, 0, 33)
    glRotatef(180, 0, 1, 0)
    draw_wardrobe(0, 0, 0)
    glPopMatrix()

    #quadro van gogh
    glPushMatrix()
    glColor3ub(255, 255, 255)
    draw_texturized_block_front(2, 4, -9.99, 3, 0.05, 2, textures['quadro1'])
    glPopMatrix()

    #quadro miro
    glPushMatrix()
    glColor3ub(255, 255, 255)
    draw_texturized_block_front(-4, 4, -9.99, 2, 0.05, 2, textures['miro'])
    glColor3ub(50, 50, 50)
    draw_block(-4.1, 3.9, -9.99, 0.1, 0.1, 2.2)#left
    draw_block(-2, 3.9, -9.99, 0.1, 0.1, 2.2)#down
    draw_block(-4.1, 3.9, -9.99, 2.1, 0.1, 0.1)#right
    draw_block(-4.1, 6, -9.99, 2.1, 0.1, 0.1)#up
    glPopMatrix()

    #mesa do ventilador
    glPushMatrix()
    glTranslatef(-1.3, 0, 9.9)
    glRotatef(180, 0, 1, 0)
    draw_fan_table(0, 0, 0)
    glScalef(0.7, 0.7, 0.7)
    draw_fan(2, 2.3, 1.3, fan_rotation)
    glPopMatrix()


    glPopMatrix()  # pop quarto

    glutSwapBuffers()

    # incrementa a variavel de rotação do ventilador
    if fan_rotation >= 360:
        fan_rotation = 0.0
    fan_rotation += 3 #velocidade da rotação
    """
    glPopMatrix()  # pop quarto

    glutSwapBuffers()

def keyboard_d_keys(key, dx, y):
    global angle, cameraFront, cameraUp, cameraPos

    if not isinstance(key, int):
        key = key.decode("utf-8")

    front = glm.vec3(0, 0, -1)

    cam_speed = 0.2

    if key == GLUT_KEY_LEFT:
        print("D_KEYS_L ", key)
        angle -= cam_speed
        front.x = glm.sin(angle)
        front.z = -glm.cos(angle)
    elif key == GLUT_KEY_RIGHT:
        print("D_KEYS_R ", key)
        angle += cam_speed
        front.x = glm.sin(angle)
        front.z = -glm.cos(angle)
    elif key == GLUT_KEY_UP:
        print("D_KEYS_U ", key)
        angle += cam_speed
        front.y = glm.sin(angle)
        # front.z = -glm.cos(angle)
    elif key == GLUT_KEY_DOWN:
        print("D_KEYS_D ", key)
        angle -= cam_speed
        front.y = glm.sin(angle)
        # front.z = -glm.cos(angle)

    # cameraFront = glm.normalize(front)
    cameraFront = front
    glutPostRedisplay()


def keyboard(key, x, y):
    global angle, cameraFront, cameraUp, cameraPos, door_angle, window_angle, light_ambient, light_specular, light_diffuse, lamp_color

    cameraSpeed = 0.5

    if not isinstance(key, int):
        key = key.decode("utf-8")
    #controles da camera
    if key == 'w' or key == 'W':
        cameraPos += cameraSpeed * cameraFront
    elif key == 'a' or key == 'A':
        cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    elif key == 's' or key == 'S':
        cameraPos -= cameraSpeed * cameraFront
    elif key == 'd' or key == 'D':
        cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    elif key == 'q' or key == 'Q':
        cameraPos.y += cameraSpeed/2
    elif key == 'e' or key == 'E':
        cameraPos.y -= cameraSpeed/2

    #abertura da porta
    if key == 'o':
        door_angle += 5
    if key == 'O':
        door_angle -= 5
    #abertura das janelas
    if key == 'j':
        window_angle += 5
    if key == 'J':
        window_angle -= 5
    #controle da iluminação
    if key == 'i':
        glEnable(GL_LIGHT0)
    if key == 'I':
        glDisable(GL_LIGHT0)
    #controle spotlight
    if key == 'l':
        lamp_color = glm.vec3(255, 255, 255)
        glEnable(GL_LIGHT1)
    if key == 'L':
        lamp_color = glm.vec3(10, 10, 10)
        glDisable(GL_LIGHT1)


    glutPostRedisplay()


def change_side(w, h):
    global half_width, half_height
    if h == 0:
        h = 1
    ratio = w * 1/h

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    glViewport(0, 0, w, h)

    half_width = w / 2
    half_height = h / 2

    gluPerspective(45, ratio, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)


def mouse_click(button, state, x, y):
    global old_mouse_x, old_mouse_y
    old_mouse_x = x
    old_mouse_y = y


def mouse_camera(mouse_x, mouse_y):
    global mouse_sensitivity, mouse_speed, angle_x, angle_y, cameraFront, old_mouse_x, old_mouse_y

    angle_x -= (mouse_x - old_mouse_x) * mouse_sensitivity
    angle_y -= (mouse_y - old_mouse_y) * mouse_sensitivity

    if angle_y > 2:
        angle_y = 2
    if angle_y < 1:
        angle_y = 1

    front = glm.vec3()
    front.x = glm.cos(angle_x) * glm.sin(angle_y)
    front.z = glm.sin(angle_x) * glm.sin(angle_y)
    front.y = glm.cos(angle_y)
    cameraFront = front

    old_mouse_x = mouse_x
    old_mouse_y = mouse_y
    glutPostRedisplay()


def load_texture(image):
    textureSurface = pygame.image.load(image)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glGenerateMipmap(GL_TEXTURE_2D)

    return texid


def setup_lighting():
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHT1)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1])

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.8, 0.8, 0.8, 1])
    # glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1])

    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.3, 0.3, 0.3, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 7, 0, 1])


    #spot light
    # spot light
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1, 1, 1, 1])

    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, [0, -1, 0])
    glLightfv(GL_LIGHT1, GL_POSITION, [0, 6, -1])

    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 20)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 2.0)

    # glLightfv(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1)
    # glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.5)
    # glLightfv(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.2)
    # glLightfv(GL_LIGHT1, GL_SPOT_EXPONENT, 2.0)


def main():
    global textures

    # inicialização
    glutInit()  # inicia glut
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(WINDOW_WIDHT, WINDOW_HEIGHT)
    window = glutCreateWindow("Cozinha")

    #iluminação
    setup_lighting()

    #callbacks
    glutDisplayFunc(display)
    glutReshapeFunc(change_side)
    glutKeyboardFunc(keyboard)
    # glutSpecialFunc(keyboard_d_keys) #old camera
    glutMouseFunc(mouse_click)
    glutMotionFunc(mouse_camera)

    #textures
    textures['brick'] = load_texture("textures/wall.png")
    textures['ceramica'] = load_texture("textures/ceramica.png")
    textures['guardaroupa'] = load_texture("textures/guarda-roupa.png")
    textures['ednaldo'] = load_texture("textures/ednaldo.png")
    textures['gavetas_comoda'] = load_texture("textures/gavetas_comoda.png")
    textures['portas_comoda'] = load_texture("textures/portas_comoda.png")
    textures['teto'] = load_texture("textures/teto-pvc.png")
    textures['parede'] = load_texture("textures/parede.png")
    textures['quadro1'] = load_texture("textures/quadro1.png")
    textures['miro'] = load_texture("textures/classic-miro.jpg")
    textures['tela_notebook'] = load_texture("textures/tela_notebook.png")
    textures['base_notebook'] = load_texture("textures/base_notebook.png")
    textures['porta1'] = load_texture("textures/porta1.png")
    textures['porta2'] = load_texture("textures/porta2.png")
    textures['wood'] = load_texture("textures/wood.png")
    textures['teclado'] = load_texture("textures/teclado.png")
    textures['tomada1'] = load_texture("textures/tomada1.png")
    textures['tomada2'] = load_texture("textures/tomada2.png")

    glutMainLoop()


main()
