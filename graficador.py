import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

AJUSTE = 1.2


class Grafica():
    def __init__(self, archivo, frecuencia):
        self.dataset = pd.read_csv(archivo)
        self.frecuencia = frecuencia
        return

    def getPromedio(self):
        return np.mean(self.dataset.hart)

    def getPromedioDinamico(self, promedio):
        promedioDinamico = pd.rolling_mean(self.dataset.hart, window=self.frecuencia)
        promedioDinamico = [promedio if math.isnan(x) else x for x in promedioDinamico]
        promedioDinamico = [x * AJUSTE for x in promedioDinamico]
        return promedioDinamico

    def getMaximos(self, promedioDinamico):
        self.dataset['promedio'] = promedioDinamico
        i, rango, maximos = 0, [], []
        for punto in self.dataset.hart:
            promedio = self.dataset.promedio[i]
            if punto <= promedio and len(rango) < 1:
                i += 1
            elif punto > promedio:
                rango.append(punto)
                i += 1
            else:
                maximo = max(rango)
                posicion = i - len(rango) + rango.index(maximo)
                maximos.append(posicion)
                rango = []
                i += 1
        return maximos

    # BPM = Beats por minuto.
    def getBpm(self, maximos):
        i, distancia = 0, []
        while i < len(maximos) - 1:
            intervalo = maximos[i + 1] - maximos[i]
            intervalo /= self.frecuencia
            distancia.append(intervalo)
            i += 1
        return 60 / np.mean(distancia)

    def getDistanciasEntrePicos(self, maximos):
        i, distancias = 0, []
        while i < len(maximos) - 1:
            distancias.append(maximos[i + 1] - maximos[i])
            i += 1
        return distancias

    # IBI = Promedio de las distancias entre picos.
    def getIbi(self, maximos):
        distancias = self.getDistanciasEntrePicos(maximos)
        return np.mean(distancias) / 100

    # SDNN = Desviacion estandar de las distancias entre picos.
    def getSdnn(self, maximos):
        distancias = self.getDistanciasEntrePicos(maximos)
        return np.std(distancias) / 100

    def getDiferenciasIntervalosPicos(self, maximos):
        distancias = self.getDistanciasEntrePicos(maximos)
        i, diferencias = 0, []
        while i < len(distancias) - 1:
            diferencia = abs(self.dataset.hart[distancias[i + 1]] - self.dataset.hart[distancias[i]])
            diferencias.append(diferencia)
            i += 1
        return diferencias

    def getSdsd(self, maximos):
        diferencias = self.getDiferenciasIntervalosPicos(maximos)
        return np.std(diferencias) / 100

    def getDiferenciasCuadradosIntervalosPicos(self, maximos):
        distancias = self.getDistanciasEntrePicos(maximos)
        i, diferencias = 0, []
        while i < len(distancias) - 1:
            diferencia = math.pow(self.dataset.hart[distancias[i + 1]] - self.dataset.hart[distancias[i]], 2)
            diferencias.append(diferencia)
            i += 1
        return diferencias

    def getRmssd(self, maximos):
        diferencias = self.getDiferenciasIntervalosPicos(maximos)
        return np.sqrt(np.mean(diferencias)) / 100

    def getNn(self, maximos, factor):
        diferencias = self.getDiferenciasIntervalosPicos(maximos)
        numeros = []
        for elem in diferencias:
            if elem > factor:
                numeros.append(elem)
        return numeros

    def getPnn(self, maximos, factor):
        numeros = self.getNn(maximos, factor)
        if len(maximos)==0:
            return 0
        else:
            return len(numeros) / len(maximos)

    def procesar(self):
        promedio = self.getPromedio()
        promedioDinamico = self.getPromedioDinamico(promedio)
        maximos = self.getMaximos(promedioDinamico)

        maximosy = [self.dataset.hart[x] for x in maximos]

        bpm = self.getBpm(maximos)
        ibi = self.getIbi(maximos)
        sdnn = self.getSdnn(maximos)
        sdsd = self.getSdsd(maximos)
        rmssd = self.getRmssd(maximos)
        pnn20 = self.getPnn(maximos, 20)
        pnn50 = self.getPnn(maximos, 50)

        plt.title("Frecuencia cardiaca")
        plt.plot(self.dataset.hart, color="red", label="Frecuencia")
        plt.plot(promedioDinamico, color="blue", label="Promedio")
        plt.scatter(maximos, maximosy, color="green", label="Frecuencia es %0.01f" % bpm)

        vacio, alpha = [], 0
        plt.scatter(vacio, vacio, alpha=alpha, label="IBI: %s" % ibi)
        plt.scatter(vacio, vacio, alpha=alpha, label="SDNN: %s" % sdnn)
        plt.scatter(vacio, vacio, alpha=alpha, label="SDSD: %s" % sdsd)
        plt.scatter(vacio, vacio, alpha=alpha, label="RMSSD: %s" % rmssd)
        plt.scatter(vacio, vacio, alpha=alpha, label="pNN20: %0.1f" % pnn20)
        plt.scatter(vacio, vacio, alpha=alpha, label="pNN50: %0.1f" % pnn50)

        plt.legend(loc=4, framealpha=0.7)
        plt.show()

        return bpm, ibi, sdnn, sdsd, rmssd, pnn20, pnn50