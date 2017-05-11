import matplotlib.pyplot as plt


class Graficador:
    def graficar(self, values):
        plt.title("Frecuencia cardiaca")
        plt.plot(values, color="red", label="Frecuencia")

        plt.legend(loc=4, framealpha=0.7)
        plt.show()
        return
