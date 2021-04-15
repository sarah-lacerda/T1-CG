# T1 de Fundamentos de Computação Gráfica

---
### Sarah Lacerda da Silva
#### Matrícula 17104191

O programa consiste em uma janela com seis subdvisões, que representam as seguintes imagens:

1. Polígono A
2. Polígono B
3. União entre polígono A e B
4. Intersecção entre polígono A e B
5. Diferença entre polígono A e B
6. Diferença entre polígono B e A

Ao inicializar o programa a partir de `ExibePoligonosCSG.py` fica necessario receber como argumentos os caminhos de dois
arquivos de texto com a definição dos primeiros dois polígonos a serem operados.

#### O programa também aceita comandos pelo teclado, sendo os seguintes:

| Tecla      | Descrição |
| ----------- | ----------- |
| **ESC** ou **q**  | Sai do programa.                                         |
| **a**             | Carrega polígono de arquivo de texto para o polígono A   |
| **b**             | Carrega polígono de arquivo de texto para o polígono B   |
| **u**             | Operação de união                                        |
| **i**             | Operação de intersecção                                  |
| **s**             | Operação de diferença entre A e B                        |
| **d**             | Operação de diferença entre B e A                        |

*Após realizada uma das operações, o programa salva o(s) polígono(s) resultante(s) em arquivo(s) de texto.
Se a operação resulta em mais de um polígono, o programa salva cada um em um arquivo diferente.*

#### IMPORTANTE! O programa não aceita polígonos com valores negativos na coordenada de seus pontos.
#### IMPORTANTE! Algumas operações com polígonos que possuem arestas compartilhadas podem resultar em problemas.
