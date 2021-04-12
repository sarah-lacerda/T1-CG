# ************************************************
#   Poligonos.py
#   Define a classe Polygon
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Point import *
from Aresta import *
import copy
import random


class Polygon:

    def __init__(self):
        self.Vertices = []
        self.sentidoHorario = None

    def getNVertices(self):
        return len(self.Vertices)
    
    def insereVertice(self, Point, position = -1):
        if position == -1:
            self.Vertices += [Point]
        else:
            self.Vertices = self.Vertices[:position] + [Point] + self.Vertices[position:]

    def desenhaPoligono(self):
        glBegin(GL_LINE_LOOP)
        for V in self.Vertices:
            glVertex3f(V.x,V.y,V.z)
        glEnd()

    def desenhaVertices(self):
        glPointSize(5)
        glBegin(GL_POINTS)
        for V in self.Vertices:
            glVertex3f(V.x,V.y,V.z)
        glEnd()

    def imprimeVertices(self):
        for x in self.Vertices:
            x.imprime()

    def getVertices(self, antiHorario = False):
        if self.sentidoHorario is None and len(self.Vertices) > 1:
            self.defineSentidoHorario()

        if self.sentidoHorario == True:
            if antiHorario == False:
                return self.Vertices
            else:
                return self.Vertices.reverse()
        elif self.sentidoHorario == False:
            if antiHorario == False:
                return self.Vertices.reverse()
            else:
                return self.Vertices
        else:
            return self.Vertices

    def getArestas(self, antiHorario = False):
        
        if len(self.Vertices) < 2:
            return []
        
        if self.sentidoHorario is None and len(self.Vertices) > 2:
            self.defineSentidoHorario()

        arestas = []

        if (self.sentidoHorario == True and antiHorario == False) or (self.sentidoHorario == False and antiHorario == True):

            for i in range(len(self.Vertices) - 1):
                nova_aresta = Aresta(self.Vertices[i], self.Vertices[i+1])
                arestas += [nova_aresta]

            arestas += [Aresta(self.Vertices[-1], self.Vertices[0])]

            return arestas

        else:

            for i in range(len(self.Vertices) - 1, 0, -1):
                nova_aresta = Aresta(self.Vertices[i], self.Vertices[i-1])
                arestas += [nova_aresta]

            arestas += [Aresta(self.Vertices[0], self.Vertices[-1])]

            return arestas

    #Algoritmo de checar se os vertices estão em sentido horário inspirado no algoritmo encontrado na
    #seguinte referência: https://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
    def defineSentidoHorario(self):
        sum = 0

        for i in range(len(self.Vertices) - 1):
            sum += (self.Vertices[i+1].x - self.Vertices[i].x) * (self.Vertices[i+1].y + self.Vertices[i].y)

        sum += (self.Vertices[0].x - self.Vertices[-1].x) * (self.Vertices[0].y + self.Vertices[-1].y)

        if sum >= 0:
            self.sentidoHorario = True
        else:
            self.sentidoHorario = False

    def getLimits(self):
        Min = copy.deepcopy(self.Vertices[0])
        Max = copy.deepcopy(self.Vertices[0])
        for V in self.Vertices:
            if V.x > Max.x:
                Max.x = V.x
            if V.y > Max.y:
                Max.y = V.y
            if V.z > Max.z:
                Max.z = V.z
            if V.x < Min.x:
                Min.x = V.x
            if V.y < Min.y:
                Min.y = V.y
            if V.z < Min.z:
                Min.z = V.z
        #Min.imprime()
        #Max.imprime()
        return Min, Max
    
    def EhPontoMinimoOuMaximoLocal(self, ponto):
        for i, vertice in enumerate(self.Vertices):
            if ponto.x == vertice.x and ponto.y == vertice.y:
                if vertice.y > self.Vertices[i-1].y and vertice.y > self.Vertices[(i+1) % len(self.Vertices)].y:
                    return True
                if vertice.y < self.Vertices[i-1].y and vertice.y < self.Vertices[(i+1) % len(self.Vertices)].y:
                    return True
        return False

    def RetornaIndexDoPonto(self, ponto):
        for i, vertice in enumerate(self.Vertices):
            if vertice.x == ponto.x and vertice.y == ponto.y:
                return i
        return False
    
    def PontoEstaDentro (self, ponto):
        poligonoMinMax = self.getLimits()
        numVerticesPoligono = self.getNVertices()
        arestaBase = Aresta(ponto, Point(poligonoMinMax[0].x-1, ponto.y))
        numInterseccoes = 0

        for i in range(numVerticesPoligono):
            arestaPoligono = Aresta(self.Vertices[i], self.Vertices[(i+1) % numVerticesPoligono])
            pontoDeInterseccao = HaIntersec(arestaBase, arestaPoligono)
        
            if pontoDeInterseccao:
                if self.EhPontoMinimoOuMaximoLocal(pontoDeInterseccao):
                    numInterseccoes += 2
                elif self.RetornaIndexDoPonto(pontoDeInterseccao):
                    numInterseccoes += 0.5
                else:
                    numInterseccoes += 1

        return numInterseccoes % 2 == 1

