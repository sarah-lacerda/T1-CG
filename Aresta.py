# ************************************************
#   Aresta.py
#   Define a classe Aresta
#   Autora: Sarah Lacerda da Silva
# ************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *

class Aresta:   
    def __init__(self, k=Ponto(), l=Ponto()):
        self.k = k
        self.l = l
    
    def imprime(self):
         print ("({x1}, {y1}, {z1}), ({x2}, {y2}, {z2})".format(x1=self.k.x, y1=self.k.y, z1=self.k.z, x2=self.l.x, y2=self.l.y, z2=self.l.z))
    
    def set(self, k, l):
        self.k = k
        self.l = l

    def desenhaAresta(self):
        glBegin(GL_LINE_LOOP)
        glVertex3f(self.k.x,self.k.y,self.k.z)
        glVertex3f(self.l.x,self.l.y,self.l.z)
        glEnd()
    
    def getPontoInicial(self):
        return self.k

    def getPontoFinal(self):
        return self.l

    def getPontoIntermediario(self):
        PosicaoXDoPontoIntermediario = (self.k.x + self.l.x)/2
        PosicaoYDoPontoIntermediario = (self.k.y + self.l.y)/2
        return Ponto(PosicaoXDoPontoIntermediario, PosicaoYDoPontoIntermediario)

# Funções passadas pelo professor em aula, determinam se existe um ponto de intersecção entre duas arestas.
# Retorna o ponto de intersecção, caso exista. De outro lado, retorna falso.
def Intersec2d(arestaA, arestaB):

    k = arestaA.getPontoInicial()
    l = arestaA.getPontoFinal() 
    m = arestaB.getPontoInicial() 
    n = arestaB.getPontoFinal() 

    det = (n.x - m.x) * (l.y - k.y) - (n.y - m.y) * (l.x - k.x)
    
    if det == 0:
        return False
    
    s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x))/det
    t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x))/det

    return (s, t)

def HaIntersec(arestaA, arestaB):

    ret = Intersec2d (arestaA, arestaB)

    k = arestaA.getPontoInicial()
    l = arestaA.getPontoFinal() 

    if not ret:
        return False
    if ret[0] >= 0.0 and ret[0] <= 1.0 and ret[1] >= 0.0 and ret[1] <= 1.0:
        pontoInicial = round((k.x + (l.x - k.x) * ret[0]), 2)
        pontoFinal = round((k.y + (l.y - k.y) * ret[0]), 2)
        PontoDeInterseccao = Ponto(pontoInicial, pontoFinal)
        return PontoDeInterseccao
    else:
        return False