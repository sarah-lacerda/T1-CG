# ************************************************
#   Point.py
#   Define a classe Ponto
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Point:   
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
        #print ("Objeto criado")
    
    def imprime(self):
        print (self.x, self.y, self.z)
    
    def set(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def multiplica(self, x, y, z):
        self.x *= x;
        self.y *= y;
        self.z *= z;

    def desenhaPonto(self):
        glPointSize(5);
        glBegin(GL_POINTS);
        glVertex3f(self.x,self.y,self.z);
        glEnd();

#P = Point()
#P.set(1,2)
#P.imprime()
#P.set(23,34,56)
#P.imprime()

