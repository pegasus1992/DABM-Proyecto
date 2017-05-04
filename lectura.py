import serial
import matplotlib.pyplot as plt
import atexit


class Lectura():
    def __init__(self):
        self.serialArduino = serial.Serial('COM4', 9600)
        return

    def doAtExit(self):
        self.serialArduino.close()
        print("Puerto cerrado")
        print("serialArduino.isOpen() = " + str(self.serialArduino.isOpen()))
        return

    # Lee y grafica en tiempo real.
    def leer(self, numLecturas):
        atexit.register(self.doAtExit)
        print("serialArduino.isOpen() = " + str(self.serialArduino.isOpen()))

        values, i = [], 0
        while i <= numLecturas:
            while self.serialArduino.inWaiting() == 0:
                pass

            valueRead = self.serialArduino.readline()
            valuefloat = float(valueRead)
            # print(valuefloat)
            values.append(valuefloat)

            i += 1
        return values
