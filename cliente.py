from socket import socket
import pickle

from models.lectura import Lectura
from models.graficar import Graficador


def main():
    s = socket()
    s.connect(("localhost", 6030))

    while True:
        archivo = raw_input("> ")

        lectura = Lectura("COM4")
        values = []
        for i in range(500):
            value = lectura.leer()
            values.append(value)
        lectura.doAtExit()
        values_string = pickle.dumps(values)

        if archivo:
            # Enviar entrada. Comptabilidad con Python 3.
            try:
                s.send(archivo)
                s.send(values_string)
            except TypeError:
                s.send(bytes(archivo, "utf-8"))
                s.send(bytes(values_string, "utf-8"))
            else:
                # Recibir respuesta.
                BPM = s.recv(1024)
                IBI = s.recv(1024)
                SDNN = s.recv(1024)
                SDSD = s.recv(1024)
                RMSSD = s.recv(1024)
                pNN20 = s.recv(1024)
                pNN50 = s.recv(1024)
                if BPM and IBI and SDNN and SDSD and RMSSD and pNN20 and pNN50:
                    Graficador().graficar(values)


if __name__ == "__main__":
    main()
