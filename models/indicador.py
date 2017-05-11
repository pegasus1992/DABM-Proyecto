import pandas as pd
import numpy as np
import math

AJUSTE = 1.2


class Indicadores:
    def __init__(self, frecuencia, dataset):
        self.frecuencia = frecuencia
        self.dataset = dataset
        self.bpm = 0
        self.ibi = 0
        self.sdnn = 0
        self.sdsd = 0
        self.rmssd = 0
        self.pnn20 = 0
        self.pnn50 = 0
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

    # SDSD = Desviacion estandar de las diferencias entre los intervalos de los picos
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

    # RMSSD = Raiz cuadrada del promedio de las diferencias entre los intervalos de los picos
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

    # pNN20 o pNN50 (pNNxx)
    def getPnn(self, maximos, factor):
        numeros = self.getNn(maximos, factor)
        if len(maximos) == 0:
            return 0
        else:
            return len(numeros) / len(maximos)

    def procesar(self):
        promedio = self.getPromedio()
        promedioDinamico = self.getPromedioDinamico(promedio)
        maximos = self.getMaximos(promedioDinamico)

        maximosy = [self.dataset.hart[x] for x in maximos]

        self.bpm = self.getBpm(maximos)
        self.ibi = self.getIbi(maximos)
        self.sdnn = self.getSdnn(maximos)
        self.sdsd = self.getSdsd(maximos)
        self.rmssd = self.getRmssd(maximos)
        self.pnn20 = self.getPnn(maximos, 20)
        self.pnn50 = self.getPnn(maximos, 50)
        return

    def getIndicadores(self):
        return self.bpm, self.ibi, self.sdnn, self.sdsd, self.rmssd, self.pnn20, self.pnn50
