from PyQt5 import QtCore
#from interfaz2 import U
class ThreadClass(QtCore.QThread):
    #el parametro que se pasa aqui, es el parametro que recibe el metodo de la señal, en este caso actualizar recibe un float
    sig = QtCore.pyqtSignal(float)

    def __init__(self, parent= None, ):
        super(ThreadClass,self).__init__(parent)
        #COnectar la señal a la funcion deseada
        self.sig.connect(Ui_mainWindow.actualizarIndicadores)
        #self.serial0 = serial.Serial('COM5', 9600)

    def run(self):
        while True:
            print ("HOLA")
            self.sig.emit(1)