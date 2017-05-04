import pandas as pd


class Escritura():
    def __init__(self, values, archivo):
        self.values = values
        self.archivo = archivo
        return

    # Escribe en un archivo dado (en formato CSV).
    def escribir(self):
        df = pd.DataFrame({'hart': self.values})
        df.to_csv(self.archivo, index=False, sep='\t')
        return
