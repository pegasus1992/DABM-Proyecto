from socket import socket, error
import pickle
import pandas as pd
import json
from threading import Thread

from models.escritura import Escritura
from models.graficador import Grafica
from models.Indicadores import Indicadores


# Link: http://stackoverflow.com/questions/24423162/how-to-send-an-array-over-a-socket-in-python
class Server(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        return

    def run(self):
        while True:
            try:
                # Recibir datos del cliente.
                archivo = self.conn.recv(2048).decode()
                values = pickle.loads(self.conn.recv(1500000))
            except error:
                print("[%s] Error de lectura." % self.name)
                break
            else:
                # Reenviar la informacion recibida.
                if archivo and values:
                    Escritura(values, archivo).escribir()

                    dataset = pd.read_csv(archivo)
                    indicadores = Indicadores(100, dataset)

                    indicadores.ejecutar()
                    bpm, ibi, sdnn, sdsd, rmssd, pnn20, pnn50 = indicadores.traerIndicadores()

                    self.conn.send(bytes(str(bpm), "utf-8"))
                    self.conn.send(bytes(str(ibi), "utf-8"))
                    self.conn.send(bytes(str(sdnn), "utf-8"))
                    self.conn.send(bytes(str(sdsd), "utf-8"))
                    self.conn.send(bytes(str(rmssd), "utf-8"))
                    self.conn.send(bytes(str(pnn20), "utf-8"))
                    self.conn.send(bytes(str(pnn50), "utf-8"))
        return


def main():
    s = socket()

    # Escuchar peticiones en el puerto 6030.
    s.bind(("", 6030))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        c = Server(conn, addr)
        c.start()
        print("%s:%d se ha conectado." % addr)


if __name__ == "__main__":
    main()
