import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
import numpy as np
from math import pi,cos,sin

def move (dx,dy,dz):
    T = np.eye(4)
    T[0,-1] = dx
    T[1,-1] = dy
    T[2,-1] = dz
    return T

def rotz(angle):
    rotation_matrix=np.array([[cos(angle),-sin(angle),0,0],[sin(angle),cos(angle),0,0],[0,0,1,0],[0,0,0,1]])
    return rotation_matrix

def rotx(angle):
    rotation_matrix=np.array([[1,0,0,0],[0, cos(angle),-sin(angle),0],[0, sin(angle), cos(angle),0],[0,0,0,1]])
    return rotation_matrix

def roty(angle):
    rotation_matrix=np.array([[cos(angle),0, sin(angle),0],[0,1,0,0],[-sin(angle), 0, cos(angle),0],[0,0,0,1]])
    return rotation_matrix


def set_plot(ax=None,figure = None,lim=[-2,2]):
    if figure ==None:
        figure = plt.figure(figsize=(8,8))
    if ax==None:
        ax = plt.axes(projection='3d')
    
    ax.set_title("Camera Reference")
    ax.set_xlim(lim)
    ax.set_xlabel("x axis")
    ax.set_ylim(lim)
    ax.set_ylabel("y axis")
    ax.set_zlim(lim)
    ax.set_zlabel("z axis")
    return ax

#adding quivers to the plot
def draw_arrows(point,base,axis,length=1.5):
    # The object base is a matrix, where each column represents the vector 
    # of one of the axis, written in homogeneous coordinates (ax,ay,az,0)
    

    # Plot vector of x-axis
    axis.quiver(point[0],point[1],point[2],base[0,0],base[1,0],base[2,0],color='red',pivot='tail',  length=length)
    # Plot vector of y-axis
    axis.quiver(point[0],point[1],point[2],base[0,1],base[1,1],base[2,1],color='green',pivot='tail',  length=length)
    # Plot vector of z-axis
    axis.quiver(point[0],point[1],point[2],base[0,2],base[1,2],base[2,2],color='blue',pivot='tail',  length=length)

    return axis 

