# ************************************************
#   Ponto.py
#   Define a classe Ponto
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Adaptada por Sarah Lacerda da Silva
# ************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import copy

class Ponto:   
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def imprime(self):
        print (self.x, self.y, self.z)
    
    def set(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def multiplica(self, x, y, z):
        self.x *= x
        self.y *= y
        self.z *= z

    def desenhaPonto(self):
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex3f(self.x,self.y,self.z)
        glEnd()

def ObtemMaximo (P1, P2):
    Max = copy.deepcopy(P1)
    
    if (P2.x > Max.x):
        Max.x = P2.x

    if (P2.y > Max.y):
        Max.y = P2.y

    if (P2.z > Max.z):
        Max.z = P2.z

    return Max

def ObtemMinimo (P1, P2):
    Min = copy.deepcopy(P1)
    
    if (P2.x < Min.x):
        Min.x = P2.x
    
    if (P2.y < Min.y):
        Min.y = P2.y
    
    if (P2.z < Min.z):
        Min.z = P2.z

    return Min