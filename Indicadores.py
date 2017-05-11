import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

class Indicadores():

    def __init__(self, frecuencia, dataSet):
        self.dataSet = dataSet
        self.frecuencia = frecuencia
        self.IBI = 0
        self.SDNN = 0
        self.SDSD = 0
        self.RMSSD = 0
        self.pNN20 = 0
        self.pNN50 = 0
        self.BPM = 0

    def asignarDataSet(self, arreglo):
        self.dataSet = arreglo

    #Metodo encargado de traer el promedio de los datos del dataSet
    def traerPromedioDataSet(self):
        return np.mean(self.dataSet.hart)

    #Metodo encargado de traer el promedio dinamico del dataSet
    def traerYAsignarPromedioDinamico(self, promedio, valorAumentar):
        promedio_dinamico =  pd.rolling_mean(self.dataSet.hart, window=(self.frecuencia))
        promedio_dinamico = [promedio if math.isnan(x) else x for x in promedio_dinamico]
        promedio_dinamico = [x * valorAumentar for x in promedio_dinamico]
        self.dataSet['promedio'] = promedio_dinamico
        return promedio_dinamico

    #Metodo encargado de traer los maximos
    def traerMaximos(self):
        cont = 0
        rango = []
        maximos = []
        for punto in self.dataSet.hart:
            promedio1 = self.dataSet.promedio[cont]
            if punto <= promedio1 and (len(rango) < 1):
                cont += 1
            elif punto > promedio1:
                rango.append(punto)
                cont += 1
            else:
                maximo = max(rango)
                posicion = cont - len(rango) + rango.index(maximo)
                maximos.append(posicion)
                rango = []
                cont += 1

        return maximos

    #Metodo encargado de traer los maximos en Y
    def traerMaximosEnY(self, maximos):
        maximosY = [self.dataSet.hart[x] for x in maximos]
        return maximosY

    #Metodo encargado de traer las distancias entre picos
    def traerDistanciaEntrePicos(self, maximos):
        cont = 0
        dist = []
        while cont < len(maximos) - 1:
            intervalo = float(maximos[cont + 1] - maximos[cont])
            intervalo = float(intervalo / self.frecuencia)
            dist.append(intervalo)
            cont += 1
        return dist

    #Metodo encargado de traer los BPM
    def calcularBPMPromedio(self, distanciaEntrePicos):
        bpm = 60 / np.mean(distanciaEntrePicos)
        self.BPM = bpm
        return bpm

    #MEtodo encargado de calcular todos los indicadores
    def calcularIndicadores(self, arregloDistancias):
        arregloDiferencias = []
        arregloRaizDiferencias = []

        contador = 0
        while (contador < (len(arregloDistancias) - 1)):
            arregloDiferencias.append(abs(arregloDistancias[contador] - arregloDistancias[contador + 1]))
            arregloRaizDiferencias.append(math.pow(arregloDistancias[contador] - arregloDistancias[contador + 1], 2))
            contador += 1

        self.IBI = np.mean(arregloDistancias)
        self.SDNN = np.std(arregloDistancias)
        self.SDSD = np.std(arregloDiferencias)
        self.RMSSD = np.sqrt(np.mean(arregloRaizDiferencias))

        nn20 = [x for x in arregloDiferencias if (x > 20)]
        nn50 = [x for x in arregloDiferencias if (x > 50)]
        self.pNN20 = float(len(nn20)) / float(len(arregloDiferencias))
        self.pNN50 = float(len(nn50)) / float(len(arregloDiferencias))


    #Metodo encargado de calcular los indicadores y graficar
    def ejecutar(self):
        promedio = self.traerPromedioDataSet()
        print ("Promedio",promedio)
        promedioDinamico = self.traerYAsignarPromedioDinamico(promedio, 1.2)
        print ("promedioDinamico",promedioDinamico)
        maximos = self.traerMaximos()
        print ("maximos",maximos)
        maximosY = self.traerMaximosEnY(maximos)
        print ("maximosY",maximosY)
        arregloDistancias = self.traerDistanciaEntrePicos(maximos)
        print ("arregloDistancias",arregloDistancias)
        frecuencia = self.calcularBPMPromedio(arregloDistancias)
        print ("frecuencia",frecuencia)
        self.calcularIndicadores(arregloDistancias)

    def traerIndicadores(self):
        return self.IBI, self.SDNN, self.SDSD, self.RMSSD, self.pNN20, self.pNN50, self.BPM