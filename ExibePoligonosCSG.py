# ***********************************************************************************
#   ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe um polígono em OpenGL
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
# ***********************************************************************************

import os
import tkinter as tk
from tkinter import filedialog, messagebox

from Poligono import *
from Ponto import *

# Polígonos e lista de polígonos que serão exibidos nas janelas
A = Poligono()
B = Poligono()
Uniao = []
Interseccao = []
DiferencaAB = []
DiferencaBA = []

# Limites lógicos da área de desenho
Min = Ponto()
Max = Ponto()
Meio = Ponto()
Terco = Ponto()
Largura = Ponto()

def reshape(w,h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, Max.x, 0, Max.y, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def DesenhaEixos():
    glBegin(GL_LINES)
    # eixo horizontal
    glVertex2f(0,Meio.y)
    glVertex2f(Max.x,Meio.y)
    #  eixo vertical 1
    glVertex2f(Terco.x,0)
    glVertex2f(Terco.x,Max.y)
    #  eixo vertical 2
    glVertex2f(2*Terco.x,0)
    glVertex2f(2*Terco.x,Max.y)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glOrtho(0, Max.x, 0, Max.y, 0.0, 1.0)
    glLoadIdentity()

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(1)
    DesenhaEixos()
    
    # Canto superior esquerdo
    glPushMatrix()
    glTranslatef(0, Meio.y, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    glColor3f(1,1,0)
    A.desenhaPoligono()
    glPopMatrix()

    # Meio, acima
    glPushMatrix()
    glTranslatef(Terco.x, Meio.y, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    glColor3f(1,0,1)
    B.desenhaPoligono()
    glPopMatrix()

    # Canto superior direito
    glPushMatrix()
    glTranslatef(Terco.x*2, Meio.y, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    for poligono in Uniao:
        glColor3f(1,0,0) # R, G, B  [0..1]
        poligono.desenhaPoligono()
    glPopMatrix()
    
    #Canto inferior esquerdo
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    for poligono in Interseccao:
        glColor3f(1,0,0) # R, G, B  [0..1]
        poligono.desenhaPoligono()
    glPopMatrix()
    
    # Meio, abaixo
    glPushMatrix()
    glTranslatef(Terco.x, 0, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    for poligono in DiferencaAB:
        glColor3f(1,0,0) # R, G, B  [0..1]
        poligono.desenhaPoligono()
    glPopMatrix()

    # Canto inferior direito
    glPushMatrix()
    glTranslatef(Terco.x*2, 0, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    for poligono in DiferencaBA:
        glColor3f(1,0,0) # R, G, B  [0..1]
        poligono.desenhaPoligono()
    glPopMatrix()

    glutSwapBuffers()

def resizeWindow():
    global A, B, Min, Max, Largura, Terco, Meio, Uniao, Interseccao, DiferencaAB, DiferencaBA

    Uniao = []
    Interseccao = []
    DiferencaAB = []
    DiferencaBA = []

    Min, Max = A.getLimits()
    MinAux, MaxAux = B.getLimits()

    # Atualiza os limites globais após cada leitura
    Min = ObtemMinimo(Min, MinAux)
    Max = ObtemMaximo(Max, MaxAux)

    # Ajusta a largura da janela lógica em função do tamanho dos polígonos
    Largura.x = Max.x
    Largura.y = Max.y
    
    # Calcula 1/3 da largura da janela
    Terco = Largura
    fator = 1.0/3.0
    Terco.multiplica(fator, fator, fator)
    
    #Calcula 1/2 da largura da janela
    Meio.x = Max.x/2
    Meio.y = Max.y/2
    Meio.z = Max.z/2

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, Max.x, 0, Max.y, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def keyboard(*args):
    
    global Uniao, Interseccao, DiferencaAB, DiferencaBA
    ESCAPE = b'\x1b'

    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    
    if args[0] == ESCAPE:
        os._exit(0)
    
    if args[0] == b'a':
        tk.messagebox.showinfo(title=None, message="Escolha o arquivo que contém o polígono A")
        file_path = filedialog.askopenfilename(initialdir=os.getcwd)
        A.LePontosDeArquivo(file_path)
        resizeWindow()

    if args[0] == b'b':
        tk.messagebox.showinfo(title=None, message="Escolha o arquivo que contém o polígono B")
        file_path = filedialog.askopenfilename(initialdir=os.getcwd)
        B.LePontosDeArquivo(file_path)
        resizeWindow()
    
    if args[0] == b'u':
        tk.messagebox.showinfo(title=None, message="Fazendo operação de união")
        Uniao = fazOperacoesPoligonos(A, B, 'uniao')
        for i, poligono in enumerate(Uniao):
            nomeDoArquivo = "AUniaoB{}.txt".format(i if i > 0 else "")
            poligono.SalvaParaArquivo(nomeDoArquivo)

    if args[0] == b'i':
        tk.messagebox.showinfo(title=None, message="Fazendo operação de intersecção")
        Interseccao = fazOperacoesPoligonos(A, B, 'interseccao')
        for i, poligono in enumerate(Interseccao):
            nomeDoArquivo = "AInterseccaoB{}.txt".format(i if i > 0 else "")
            poligono.SalvaParaArquivo(nomeDoArquivo)
    
    if args[0] == b's':
        tk.messagebox.showinfo(title=None, message="Fazendo operação de diferença entre A e B")
        DiferencaAB = fazOperacoesPoligonos(A, B, 'sub')
        for i, poligono in enumerate(DiferencaAB):
            nomeDoArquivo = "ADiferencaB{}.txt".format(i if i > 0 else "")
            poligono.SalvaParaArquivo(nomeDoArquivo)
    
    if args[0] == b'd':
        tk.messagebox.showinfo(title=None, message="Fazendo operação de diferença entre B e A")
        DiferencaBA = fazOperacoesPoligonos(B, A, 'sub')
        for i, poligono in enumerate(DiferencaBA):
            nomeDoArquivo = "BDiferencaA{}.txt".format(i if i > 0 else "")
            poligono.SalvaParaArquivo(nomeDoArquivo)

    # Força o redesenho da tela
    glutPostRedisplay()

def init():
    
    root = tk.Tk()
    root.withdraw()

    A.LePontosDeArquivo(sys.argv[1])
    B.LePontosDeArquivo(sys.argv[2])

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(1000, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Exibe Poligonos")
    resizeWindow()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    
# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

init()

try:
    glutMainLoop()
except SystemExit:
    pass
