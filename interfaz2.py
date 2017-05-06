# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfazProyecto.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from lectura import Lectura
from escritura import Escritura
from graficador import Grafica
import sys

LIM = 100


# Link: http://www.boxcontrol.net/embedding-matplotlib-plot-on-pyqt5-gui.html
class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.resetValues()
        return

    def setPuerto(self, puerto):
        self.puerto = puerto
        return

    def resetValues(self):
        self.values = []
        self.i = 0
        self.setPuerto(None)
        self.lectura = None
        return

    def resetDrawing(self):
        self.resetValues()
        self.compute_initial_figure()
        return

    def compute_initial_figure(self):
        self.x, self.y = [], []
        for i in range(0, LIM + 1):
            self.x.append(i)
            self.y.append(0)
        self.axes.plot(self.x, self.y, 'r')
        return

    def update_figure(self):
        if self.puerto is not None:
            self.lectura = Lectura(self.puerto)
            self.puerto = None
        if self.lectura is not None:
            value = self.lectura.leer()
            self.values.append(value)
        if self.i < len(self.values):
            elem = self.values[self.i]
            self.y.append(elem)
            self.y.pop(0)
            self.i += 1
            self.axes.plot(self.x, self.y, 'r')
            self.draw()
        return


class Ui_mainWindow(object):
    val = 0

    def __init__(self):
        self.values = []
        return

    def definirGraficas(self):
        self.grafica = QVBoxLayout(self.frame)
        self.graficarLeyendo = MyDynamicMplCanvas(self.frame, width=5, height=4, dpi=100)
        self.grafica.addWidget(self.graficarLeyendo)
        return

    def accionesBotones(self):
        self.pushButton.clicked.connect(self.accionIniciar)
        self.pushButton_2.clicked.connect(self.accionParar)
        return

    def accionIniciar(self):
        archivo = self.txt_archivo.toPlainText()
        puerto = self.txt_puerto.toPlainText()

        if puerto != '' and archivo != '' and archivo.endswith('.csv'):
            self.graficarLeyendo.setPuerto(puerto)
            self.graficarLeyendo.timer.start()
        return

    def accionParar(self):
        archivo = self.txt_archivo.toPlainText()
        self.graficarLeyendo.lectura.doAtExit()
        self.graficarLeyendo.timer.stop()
        self.values = self.graficarLeyendo.values
        self.graficarLeyendo.resetDrawing()

        if archivo != '' and archivo.endswith('.csv'):
            Escritura(self.values, archivo).escribir()

            frecuencia = 100  # Hz
            bpm, ibi, sdnn, sdsd, rmssd, pnn20, pnn50 = Grafica(archivo, frecuencia).procesar()
            self.txt_bpm.setText(str(bpm))
            self.txt_ibi.setText(str(ibi))
            self.txt_sdnn.setText(str(sdnn))
            self.txt_sdsd.setText(str(sdsd))
            self.txt_rmssd.setText(str(rmssd))
            self.txt_pnn20.setText(str(pnn20))
            self.txt_pnn50.setText(str(pnn50))
        return

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1054, 622)
        mainWindow.setStyleSheet("background-color: rgb(107, 107, 107);")
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 70, 491, 411))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.grupoConfiguracion = QtWidgets.QGroupBox(self.centralwidget)
        self.grupoConfiguracion.setGeometry(QtCore.QRect(510, 430, 531, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.grupoConfiguracion.setFont(font)
        self.grupoConfiguracion.setStyleSheet("color: rgb(241, 241, 241);")
        self.grupoConfiguracion.setObjectName("grupoConfiguracion")
        self.lbl_puerto = QtWidgets.QLabel(self.grupoConfiguracion)
        self.lbl_puerto.setGeometry(QtCore.QRect(20, 30, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_puerto.setFont(font)
        self.lbl_puerto.setObjectName("lbl_puerto")
        self.txt_puerto = QtWidgets.QTextEdit(self.grupoConfiguracion)
        self.txt_puerto.setGeometry(QtCore.QRect(70, 30, 111, 41))
        self.txt_puerto.setObjectName("txt_puerto")
        self.lbl_archivo = QtWidgets.QLabel(self.grupoConfiguracion)
        self.lbl_archivo.setGeometry(QtCore.QRect(190, 30, 61, 16))
        self.lbl_archivo.setObjectName("lbl_archivo")
        self.txt_archivo = QtWidgets.QTextEdit(self.grupoConfiguracion)
        self.txt_archivo.setGeometry(QtCore.QRect(250, 30, 271, 41))
        self.txt_archivo.setObjectName("txt_archivo")
        self.grupoIndicadores = QtWidgets.QGroupBox(self.centralwidget)
        self.grupoIndicadores.setGeometry(QtCore.QRect(550, 80, 431, 311))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.grupoIndicadores.setFont(font)
        self.grupoIndicadores.setStyleSheet("color: rgb(243, 243, 243);")
        self.grupoIndicadores.setObjectName("grupoIndicadores")
        self.lbl_bpm = QtWidgets.QLabel(self.grupoIndicadores)
        self.lbl_bpm.setGeometry(QtCore.QRect(90, 30, 47, 13))
        self.lbl_bpm.setObjectName("lbl_bpm")
        self.lbl_ibi = QtWidgets.QLabel(self.grupoIndicadores)
        self.lbl_ibi.setGeometry(QtCore.QRect(90, 70, 47, 13))
        self.lbl_ibi.setObjectName("lbl_ibi")
        self.lbl_sdnn = QtWidgets.QLabel(self.grupoIndicadores)
        self.lbl_sdnn.setGeometry(QtCore.QRect(90, 110, 47, 13))
        self.lbl_sdnn.setObjectName("lbl_sdnn")
        self.lbl_sdsd = QtWidgets.QLabel(self.grupoIndicadores)
        self.lbl_sdsd.setGeometry(QtCore.QRect(90, 150, 47, 13))
        self.lbl_sdsd.setObjectName("lbl_sdsd")
        self.lbl_rmssd = QtWidgets.QLabel(self.grupoIndicadores)
        self.lbl_rmssd.setGeometry(QtCore.QRect(90, 190, 61, 16))
        self.lbl_rmssd.setObjectName("lbl_rmssd")
        self.lbl_pnn20 = QtWidgets.QLabel(self.grupoIndicadores)
        self.lbl_pnn20.setGeometry(QtCore.QRect(90, 230, 61, 16))
        self.lbl_pnn20.setObjectName("lbl_pnn20")
        self.lbl_pnn50 = QtWidgets.QLabel(self.grupoIndicadores)
        self.lbl_pnn50.setGeometry(QtCore.QRect(90, 270, 61, 16))
        self.lbl_pnn50.setObjectName("lbl_pnn50")
        self.txt_bpm = QtWidgets.QTextEdit(self.grupoIndicadores)
        self.txt_bpm.setEnabled(False)
        self.txt_bpm.setGeometry(QtCore.QRect(150, 30, 181, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.txt_bpm.setFont(font)
        self.txt_bpm.setStyleSheet("color: rgb(255, 255, 255);")
        self.txt_bpm.setObjectName("txt_bpm")
        self.txt_ibi = QtWidgets.QTextEdit(self.grupoIndicadores)
        self.txt_ibi.setEnabled(False)
        self.txt_ibi.setGeometry(QtCore.QRect(150, 70, 181, 31))
        self.txt_ibi.setStyleSheet("color: rgb(255, 255, 255);")
        self.txt_ibi.setObjectName("txt_ibi")
        self.txt_sdnn = QtWidgets.QTextEdit(self.grupoIndicadores)
        self.txt_sdnn.setEnabled(False)
        self.txt_sdnn.setGeometry(QtCore.QRect(150, 110, 181, 31))
        self.txt_sdnn.setStyleSheet("color: rgb(255, 255, 255);")
        self.txt_sdnn.setObjectName("txt_sdnn")
        self.txt_sdsd = QtWidgets.QTextEdit(self.grupoIndicadores)
        self.txt_sdsd.setEnabled(False)
        self.txt_sdsd.setGeometry(QtCore.QRect(150, 150, 181, 31))
        self.txt_sdsd.setStyleSheet("color: rgb(255, 255, 255);")
        self.txt_sdsd.setObjectName("txt_sdsd")
        self.txt_rmssd = QtWidgets.QTextEdit(self.grupoIndicadores)
        self.txt_rmssd.setEnabled(False)
        self.txt_rmssd.setGeometry(QtCore.QRect(150, 190, 181, 31))
        self.txt_rmssd.setStyleSheet("color: rgb(255, 255, 255);")
        self.txt_rmssd.setObjectName("txt_rmssd")
        self.txt_pnn20 = QtWidgets.QTextEdit(self.grupoIndicadores)
        self.txt_pnn20.setEnabled(False)
        self.txt_pnn20.setGeometry(QtCore.QRect(150, 230, 181, 31))
        self.txt_pnn20.setStyleSheet("color: rgb(255, 255, 255);")
        self.txt_pnn20.setObjectName("txt_pnn20")
        self.txt_pnn50 = QtWidgets.QTextEdit(self.grupoIndicadores)
        self.txt_pnn50.setEnabled(False)
        self.txt_pnn50.setGeometry(QtCore.QRect(150, 270, 181, 31))
        self.txt_pnn50.setStyleSheet("color: rgb(255, 255, 255);")
        self.txt_pnn50.setObjectName("txt_pnn50")
        self.numero_BPM = QtWidgets.QLCDNumber(self.grupoIndicadores)
        self.numero_BPM.setGeometry(QtCore.QRect(340, 30, 81, 31))
        self.numero_BPM.setProperty("intValue", 7866)
        self.numero_BPM.setObjectName("numero_BPM")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 550, 131, 41))
        self.pushButton.setStyleSheet("background-color: rgb(85, 170, 0);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 550, 131, 41))
        self.pushButton_2.setStyleSheet("background-color: rgb(214, 0, 0);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.lbl_titulo = QtWidgets.QLabel(self.centralwidget)
        self.lbl_titulo.setGeometry(QtCore.QRect(10, 10, 1031, 31))
        font = QtGui.QFont()
        font.setPointSize(23)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_titulo.setFont(font)
        self.lbl_titulo.setStyleSheet("color: rgb(239, 239, 239);")
        self.lbl_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_titulo.setObjectName("lbl_titulo")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        self.definirGraficas()
        self.accionesBotones()
        return

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Monitor de Frecuencia Cardiaca"))
        self.grupoConfiguracion.setTitle(_translate("mainWindow", "Configuracion"))
        self.lbl_puerto.setText(_translate("mainWindow", "Puerto:"))
        self.txt_puerto.setPlaceholderText(_translate("mainWindow", "COM5"))
        self.lbl_archivo.setText(_translate("mainWindow", "Archivo:"))
        self.txt_archivo.setPlaceholderText(_translate("mainWindow", "nombreArchivo.csv"))
        self.grupoIndicadores.setTitle(_translate("mainWindow", "Indicadores"))
        self.lbl_bpm.setText(_translate("mainWindow", "BPM:"))
        self.lbl_ibi.setText(_translate("mainWindow", "IBI:"))
        self.lbl_sdnn.setText(_translate("mainWindow", "SDNN: "))
        self.lbl_sdsd.setText(_translate("mainWindow", "SDSD:"))
        self.lbl_rmssd.setText(_translate("mainWindow", "RMSSD:"))
        self.lbl_pnn20.setText(_translate("mainWindow", "PNN20:"))
        self.lbl_pnn50.setText(_translate("mainWindow", "PNN50:"))
        self.txt_bpm.setHtml(_translate("mainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:italic;\">\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton.setText(_translate("mainWindow", "Iniciar Lecturas"))
        self.pushButton_2.setText(_translate("mainWindow", "Detener Lecturas"))
        self.lbl_titulo.setText(_translate("mainWindow", "Monitor de frecuencia cardiaca"))
        return
