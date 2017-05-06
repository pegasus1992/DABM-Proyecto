import serial
import matplotlib.pyplot as plt
import atexit


class Lectura():
    def __init__(self, port):
        self.serialArduino = serial.Serial(port, 9600)
        return

    def doAtExit(self):
        self.serialArduino.close()
        print("Puerto cerrado")
        print("serialArduino.isOpen() = " + str(self.serialArduino.isOpen()))
        return

    def leer(self):
        atexit.register(self.doAtExit)
        print("serialArduino.isOpen() = " + str(self.serialArduino.isOpen()))

        while self.serialArduino.inWaiting() == 0:
            pass
        valueRead = self.serialArduino.readline()
        value = int(float(valueRead))

        return value
