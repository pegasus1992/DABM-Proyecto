# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaz.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from drawnow import *
from lectura import Lectura
from escritura import Escritura
from graficador import Grafica

LIM = 100


class Ui_MainWindow(object):
    def __init__(self):
        plt.ion()
        self.values = []
        return

    def accionesBotones(self):
        self.btn_lecturas.clicked.connect(self.accionIniciar)
        self.btn_indicadores.clicked.connect(self.accionIndicadores)
        return

    def accionIndicadores(self):
        archivo = self.txt_archivo.toPlainText()
        if archivo != '':
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

    def accionIniciar(self):
        cantidad = self.txt_cantidad.toPlainText()
        archivo = self.txt_archivo.toPlainText()

        if cantidad != '' and archivo != '':
            cantidad = int(cantidad)
            self.archivo = archivo
            self.values = Lectura().leer(cantidad)
            self.dibujarLectura(self.values)
            Escritura(self.values, self.archivo).escribir()
        return

    def dibujarLectura(self, valores):
        values, i = [], 0
        for i in range(0, LIM + 1):
            values.append(0)
        for elem in valores:
            values.append(elem)
            values.pop(0)
            drawnow(self.plotValues, False, False, values)
        plt.close()
        return

    def plotValues(self, values):
        plt.title("Serial value from Arduino")
        plt.grid(True)
        plt.ylabel("Values")
        plt.plot(values, 'rx-', label='values')
        plt.legend(loc='upper right')
        return

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 470, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(210, 90, 330, 100))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.lbl_cantidad = QtWidgets.QLabel(self.groupBox)
        self.lbl_cantidad.setGeometry(QtCore.QRect(20, 20, 80, 15))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lbl_cantidad.setFont(font)
        self.lbl_cantidad.setObjectName("label_2")
        self.lbl_archivo = QtWidgets.QLabel(self.groupBox)
        self.lbl_archivo.setGeometry(QtCore.QRect(20, 70, 70, 15))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lbl_archivo.setFont(font)
        self.lbl_archivo.setObjectName("label_3")
        self.txt_cantidad = QtWidgets.QTextEdit(self.groupBox)
        self.txt_cantidad.setGeometry(QtCore.QRect(120, 10, 190, 30))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.txt_cantidad.setFont(font)
        self.txt_cantidad.setObjectName("textEdit")
        self.txt_archivo = QtWidgets.QTextEdit(self.groupBox)
        self.txt_archivo.setGeometry(QtCore.QRect(120, 60, 190, 30))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.txt_archivo.setFont(font)
        self.txt_archivo.setObjectName("textEdit_2")

        lblY, lblWidth = 20, 30

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(210, 200, 330, 320))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.lbl_bpm = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_bpm.setGeometry(QtCore.QRect(20, lblY, 80, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lbl_bpm.setFont(font)
        self.lbl_bpm.setObjectName("label_4")
        self.txt_bpm = QtWidgets.QTextEdit(self.groupBox_2)
        self.txt_bpm.setEnabled(False)
        self.txt_bpm.setGeometry(QtCore.QRect(120, lblY, 190, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.txt_bpm.setFont(font)
        self.txt_bpm.setPlaceholderText("")
        self.txt_bpm.setObjectName("textEdit_3")
        self.txt_ibi = QtWidgets.QTextEdit(self.groupBox_2)
        self.txt_ibi.setEnabled(False)
        self.txt_ibi.setGeometry(QtCore.QRect(120, lblY * 3, 190, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.txt_ibi.setFont(font)
        self.txt_ibi.setPlaceholderText("")
        self.txt_ibi.setObjectName("textEdit_4")
        self.lbl_ibi = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_ibi.setGeometry(QtCore.QRect(20, lblY * 3, 80, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lbl_ibi.setFont(font)
        self.lbl_ibi.setObjectName("label_5")
        self.txt_sdnn = QtWidgets.QTextEdit(self.groupBox_2)
        self.txt_sdnn.setEnabled(False)
        self.txt_sdnn.setGeometry(QtCore.QRect(120, lblY * 5, 190, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.txt_sdnn.setFont(font)
        self.txt_sdnn.setPlaceholderText("")
        self.txt_sdnn.setObjectName("textEdit_5")
        self.lbl_sdnn = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_sdnn.setGeometry(QtCore.QRect(20, lblY * 5, 80, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lbl_sdnn.setFont(font)
        self.lbl_sdnn.setObjectName("label_6")
        self.txt_sdsd = QtWidgets.QTextEdit(self.groupBox_2)
        self.txt_sdsd.setEnabled(False)
        self.txt_sdsd.setGeometry(QtCore.QRect(120, lblY * 7, 190, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.txt_sdsd.setFont(font)
        self.txt_sdsd.setPlaceholderText("")
        self.txt_sdsd.setObjectName("textEdit_6")
        self.lbl_sdsd = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_sdsd.setGeometry(QtCore.QRect(20, lblY * 7, 80, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lbl_sdsd.setFont(font)
        self.lbl_sdsd.setObjectName("label_7")
        self.txt_rmssd = QtWidgets.QTextEdit(self.groupBox_2)
        self.txt_rmssd.setEnabled(False)
        self.txt_rmssd.setGeometry(QtCore.QRect(120, lblY * 9, 190, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.txt_rmssd.setFont(font)
        self.txt_rmssd.setPlaceholderText("")
        self.txt_rmssd.setObjectName("textEdit_7")
        self.lbl_rmssd = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_rmssd.setGeometry(QtCore.QRect(20, lblY * 9, 80, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lbl_rmssd.setFont(font)
        self.lbl_rmssd.setObjectName("label_8")
        self.txt_pnn20 = QtWidgets.QTextEdit(self.groupBox_2)
        self.txt_pnn20.setEnabled(False)
        self.txt_pnn20.setGeometry(QtCore.QRect(120, lblY * 11, 190, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.txt_pnn20.setFont(font)
        self.txt_pnn20.setPlaceholderText("")
        self.txt_pnn20.setObjectName("textEdit_8")
        self.lbl_pnn20 = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_pnn20.setGeometry(QtCore.QRect(20, lblY * 11, 80, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lbl_pnn20.setFont(font)
        self.lbl_pnn20.setObjectName("label_9")
        self.txt_pnn50 = QtWidgets.QTextEdit(self.groupBox_2)
        self.txt_pnn50.setEnabled(False)
        self.txt_pnn50.setGeometry(QtCore.QRect(120, lblY * 13, 190, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.txt_pnn50.setFont(font)
        self.txt_pnn50.setPlaceholderText("")
        self.txt_pnn50.setObjectName("textEdit_9")
        self.lbl_pnn50 = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_pnn50.setGeometry(QtCore.QRect(20, lblY * 13, 80, lblWidth))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.lbl_pnn50.setFont(font)
        self.lbl_pnn50.setObjectName("label_10")

        self.btn_lecturas = QtWidgets.QPushButton(self.centralwidget)
        self.btn_lecturas.setGeometry(QtCore.QRect(30, 100, 140, 80))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.btn_lecturas.setFont(font)
        self.btn_lecturas.setObjectName("pushButton")
        self.btn_indicadores = QtWidgets.QPushButton(self.centralwidget)
        self.btn_indicadores.setGeometry(QtCore.QRect(30, 210, 140, 80))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.btn_indicadores.setFont(font)
        self.btn_indicadores.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.accionesBotones()
        return

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Monitor de frecuencia cardíaca"))
        self.lbl_cantidad.setText(_translate("MainWindow", "Cantidad"))
        self.lbl_archivo.setText(_translate("MainWindow", "Archivo"))
        self.txt_cantidad.setPlaceholderText(_translate("MainWindow", "0"))
        self.txt_archivo.setPlaceholderText(_translate("MainWindow", "archivo.csv"))
        self.lbl_bpm.setText(_translate("MainWindow", "BPM"))
        self.lbl_ibi.setText(_translate("MainWindow", "IBI"))
        self.lbl_sdnn.setText(_translate("MainWindow", "SDNN"))
        self.lbl_sdsd.setText(_translate("MainWindow", "SDSD"))
        self.lbl_rmssd.setText(_translate("MainWindow", "RMSSD"))
        self.lbl_pnn20.setText(_translate("MainWindow", "pnn20"))
        self.lbl_pnn50.setText(_translate("MainWindow", "pnn50"))
        self.btn_lecturas.setText(_translate("MainWindow", "Iniciar lecturas"))
        self.btn_indicadores.setText(_translate("MainWindow", "Indicadores"))
        return
