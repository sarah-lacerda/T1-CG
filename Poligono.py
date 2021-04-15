# ************************************************
#   Poligono.py
#   Define a classe Poligono
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Adaptada por Sarah Lacerda da Silva
# ************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *
from Aresta import *
import copy, random, math

class Poligono:

    def __init__(self):
        self.Vertices = []
        self.sentidoHorario = None

    def getNVertices(self):
        return len(self.Vertices)
    
    def insereVertice(self, ponto, position = -1):
        if position == -1:
            self.Vertices += [ponto]
        else:
            self.Vertices = self.Vertices[:position] + [ponto] + self.Vertices[position:]

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

    # Algoritmo de checar se os vértices do polígono estão em sentido horário inspirado no algoritmo encontrado na
    # seguinte referência: https://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
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
    
    def TemPonto(self, ponto):
        for vertice in self.Vertices:
            if vertice.x == ponto.x and vertice.y == ponto.y and vertice.z == ponto.z:
                return True
        return False

    def PontoEstaDentro (self, ponto):
        poligonoMinMax = self.getLimits()
        numVerticesPoligono = self.getNVertices()
        arestaBase = Aresta(ponto, Ponto(poligonoMinMax[0].x-1, ponto.y))
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

    def LePontosDeArquivo(self, Nome):
        self.Vertices = []
        infile = open(Nome)
        line = int(infile.readline())
        for _ in range(line):
            words = infile.readline().split()
            x = float (words[0])
            y = float (words[1])
            Pt = Ponto(x, y)
            self.insereVertice(Pt)
        infile.close()
    
    def SalvaParaArquivo(self, Nome):
        with open(Nome, 'w') as f:
            f.write(str(self.getNVertices()) + '\n')
            for vertice in self.Vertices:
                f.write("{} {}\n".format(vertice.x, vertice.y))

def CriaPoligonosComInterseccoes (poligonoA, poligonoB):
    
    poligonoAComInterseccoes = copy.deepcopy(poligonoA)
    poligonoBComInterseccoes = copy.deepcopy(poligonoB)

    VerticesA = poligonoA.Vertices
    VerticesB = poligonoB.Vertices

    numVerticesA = poligonoAComInterseccoes.getNVertices()
    numVerticesB = poligonoB.getNVertices()

    pontosDeInterseccao = copy.deepcopy(VerticesA)

    for i in range(numVerticesB):
        arestaB = Aresta(VerticesB[i], VerticesB[(i+1) % numVerticesB])
        j = 0
        while j < numVerticesA:
            VerticesA = poligonoAComInterseccoes.Vertices
            arestaA = Aresta(VerticesA[j], VerticesA[(j+1) % numVerticesA])
            pontoDeInterseccao = HaIntersec(arestaA, arestaB)
            if pontoDeInterseccao:
                if not poligonoAComInterseccoes.TemPonto(pontoDeInterseccao):
                    pontosDeInterseccao.append(pontoDeInterseccao)
                    poligonoAComInterseccoes.insereVertice(pontoDeInterseccao, j + 1)
                    numVerticesA += 1
                    j += 1
            j += 1

    for i in range(numVerticesA):
        arestaA = Aresta(VerticesA[i], VerticesA[(i+1) % numVerticesA])
        j = 0
        while j < numVerticesB:
            VerticesB = poligonoBComInterseccoes.Vertices
            arestaB = Aresta(VerticesB[j], VerticesB[(j+1) % numVerticesB])
            pontoDeInterseccao = HaIntersec(arestaB, arestaA)
            if pontoDeInterseccao:

                noMatch = True
                for ponto in pontosDeInterseccao:
                    if pontoDeInterseccao.x == ponto.x and pontoDeInterseccao.y == ponto.y and pontoDeInterseccao.z == ponto.z:
                        noMatch = False

                if noMatch:
                    indexMinDist = 0
                    minDist = math.sqrt((pontoDeInterseccao.x - pontosDeInterseccao[0].x)**2 + (pontoDeInterseccao.y - pontosDeInterseccao[0].y)**2 + (pontoDeInterseccao.z - pontosDeInterseccao[0].z)**2)

                    for i in range(1, len(pontosDeInterseccao)):
                        currentDist = math.sqrt((pontoDeInterseccao.x - pontosDeInterseccao[i].x)**2 + (pontoDeInterseccao.y - pontosDeInterseccao[i].y)**2 + (pontoDeInterseccao.z - pontosDeInterseccao[i].z)**2)
                        if currentDist < minDist:
                            minDist = currentDist
                            indexMinDist = i
                    
                    pontoDeInterseccao = pontosDeInterseccao[indexMinDist]

                if not poligonoBComInterseccoes.TemPonto(pontoDeInterseccao):
                    poligonoBComInterseccoes.insereVertice(pontoDeInterseccao, j + 1)
                    numVerticesB += 1
                    j += 1
            j += 1

    return poligonoAComInterseccoes, poligonoBComInterseccoes

def fazOperacoesPoligonos(poligonoA, poligonoB, operacao):

    AComIntersec, BComIntersec = CriaPoligonosComInterseccoes(poligonoA, poligonoB)

    arestasA = []
    arestasB = []

    for aresta in AComIntersec.getArestas():
        if operacao == "uniao" or operacao == "sub":
            if not poligonoB.PontoEstaDentro(aresta.getPontoIntermediario()):
                arestasA += [aresta]
        elif operacao == "interseccao":
            if poligonoB.PontoEstaDentro(aresta.getPontoIntermediario()):
                arestasA += [aresta]
    
    reverse = operacao == "sub"

    for aresta in BComIntersec.getArestas(reverse):
        if operacao == "uniao":
            if not poligonoA.PontoEstaDentro(aresta.getPontoIntermediario()):
                arestasB += [aresta]
        elif operacao == "interseccao" or operacao == "sub":
            if poligonoA.PontoEstaDentro(aresta.getPontoIntermediario()):
                arestasB += [aresta]

    PoligonosRetorno = EncontraCiclos(arestasA, arestasB)

    return PoligonosRetorno

def EncontraCiclos(arestasA, arestasB):

    poligonosRetorno = []

    arestasTotais = arestasA + arestasB

    while arestasTotais:
        
        # Impede loop infinito
        numArestas = len(arestasTotais)

        poligono = Poligono()
        arestasCiclo = []

        arestasCiclo.append(arestasTotais.pop(0))
        arestaInicioCiclo = arestasCiclo[0]
        arestaFimCiclo = arestasCiclo[-1]

        while not (arestaInicioCiclo.getPontoInicial().x == arestaFimCiclo.getPontoFinal().x and arestaInicioCiclo.getPontoInicial().y == arestaFimCiclo.getPontoFinal().y):

            # Impede loop infinito
            numArestasInsideLoop = len(arestasTotais)

            for i, aresta in enumerate(arestasTotais):
                if aresta.getPontoInicial().x == arestaFimCiclo.getPontoFinal().x and aresta.getPontoInicial().y == arestaFimCiclo.getPontoFinal().y:    
                    arestasCiclo.append(arestasTotais.pop(i))
                    break

            arestaInicioCiclo = arestasCiclo[0]
            arestaFimCiclo = arestasCiclo[-1]

            # Impede loop infinito
            if numArestasInsideLoop == len(arestasTotais):
                return []

        for aresta in arestasCiclo:
            poligono.insereVertice(aresta.getPontoInicial())

        poligonosRetorno += [poligono]
        
        # Impede loop infinito
        if numArestas == len(arestasTotais):
            return []

    return poligonosRetorno