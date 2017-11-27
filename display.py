import sys
import random
import std_path
import readin
import ga_pbd
#import fgn_2_main
import sa
#import hill_climbing_main
#import hc
#这里要import原主函数里的“头文件”
import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

mode1 = 'sa_initial'
mode2 = 'ga_initial'

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyStaticMplCanvas(MyMplCanvas):
    def compute_initial_figure(self):
        opt_tour = std_path.read_std_path()
        opt_tour.append(opt_tour[0])
        lf_title = "The Standard Path"
        self.axes.scatter(*zip(*opt_tour))
        self.axes.plot(*zip(*opt_tour))
        self.axes.set_title(lf_title)

class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, mywork = 'sa',*args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(10)
        self.mywork = mywork
        self.obj = sa.Sa(r"data\eil101.tsp")
        self.obh = ga_pbd.GA(r"data\eil101.tsp")

    def compute_initial_figure(self):
        self.axes.plot(readin.readin()[1])

    def update_figure(self,opt_tour = std_path.read_std_path(),dif = 1):
        global mode1
        global mode2
        if self.mywork == 'sa':
            if mode1 == 'null':
                self.obj = sa.Sa(r"data\eil101.tsp")
                path = std_path.read_ini_path()
                path.append(path[0])
            elif mode1 == 'sa_initial':
                self.obj = sa.Sa(r"data\eil101.tsp")
                path = std_path.read_ini_path()
                path.append(path[0])
                dif = self.obj.get_dif()
                #mode = 'sa_run'
            elif mode1 == 'sa_run':
                path = self.obj.next()
                path.append(path[0])
                dif = self.obj.get_dif()
            lf_title = "SA Deviation degree:" + str(round(dif*100,2)) + '%'
        else:
            if mode2 == 'null':
                path = std_path.read_ini_path()
                path.append(path[0])
            elif mode2 == 'ga_initial':
                self.obh = ga_pbd.GA()
                path = std_path.read_ini_path()
                path.append(path[0])
                ob = sa.Sa(r"data\eil101.tsp")
                dif = ob.get_dif()
            elif mode2 == 'ga_run':
                path,dif = self.obh.next_()
            lf_title = "GA Deviation degree:" + str(round(dif*100,2)) + '%'

        self.axes.scatter(*zip(*path))
        self.axes.plot(*zip(*path))
        self.axes.set_title(lf_title)
        self.draw()

class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("程序主窗口")

        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QWidget(self)

        l = QGridLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas('sa',self.main_widget, width=5, height=4, dpi=100)
        ec = MyDynamicMplCanvas('ga',self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc,0,0)
        l.addWidget(dc,0,1)
        l.addWidget(ec,1,1)



        #启动按钮
        self.btn3 = QPushButton("LET'S ROCK ON!!!", self)
        self.btn3.resize(self.btn3.sizeHint())
        #这里改成启动程序
        self.btn3.clicked.connect(set_start)
        l.addWidget(self.btn3,1,0)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        # 状态条显示2秒
        #self.statusBar().showMessage("matplotlib 万岁!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QMessageBox.about(self, "About", "no about")

def set_sa_initial():
    global mode1
    mode1 = 'sa_initial'

def set_hc_initial():
    global mode2
    mode2 = 'ga_initial'

def set_start():
    global mode1,mode2
    if mode1 == 'sa_initial':
        mode1 = 'sa_run'
    if mode2 == 'ga_initial':
        mode2 = 'ga_run'


if __name__ == '__main__':
    app = QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.setWindowTitle("show path")
    aw.show()
    #sys.exit(qApp.exec_())
    app.exec_()