import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QGroupBox, QGridLayout, QPushButton, QLabel, QSpinBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class App(QDialog):
    def __init__(self):
        super().__init__()

        self.e1 = np.array([[1],[0],[0],[0]]) # X
        self.e2 = np.array([[0],[1],[0],[0]]) # Y
        self.e3 = np.array([[0],[0],[1],[0]]) # Z
        self.base = np.hstack((self.e1,self.e2,self.e3))

        self.point = np.array([[0],[0],[0],[1]])
        self.cam = np.hstack((self.base, self.point))

        self.house = np.array([[0,0,0],
                  [0,522,0],
                  [0,522,-80],
                  [0,522,-160],
                  [0,522,-240],
                  [0,507,-317],
                  [0,486,-390],
                  [0,443,-473],
                  [0,346,-547],
                  [0,260,-630],
                  [0,141,-547],
                  [0,74,-473],
                  [0,33,-390],
                  [0,11,-317],
                  [0,5,-240],
                  [0,0,-160],
                  [0,0,-80],
                  [0,0,0],
                  [0,522,0],
                  [0,522,-80],
                  [0,261,-80],
                  [0,261,-160],
                  [0,522,-160],
                  [0,522,-240],
                  [0,5,-240],
                  [0,11,-317],
                  [0,507,-317],
                  [0,486,-390],
                  [0,33,-390],
                  [0,74,-473],
                  [0,443,-473],
                  [0,346,-547],
                  [0,141,-547],
                  [0,74,-473],
                  [0,33,-390],
                  [0,11,-317],
                  [0,5,-240],
                  [0,0,-160],
                  [0,0,-80],
                  [0,0,0],
                  [0,261,0],
                  [0,261,-240],
                  [0,5,-240],
                  [0,0,-160],
                  [0,0,-80],
                  [0,0,0],
                  [-70,0,0],
                  [-70,522,0],
                  [0,522,0],
                  [-70,522,0],
                  [-70,522,-80],
                  [-70,522,-160],
                  [-70,522,-240],
                  [-70,507,-317],
                  [-70,486,-390],
                  [-70,443,-473],
                  [-70,346,-547],
                  [-70,260,-630],
                  [0,260,-630],
                  [-70,260,-630],
                  [-70,141,-547],
                  [-70,74,-473],
                  [-70,33,-390],
                  [-70,11,-317],
                  [-70,5,-240],
                  [-70,0,-160],
                  [-70,0,-80],
                  [-70,0,0],
                  [0,0,0],
                  [0,180,0],
                  [0,180,-50],
                  [0,50,-50],
                  [0,50,-180],
                  [0,180,-180],
                  [0,50,-180],
                  [0,50,-50],
                  [0,180,-50],
                  [0,50,-120],
                  [0,200,-200],
                  [0,50,-120],
                  [0,140,-120]])
        
        self.house = self.house*(4/100)

        self.house = np.transpose(self.house)
        self.house1 = np.vstack([self.house, np.ones(np.size(self.house,1))])

        self.matriz_M = np.eye(4)
        self.rotcam = np.dot(roty(-pi/2),np.eye(4))
        self.matriz_M = np.dot(self.rotcam, self.matriz_M) 
        self.rotcam3 = np.dot(rotz(pi/2),np.eye(4))
        self.matriz_M = np.dot(self.matriz_M, self.rotcam3)
        self.matriz_M = np.dot(move(20,11,-11), self.matriz_M)

        ##criando uma segunda camera
        self.nova_cam = np.dot(self.matriz_M,self.cam)

        ##criando matriz inversa de M
        self.inv_M = np.linalg.inv(self.matriz_M)

        ##parametros intrincicos
        self.f = 100
        self.fs0 = 0
        self.sx = 128/36
        self.sy = 72/24
        self.fsy = self.sy*self.f
        self.fsx = self.sx*self.f
        self.ox = 1280/2
        self.oy = 720/2
        self.xlimup = 1280
        self.xlimbt = 0
        self.ylimup = 720
        self.ylimbt = 0

        self.matriz_Mc = self.matriz_M
        self.matriz_K = np.array([[self.fsx,self.fs0,self.ox],[0,self.fsy,self.oy],[0,0,1]])
        self.z = np.eye(3,4)
        self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

        self.imgCASA = np.dot(self.p,self.house1)
        self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
        self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
        self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

        self.title = "Trabalho 01 - Andre e Zuelzer"
        self.left = 100
        self.top = 100
        self.width = 900
        self.height = 600
        
        self.fig1 = plt.figure()
        self.ax1 = self.fig1.add_subplot(111, projection='3d')
        self.initUI()
        
        self.clickbutton2(action = "reset parameter")
        self.clickbutton2(action = "reset position")

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()
        #Desenhando os Grupos do Layout
        groupw =  QGroupBox("Welcome")
        self.setFontBold(groupw)
        layout.addWidget(groupw, 0, 0, 3, 1)

        group_world = QGroupBox("World Reference")        
        self.setFontBold(group_world)
        layout.addWidget(group_world, 3, 0)

        group_cam = QGroupBox("Camera Reference") 
        self.setFontBold(group_cam)
        layout.addWidget(group_cam, 3, 1)

        group_par = QGroupBox("Intrinsic Parameters")
        self.setFontBold(group_par)
        layout.addWidget(group_par, 3, 2, 1, 2)

        group_3d = QGroupBox("3D View")
        self.setFontBold(group_3d)
        layout.addWidget(group_3d, 0, 1, 3, 1)

        group_2d = QGroupBox("2D View")
        self.setFontBold(group_2d)
        layout.addWidget(group_2d, 0, 2, 3, 1)

        #Welcome --Grupo
        gridLayoutw = QGridLayout()
        groupw.setLayout(gridLayoutw)

        #Texto Legenda
        Labelleg = QLabel("For T, read Translation.")
        Labelleg.setWordWrap(True)  # Ativa a quebra de linha automática
        Labelleg.adjustSize() 
        gridLayoutw.addWidget(Labelleg, 0, 0)

        Labellegr = QLabel("For R, read Rotation. ")
        Labellegr.setWordWrap(True)  # Ativa a quebra de linha automática
        Labellegr.adjustSize() 
        gridLayoutw.addWidget(Labellegr, 2, 0)
        #Reset
        #Botão de Reset Position
        buttonR1 = QPushButton("Reset position")
        buttonR1.setFixedWidth(130)
        buttonR1.clicked.connect(lambda: self.clickbutton2("reset position"))
        gridLayoutw.addWidget(buttonR1, 5, 0)
        #Botão de Reset Parameter
        buttonR2 = QPushButton("Reset parameter")
        buttonR2.setFixedWidth(130)
        buttonR2.clicked.connect(lambda: self.clickbutton2("reset parameter"))
        gridLayoutw.addWidget(buttonR2, 6, 0)

        #Referencial do Mundo --Grupo
        gridLayout1 = QGridLayout()
        group_world.setLayout(gridLayout1)
        #Texto
        Labelm = QLabel("T")
        Labelm.setAlignment(QtCore.Qt.AlignCenter)
        Labelm.setFixedWidth(20)
        gridLayout1.addWidget(Labelm, 0, 1)
        Labelr = QLabel("R")
        Labelr.setAlignment(QtCore.Qt.AlignCenter)
        Labelr.setFixedWidth(20)
        gridLayout1.addWidget(Labelr, 0, 4)
        #Para X, Y e Z
        #X mundo
        Labelxw = QLabel("X")
        Labelxw.setFixedWidth(40)
        gridLayout1.addWidget(Labelxw, 1, 0)
        #Para Transladar
        #Botão de Mais
        buttonXtm = QPushButton("+")
        buttonXtm.setFixedWidth(25)
        buttonXtm.clicked.connect(lambda: self.clickbutton("Xtm"))
        gridLayout1.addWidget(buttonXtm, 1, 1)
        #Botão de Menos
        buttonXtme = QPushButton("-")
        buttonXtme.setFixedWidth(25)
        buttonXtme.clicked.connect(lambda: self.clickbutton("Xtme"))
        gridLayout1.addWidget(buttonXtme, 1, 2)
        #Para Rotacionar
        #Botão de Mais
        buttonXrm = QPushButton("+")
        buttonXrm.setFixedWidth(25)
        buttonXrm.clicked.connect(lambda: self.clickbutton("Xrm"))
        gridLayout1.addWidget(buttonXrm, 1, 4)
        #Botão de Menos
        buttonXrme = QPushButton("-")
        buttonXrme.setFixedWidth(25)
        buttonXrme.clicked.connect(lambda: self.clickbutton("Xrme"))
        gridLayout1.addWidget(buttonXrme, 1, 5)

        #Y mundo
        Labelyw = QLabel("Y")
        Labelyw.setFixedWidth(40)
        gridLayout1.addWidget(Labelyw, 2, 0)
        #Para Transladar
        #Botão de Mais
        buttonYtm = QPushButton("+")
        buttonYtm.setFixedWidth(25)
        buttonYtm.clicked.connect(lambda: self.clickbutton("Ytm"))
        gridLayout1.addWidget(buttonYtm, 2, 1)
        #Botão de Menos
        buttonYtme = QPushButton("-")
        buttonYtme.setFixedWidth(25)
        buttonYtme.clicked.connect(lambda: self.clickbutton("Ytme"))
        gridLayout1.addWidget(buttonYtme, 2, 2)
        #Para Rotacionar
        #Botão de Mais
        buttonYrm = QPushButton("+")
        buttonYrm.setFixedWidth(25)
        buttonYrm.clicked.connect(lambda: self.clickbutton("Yrm"))
        gridLayout1.addWidget(buttonYrm, 2, 4)
        #Botão de Menos
        buttonYrme = QPushButton("-")
        buttonYrme.setFixedWidth(25)
        buttonYrme.clicked.connect(lambda: self.clickbutton("Yrme"))
        gridLayout1.addWidget(buttonYrme, 2, 5)

        #Z mundo
        Labelzw = QLabel("Z")
        Labelzw.setFixedWidth(40)
        gridLayout1.addWidget(Labelzw, 3, 0)
        #Para Transladar
        #Botão de Mais
        buttonZtm = QPushButton("+")
        buttonZtm.setFixedWidth(25)
        buttonZtm.clicked.connect(lambda: self.clickbutton("Ztm"))
        gridLayout1.addWidget(buttonZtm, 3, 1)
        #Botão de Menos
        buttonZtme = QPushButton("-")
        buttonZtme.setFixedWidth(25)
        buttonZtme.clicked.connect(lambda: self.clickbutton("Ztme"))
        gridLayout1.addWidget(buttonZtme, 3, 2)
        #Para Rotacionar
        #Botão de Mais
        buttonZrm = QPushButton("+")
        buttonZrm.setFixedWidth(25)
        buttonZrm.clicked.connect(lambda: self.clickbutton("Zrm"))
        gridLayout1.addWidget(buttonZrm, 3, 4)
        #Botão de Menos
        buttonZrme = QPushButton("-")
        buttonZrme.setFixedWidth(25)
        buttonZrme.clicked.connect(lambda: self.clickbutton("Zrme"))
        gridLayout1.addWidget(buttonZrme, 3, 5)

        #Referencial da Camera --Grupo
        gridLayout2 = QGridLayout()
        group_cam.setLayout(gridLayout2)
        #Texto
        Labelm = QLabel("T")
        Labelm.setAlignment(QtCore.Qt.AlignCenter)
        Labelm.setFixedWidth(20)
        gridLayout2.addWidget(Labelm, 0, 1)

        Labelr = QLabel("R")
        Labelr.setAlignment(QtCore.Qt.AlignCenter)
        Labelr.setFixedWidth(20)
        gridLayout2.addWidget(Labelr, 0, 4)

        # PARA X, Y e Z
        #CAM X
        Labelxc = QLabel("X")
        Labelxc.setFixedWidth(40)
        gridLayout2.addWidget(Labelxc, 1, 0)
        #Para Transladar
        #Botão de Mais
        buttoncXtm = QPushButton("+")
        buttoncXtm.setFixedWidth(25)
        buttoncXtm.clicked.connect(lambda: self.clickbutton("cXtm"))
        gridLayout2.addWidget(buttoncXtm, 1, 1)
        #Botão de Menos
        buttoncXtme = QPushButton("-")
        buttoncXtme.setFixedWidth(25)
        buttoncXtme.clicked.connect(lambda: self.clickbutton("cXtme"))
        gridLayout2.addWidget(buttoncXtme, 1, 2)
        #Para Rotacionar
        #Botão de Mais
        buttoncXrm = QPushButton("+")
        buttoncXrm.setFixedWidth(25)
        buttoncXrm.clicked.connect(lambda: self.clickbutton("cXrm"))
        gridLayout2.addWidget(buttoncXrm, 1, 4)
        #Botão de Menos
        buttoncXrme = QPushButton("-")
        buttoncXrme.setFixedWidth(25)
        buttoncXrme.clicked.connect(lambda: self.clickbutton("cXrme"))
        gridLayout2.addWidget(buttoncXrme, 1, 5)

        #Button Y
        Labelyc = QLabel("Y")
        Labelyc.setFixedWidth(40)
        gridLayout2.addWidget(Labelyc, 2, 0)
        #Para Transladar
        #Botão de Mais
        buttoncYtm = QPushButton("+")
        buttoncYtm.setFixedWidth(25)
        buttoncYtm.clicked.connect(lambda: self.clickbutton("cYtm"))
        gridLayout2.addWidget(buttoncYtm, 2, 1)
        #Botão de Menos
        buttoncYtme = QPushButton("-")
        buttoncYtme.setFixedWidth(25)
        buttoncYtme.clicked.connect(lambda: self.clickbutton("cYtme"))
        gridLayout2.addWidget(buttoncYtme, 2, 2)
        #Para Rotacionar
        #Botão de Mais
        buttoncYrm = QPushButton("+")
        buttoncYrm.setFixedWidth(25)
        buttoncYrm.clicked.connect(lambda: self.clickbutton("cYrm"))
        gridLayout2.addWidget(buttoncYrm, 2, 4)
        #Botão de Menos
        buttoncYrme = QPushButton("-")
        buttoncYrme.setFixedWidth(25)
        buttoncYrme.clicked.connect(lambda: self.clickbutton("cYrme"))
        gridLayout2.addWidget(buttoncYrme, 2, 5)

        #Button Z
        Labelzc = QLabel("Z")
        Labelzc.setFixedWidth(70)
        gridLayout2.addWidget(Labelzc, 3, 0)
        #Para Transladar
        #Botão de Mais
        buttoncZtm = QPushButton("+")
        buttoncZtm.setFixedWidth(25)
        buttoncZtm.clicked.connect(lambda: self.clickbutton("cZtm"))
        gridLayout2.addWidget(buttoncZtm, 3, 1)
        #Botão de Menos
        buttoncZtme = QPushButton("-")
        buttoncZtme.setFixedWidth(25)
        buttoncZtme.clicked.connect(lambda: self.clickbutton("cZtme"))
        gridLayout2.addWidget(buttoncZtme, 3, 2)
        #Para Rotacionar
        #Botão de Mais
        buttoncZrm = QPushButton("+")
        buttoncZrm.setFixedWidth(25)
        buttoncZrm.clicked.connect(lambda: self.clickbutton("cZrm"))
        gridLayout2.addWidget(buttoncZrm, 3, 4)
        #Botão de Menos
        buttoncZrme = QPushButton("-")
        buttoncZrme.setFixedWidth(25)
        buttoncZrme.clicked.connect(lambda: self.clickbutton("cZrme"))
        gridLayout2.addWidget(buttoncZrme, 3, 5)

        #Parametros intrinsecos da Camera --Grupo
        gridLayout3 = QGridLayout()
        group_par.setLayout(gridLayout3)
        #Para f
        Labelf = QLabel("f(0, 1000)")
        Labelf.setFixedWidth(80)
        gridLayout3.addWidget(Labelf, 0, 0)

        self.Numberf = QSpinBox()
        self.Numberf.setFixedWidth(50)
        self.Numberf.setValue(100) 
        self.Numberf.setMinimum(1)
        self.Numberf.setMaximum(1000)
        self.Numberf.setSingleStep(10)
        self.Numberf.valueChanged.connect(lambda: self.clickspinbox("F"))
        gridLayout3.addWidget(self.Numberf, 0, 1)

        #Para s0
        Labelso = QLabel("s0(-500, 500)")
        Labelso.setFixedWidth(90)
        gridLayout3.addWidget(Labelso, 0, 2)

        self.Numberso = QSpinBox()
        self.Numberso.setFixedWidth(50)
        self.Numberso.setValue(0)
        self.Numberso.setMinimum(-1000)
        self.Numberso.setMaximum(1000)
        self.Numberso.setSingleStep(10)
        self.Numberso.valueChanged.connect(lambda: self.clickspinbox("S0"))
        gridLayout3.addWidget(self.Numberso, 0, 3)
        #Para sx
        Labelsx = QLabel("sx(0, 1000)")
        Labelsx.setFixedWidth(80)
        gridLayout3.addWidget(Labelsx, 1, 0)

        self.Numbersx = QSpinBox()
        self.Numbersx.setFixedWidth(50)
        self.Numbersx.setValue(350)
        self.Numbersx.setMinimum(0)
        self.Numbersx.setMaximum(1000)
        self.Numbersx.setSingleStep(1)
        self.Numbersx.valueChanged.connect(lambda: self.clickspinbox("Sx"))
        gridLayout3.addWidget(self.Numbersx, 1, 1)
        #Para sy
        Labelsy = QLabel("sy(0, 1000)")
        Labelsy.setFixedWidth(80)
        gridLayout3.addWidget(Labelsy, 1, 2)

        self.Numbersy = QSpinBox()
        self.Numbersy.setFixedWidth(50)
        self.Numbersy.setValue(int(self.fsy))
        self.Numbersy.setMinimum(0)
        self.Numbersy.setMaximum(1000)
        self.Numbersy.setSingleStep(1)
        self.Numbersy.valueChanged.connect(lambda: self.clickspinbox("Sy"))
        gridLayout3.addWidget(self.Numbersy, 1, 3)
        #Para ox
        Labelox = QLabel("ox(0, 1000)")
        Labelox.setFixedWidth(80)
        gridLayout3.addWidget(Labelox, 2, 0)

        self.Numberox = QSpinBox()
        self.Numberox.setFixedWidth(50)
        self.Numberox.setValue(int(self.ox))
        self.Numberox.setMinimum(0)
        self.Numberox.setMaximum(1000)
        self.Numberox.setSingleStep(10)
        self.Numberox.valueChanged.connect(lambda: self.clickspinbox("Ox"))
        gridLayout3.addWidget(self.Numberox, 2, 1)
        #Para oy
        Labeloy = QLabel("oy(0, 500)")
        Labeloy.setFixedWidth(80)
        gridLayout3.addWidget(Labeloy, 2, 2)

        self.Numberoy = QSpinBox()
        self.Numberoy.setFixedWidth(50)
        self.Numberoy.setValue(int(self.oy))
        self.Numberoy.setMinimum(0)
        self.Numberoy.setMaximum(500)
        self.Numberoy.setSingleStep(10)
        self.Numberoy.valueChanged.connect(lambda: self.clickspinbox("Oy"))
        gridLayout3.addWidget(self.Numberoy, 2, 3)

        #Plotando em 3D --Grupo
        gridLayout3d = QGridLayout()
        group_3d.setLayout(gridLayout3d)
        #Plotando a casa
        self.ax1.clear()
        self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
        self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
        draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
        self.canvas = FigureCanvas(self.fig1)
        gridLayout3d.addWidget(self.canvas)

        #Plotando em 2D --Grupo
        gridLayout2d = QGridLayout()
        group_2d.setLayout(gridLayout2d)
        self.fig2, self.ax2 = plt.subplots()
        self.canvas2 = FigureCanvas(self.fig2)
        self.ax2.plot(self.imgCASA[0,:], self.imgCASA[1,:],'red')
        self.ax2.set_xlim([0,1280])
        self.ax2.set_ylim([720,0])
        self.ax2.grid('True')
        gridLayout2d.addWidget(self.canvas2, 0, 0)

        #Definindo o Tamanho das Colunas do Layout
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        #Fim das Definições do Layout
        self.setLayout(layout)

    #Ações dos botoes de Reset
    def clickbutton2(self, action):
        #Reseta Parametros Intrinsecos
        if action == "reset parameter":

            self.Numberf.setValue(100)
            self.Numbersx.setValue(int(3))
            self.Numbersy.setValue(int(3))
            self.Numberso.setValue(int(0))
            self.Numberox.setValue(int(640))
            self.Numberoy.setValue(int(360))

        #Reseta a Posição
        elif action == "reset position":

            self.matriz_M = self.matriz_Mc
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)
            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))
            self.imgCASA = np.dot(self.p,self.house1)
            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([0,1280])
            self.ax2.set_ylim([720,0])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

    #Alterando os Parametros Intrinsecos 
    def clickspinbox(self, action):
        if action == "F":
            self.f = self.Numberf.value()

            self.fsx = self.sx*self.f
            self.fsy = self.sy*self.f
            self.matriz_K = np.array([[self.fsx,self.fs0,self.ox],[0,self.fsy,self.oy],[0,0,1]])
            
            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura
            
        elif action == "S0":
            self.fs0 = self.Numberso.value()
            self.fsx = self.sx*self.f
            self.fsy = self.sy*self.f
            self.matriz_K = np.array([[self.fsx,self.fs0,self.ox],[0,self.fsy,self.oy],[0,0,1]])

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura
            
        elif action == "Sx":
            self.sx = self.Numbersx.value()
            self.fsx = self.sx*self.f 
            self.matriz_K = np.array([[self.fsx,self.fs0,self.ox],[0,self.fsy,self.oy],[0,0,1]])
            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura 

        elif action == "Sy":
            self.sy = self.Numbersy.value()
            self.fsy = self.sy*self.f
            self.matriz_K = np.array([[self.fsx,self.fs0,self.ox],[0,self.fsy,self.oy],[0,0,1]])
            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura 

        elif action == "Ox":
            self.ox_old = self.ox
            self.ox = self.Numberox.value()
            self.dx = self.ox - self.ox_old
            self.matriz_K = np.array([[self.fsx,self.fs0,self.ox],[0,self.fsy,self.oy],[0,0,1]])
            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.xlimup += self.dx
            self.xlimbt += self.dx
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura 


        elif action == "Oy":
            self.oy_old = self.oy
            self.oy = self.Numberoy.value()
            self.dy = self.oy - self.oy_old
            self.matriz_K = np.array([[self.fsx,self.fs0,self.ox],[0,self.fsy,self.oy],[0,0,1]]) 
            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ylimup += self.dy
            self.ylimbt += self.dy
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')             

            self.canvas2.draw()  # Redesenha a figura 

    #Açoes da camera no mundo
    def clickbutton(self, action):
        #Reseta Parametros Intrinsecos
        if action == "Xtm":
            self.matriz_M = np.dot(move(1,0,0),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura


        elif action == "Xtme":
            self.matriz_M = np.dot(move(-1,0,0),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "Ytm":
            self.matriz_M = np.dot(move(0,1,0),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "Ytme":
            self.matriz_M = np.dot(move(0,-1,0),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)


            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "Ztm":
            self.matriz_M = np.dot(move(0,0,1),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "Ztme":
            self.matriz_M = np.dot(move(0,0,-1),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "Xrm":
            self.matriz_M = np.dot(rotx(pi/90),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "Xrme":
            self.matriz_M = np.dot(rotx(-pi/90),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)


            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "Yrm":
            self.matriz_M = np.dot(roty(pi/90),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "Yrme":
            self.matriz_M = np.dot(roty(-pi/90),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()
            
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "Zrm":
            self.matriz_M = np.dot(rotz(pi/90),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()
            
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "Zrme":
            self.matriz_M = np.dot(rotz(-pi/90),self.matriz_M)

            self.nova_cam = np.dot(self.matriz_M,self.cam)

            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cXrm":
            self.matriz_M = np.dot(self.matriz_M, np.dot(rotx(pi/90),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cXrme":
            self.matriz_M = np.dot(self.matriz_M, np.dot(rotx(-pi/90),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cYrm":
            self.matriz_M = np.dot(self.matriz_M, np.dot(roty(pi/90),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cYrme":
            self.matriz_M = np.dot(self.matriz_M, np.dot(roty(-pi/90),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cZrm":
            self.matriz_M = np.dot(self.matriz_M, np.dot(rotz(pi/90),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cZrme":
            self.matriz_M = np.dot(self.matriz_M, np.dot(rotz(-pi/90),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()
            
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cXtm":
            self.matriz_M = np.dot(self.matriz_M, np.dot(move(1,0,0),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cXtme":
            self.matriz_M = np.dot(self.matriz_M, np.dot(move(-1,0,0),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cYtm":
            self.matriz_M = np.dot(self.matriz_M, np.dot(move(0,1,0),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()
            
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cYtme":
            self.matriz_M = np.dot(self.matriz_M, np.dot(move(0,-1,0),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cZtm":
            self.matriz_M = np.dot(self.matriz_M, np.dot(move(0,0,1),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()
            
            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura

        elif action == "cZtme":
            self.matriz_M = np.dot(self.matriz_M, np.dot(move(0,0,-1),np.dot(self.inv_M, self.matriz_M)))
            self.nova_cam = np.dot(self.matriz_M,self.cam)
            self.inv_M = np.linalg.inv(self.matriz_M)

            self.p = np.dot(self.matriz_K,np.dot(self.z,self.inv_M))

            self.imgCASA = np.dot(self.p,self.house1)

            self.ax1.clear()
            self.ax1 = set_plot(ax=self.ax1,lim=[-15,30])
            self.ax1.plot3D(self.house[0,:], self.house[1,:], self.house[2,:],'red')
            draw_arrows(self.nova_cam[:,-1], self.nova_cam[:,0:3],self.ax1)
            self.canvas.draw()

            self.imgCASA[0,:] = self.imgCASA[0,:]/self.imgCASA[2,:]
            self.imgCASA[1,:] = self.imgCASA[1,:]/self.imgCASA[2,:]
            self.imgCASA[2,:] = self.imgCASA[2,:]/self.imgCASA[2,:]

            self.ax2.clear()
            self.ax2.plot(self.imgCASA[0,:],self.imgCASA[1,:],'red')
            self.ax2.set_xlim([self.xlimbt,self.xlimup])
            self.ax2.set_ylim([self.ylimup, self.ylimbt])
            self.ax2.grid('True')            

            self.canvas2.draw()  # Redesenha a figura
    #Para deixar o texto em Negrito
    def setFontBold(self, widget):
        font = widget.font()
        font.setBold(True)
        widget.setFont(font)

if __name__ == "__main__":
    app = QApplication([])
    ex = App()
    ex.show()
    sys.exit(app.exec_())