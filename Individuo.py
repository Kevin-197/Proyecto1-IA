import numpy as np
import cv2
import colour
import matplotlib.pyplot as plt
import random
import math

class Individuo:
    def __init__(self, l, w, opcion, generar):
        self.l = l
        self.w = w
        self.fitness = float('inf')
        self.imagen = None
        if generar == True:
            self.genera_imagen(opcion)

    def rand_color(self):
        color_hex = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        r = int(color_hex[1:3], 16)  # extrae los dos dígitos para el componente rojo y conviértelos a decimal
        g = int(color_hex[3:5], 16)  # extrae los dos dígitos para el componente verde y conviértelos a decimal
        b = int(color_hex[5:7], 16)  # extrae los dos dígitos para el componente azul y conviértelos a decimal

        color_bgr = (b, g, r)

        return color_bgr

    def genera_imagen(self, opcion):

        # cantidad de figuras que se agregaran
        cantidad = random.randint(3, 8)

        # delimitar region
        limite = (self.l + self.w) // 8

        
        img = np.full((self.w, self.l, 3), self.rand_color(), dtype=np.uint8)

        if opcion != 1:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        for _ in range(cantidad):
            num_puntos = random.randint(3, 6)
            region_x = random.randint(0, self.w)
            region_y = random.randint(0, self.l)

            puntos = []
            for _ in range(num_puntos):
                x = random.randint(region_x - limite, region_x + limite)
                y = random.randint(region_y - limite, region_y + limite)
                puntos.append((x,y))
            cv2.fillPoly(img, [np.array(puntos)], self.rand_color())

        self.imagen = img

    def get_fitness(self, target):
        # calcular la diferencia de color utilizando la métrica CIE 1976 (CIELAB)
        fit = colour.difference.delta_E_CIE1976(target, self.imagen)
        self.fitness = np.mean(fit)