def CriaPoligonoComInterseccoes (poligonoA, poligonoB):
    poligonoAComInterseccoes = copy.deepcopy(poligonoA)
    VerticesB = poligonoB.Vertices
    numVerticesA = poligonoAComInterseccoes.getNVertices()
    numVerticesB = poligonoB.getNVertices()

    for i in range(numVerticesB):
        arestaB = Aresta(VerticesB[i], VerticesB[(i+1) % numVerticesB])
        j = 0
        while j < numVerticesA:
            VerticesA = poligonoAComInterseccoes.Vertices
            arestaA = Aresta(VerticesA[j], VerticesA[(j+1) % numVerticesA])
            pontoDeInterseccao = HaIntersec(arestaA, arestaB)
            if pontoDeInterseccao:
                poligonoAComInterseccoes.insereVertice(pontoDeInterseccao, j + 1)
                numVerticesA += 1
                j += 1
            j += 1

    return poligonoAComInterseccoes

def fazOperacoesPoligonos(poligonoA, poligonoB, operacao):

    arestasA = []
    arestasB = []

    for aresta in poligonoA.getArestas():
        if operacao == "uniao" or operacao == "sub":
            if not poligonoB.PontoEstaDentro(aresta.getPontoIntermediario()):
                arestasA += [aresta]
        elif operacao == "interseccao":
            if poligonoB.PontoEstaDentro(aresta.getPontoIntermediario()):
                arestasA += [aresta]
    
    reverse = operacao == "sub"

    for aresta in poligonoB.getArestas(reverse):
        if operacao == "uniao":
            if not poligonoA.PontoEstaDentro(aresta.getPontoIntermediario()):
                arestasB += [aresta]
        elif operacao == "interseccao" or operacao == "sub":
            if poligonoA.PontoEstaDentro(aresta.getPontoIntermediario()):
                arestasB += [aresta]

    PoligonosRetorno = []

    while arestasA or arestasB:
        
        if len(arestasA) >= len(arestasB):
            arestasPoligonoFinal = EncontraCiclo(arestasA, arestasB)
        else:
            arestasPoligonoFinal = EncontraCiclo(arestasB, arestasA)

        PoligonoRetorno = Polygon()
        
        for aresta in arestasPoligonoFinal:
            PoligonoRetorno.insereVertice(aresta.getPontoInicial())

        PoligonosRetorno += [PoligonoRetorno]

    return PoligonosRetorno

def EncontraCiclo(arestasA, arestasB):

    arestasResposta = []

    arestasResposta.append(arestasA.pop(0))
    
    arestaInicioArestasResposta = arestasResposta[0]
    arestaFimArestasResposta = arestasResposta[-1]

    while not (arestaInicioArestasResposta.getPontoInicial().x == arestaFimArestasResposta.getPontoFinal().x and arestaInicioArestasResposta.getPontoInicial().y == arestaFimArestasResposta.getPontoFinal().y):

        index = -1

        for i, aresta in enumerate(arestasA):
            if aresta.getPontoInicial().x == arestaFimArestasResposta.getPontoFinal().x and aresta.getPontoInicial().y == arestaFimArestasResposta.getPontoFinal().y:    
                index = i
                break
        if index != -1:
            arestasResposta.append(arestasA.pop(index))
        else:
            for i, aresta in enumerate(arestasB):
                if aresta.getPontoInicial().x == arestaFimArestasResposta.getPontoFinal().x and aresta.getPontoInicial().y == arestaFimArestasResposta.getPontoFinal().y:    
                    index = i
                    break
            arestasResposta.append(arestasB.pop(index))

        arestaInicioArestasResposta = arestasResposta[0]
        arestaFimArestasResposta = arestasResposta[-1]
    
    return arestasResposta