import numpy as np
import cv2
from PIL import Image, ImageTk
from Individuo import Individuo
import random
import math
import os
import imageio
import matplotlib.pyplot as plt

class Genetico:
    def __init__(self, directorio, individuos, generaciones, seleccionados, mutacion_porcentaje, ratio_imagenes, grafico, graficocanvas, panel_imagen, imagen_generada, imagen_tk_generada, opcion):
        if not os.path.exists("imagenes"):
            os.mkdir("imagenes")

        self.target = cv2.imread(directorio)
        self.individuos = individuos
        self.generaciones = generaciones
        self.seleccionados = seleccionados
        self.mutacion_porcentaje = mutacion_porcentaje/100.0
        #print(self.mutacion_porcentaje)
        self.prob_cruce1 = (1-self.mutacion_porcentaje)/3
        #print(self.prob_cruce1)
        self.prob_cruce2 = self.prob_cruce1*2
        #print(self.prob_cruce2)
        self.ratio_imagenes = ratio_imagenes

        self.grafico = grafico
        self.graficocanvas = graficocanvas
        self.panel_imagen = panel_imagen
        self.imagen_generada = imagen_generada
        self.imagen_tk_generada = imagen_tk_generada

        #self.target = cv2.resize(original, (264, 305))
        self.opcion = opcion

        if self.opcion == 1:
            self.w, self.l, _ = self.target.shape
        
        if self.opcion == 2:
            self.target = cv2.cvtColor(self.target, cv2.COLOR_RGB2GRAY)
            self.w, self.l = self.target.shape
        
        if self.opcion == 3:
            self.target = self.target[:, :, 0]
            self.w, self.l = self.target.shape
        
        if self.opcion == 4:
            self.target = self.target[:, :, 1]
            self.w, self.l = self.target.shape
        
        if self.opcion == 5:
            self.target = self.target[:, :, 2]
            self.w, self.l = self.target.shape



    def run(self):

        poblacion = []
        max_fitness = []
        med_fitness = []

        # comenzar poblacion
        for i in range(self.individuos):
            new_indiv = Individuo(self.l, self.w, self.opcion, True)
            new_indiv.get_fitness(self.target)
            poblacion.append(new_indiv)

        for i in range(self.generaciones):
            new_poblacion = []

            # llenar la nueva poblacion
            while len(new_poblacion) < len(poblacion):
                # selecciona los padres para realizar el cruce
                padre_uno = self.seleccion(poblacion, self.seleccionados)
                padre_dos = self.seleccion(poblacion, self.seleccionados)

                # segun la probabilidad se realiza un tipo de cruce o se realiza una mutacion
                probabilidad = random.uniform(0, 1)


                if probabilidad < self.prob_cruce1:
                    hijo = self.cruce_1(padre_uno, padre_dos)

                    # si el cruce no dio un buen resultado se vuelven a seleccionar otros padres
                    while hijo == None:
                        padre_uno = self.seleccion(poblacion, self.seleccionados)
                        padre_dos = self.seleccion(poblacion, self.seleccionados)

                        hijo = self.cruce_1(padre_uno, padre_dos)

                elif probabilidad <= self.prob_cruce2:
                    hijo = self.cruce_2(padre_uno, padre_dos)

                    # si el cruce no dio un buen resultado se vuelven a seleccionar otros padres
                    while hijo == None:
                        padre_uno = self.seleccion(poblacion, self.seleccionados)
                        padre_dos = self.seleccion(poblacion, self.seleccionados)

                        hijo = self.cruce_2(padre_uno, padre_dos)

                else:
                    hijo = self.mutar(padre_uno)

                    while hijo == None:
                        padre_uno = self.seleccion(poblacion, self.seleccionados)
                        hijo = self.mutar(padre_uno)

                # agrega hijo a la nueva poblacion
                new_poblacion.append(hijo)

            poblacion = new_poblacion

            fitness_val = [obj.fitness for obj in poblacion]

            if len(fitness_val) > 0:
                promedio_fitness = sum(fitness_val) / len(fitness_val)
            else:
                promedio_fitness = 0


            med_fitness.append(promedio_fitness)                
            max_fitness.append(min(poblacion, key=lambda individuo: individuo.fitness).fitness)
            self.grafico.clear()
            self.grafico.plot(max_fitness, label='Mejor fitness')
            self.grafico.plot(med_fitness, label='Promedio fitness')
            self.grafico.legend(['Fitness del individuo más apto', 'Fitness promedio'], loc='upper right')
            self.graficocanvas.draw()
            print(i)

            if i % self.ratio_imagenes == 0:

                fittest = min(poblacion, key=lambda individuo: individuo.fitness)

                print("El mejor fit de la generacion " + str(i) +
                      " tiene un fitness de: " + str(fittest.fitness))

                cv2.imwrite("imagenes/" + str(i) + ".png", fittest.imagen)

                imagen_generada = Image.open("imagenes/" + str(i) + ".png")

                # reescalar la imagen manteniendo la proporción
                max_size = (600, 600)
                imagen_generada.thumbnail(max_size, Image.BILINEAR)

                self.imagen_generada = imagen_generada

                # convertir la imagen a un formato compatible con Tkinter
                self.imagen_tk_generada = ImageTk.PhotoImage(self.imagen_generada)

                # actualizar los paneles con la imagen seleccionada
                self.panel_imagen.config(image=self.imagen_tk_generada)

        
        fitness_val = [obj.fitness for obj in poblacion]

        if len(fitness_val) > 0:
            promedio_fitness = sum(fitness_val) / len(fitness_val)
        else:
            promedio_fitness = 0

        med_fitness.append(promedio_fitness)                
        max_fitness.append(min(poblacion, key=lambda individuo: individuo.fitness).fitness)
        self.grafico.clear()
        self.grafico.plot(max_fitness, label='Mejor fitness')
        self.grafico.plot(med_fitness, label='Promedio fitness')
        self.grafico.legend(['Fitness del individuo más apto', 'Fitness promedio'], loc='upper right')
        self.graficocanvas.draw()
        
        # el mejor individuo de la ultima generacion
        fittest = min(poblacion, key=lambda individuo: individuo.fitness)

        print("El mejor fit de la generacion " + str(self.generaciones) +
                      " tiene un fitness de: " + str(fittest.fitness))

        cv2.imwrite("imagenes/" + str(self.generaciones) + ".png", fittest.imagen)

        imagen_generada = Image.open("imagenes/" + str(self.generaciones) + ".png")

        # reescalar la imagen manteniendo la proporción
        max_size = (600, 600)
        imagen_generada.thumbnail(max_size, Image.BILINEAR)

        self.imagen_generada = imagen_generada

        # convertir la imagen a un formato compatible con Tkinter
        self.imagen_tk_generada = ImageTk.PhotoImage(self.imagen_generada)

        # atualizar los paneles con la imagen seleccionada
        self.panel_imagen.config(image=self.imagen_tk_generada)

        self.generar_gif()
        return fittest

    def seleccion(self, poblacion, cant_seleccionados):

        # seleccinona posible padres de forma aleatoria
        indices = np.random.choice(len(poblacion), cant_seleccionados)
        random_subset = [poblacion[i] for i in indices]

        seleccionado = None

        # busca el individuo con el mejor fit
        for i in random_subset:
            if (seleccionado == None):
                seleccionado = i
            elif i.fitness < seleccionado.fitness:
                seleccionado = i

        return seleccionado

    def cruce_1(self, ind1, ind2):

        hijo = Individuo(self.l, self.w, self.opcion, False)

        blend_alpha = random.uniform(0, 1)

        # en este cruce hace un blend
        imagen_hijo = cv2.addWeighted(ind1.imagen, blend_alpha, ind2.imagen, 1 - blend_alpha, 0)
        hijo.imagen = imagen_hijo
        hijo.get_fitness(self.target)

        # elitismo para que se asegure una alta calidad en las nuevas generaciones
        if hijo.fitness == min(ind1.fitness, ind2.fitness, hijo.fitness):
            return hijo

        return None

    def cruce_2(self, ind1, ind2):

        probabilidad = random.uniform(0, 1)

        # cruce horizontal
        if probabilidad <= 0.5:

            split_point = random.randint(1, self.w)

            mitad_1 = ind1.imagen[:, :self.w // split_point]
            mitad_2 = ind2.imagen[:, self.w // split_point:]

            # combinar las mitades
            imagen_combinada = cv2.hconcat([mitad_1, mitad_2])

        # cruce vertical
        else:
            split_point = random.randint(1, self.l)

            mitad_1 = ind1.imagen[:self.l // split_point, :]
            mitad_2 = ind2.imagen[self.l // split_point:, :]

            # combinar las mitades
            imagen_combinada = cv2.vconcat([mitad_1, mitad_2])

        hijo = Individuo(self.l, self.w, self.opcion, False)
        hijo.imagen = imagen_combinada
        hijo.get_fitness(self.target)

        # elitismo para que se asegure una alta calidad en las nuevas generaciones
        if hijo.fitness == min(ind1.fitness, ind2.fitness, hijo.fitness):
            return hijo

        return None

    def mutar(self, individuo):

        # cantidad de figuras que se agregaran
        cantidad = random.randint(1, 4)

        # delimitar region 
        limite = random.randint(1, (self.l + self.w) // 4)

        img = individuo.imagen

        for _ in range(cantidad):
            num_puntos = random.randint(3, 6)
            region_x = random.randint(0, self.w)
            region_y = random.randint(0, self.l)

            puntos = []
            for _ in range(num_puntos):
                x = random.randint(region_x - limite, region_x + limite)
                y = random.randint(region_y - limite, region_y + limite)
                puntos.append((x,y))
            cv2.fillPoly(img, [np.array(puntos)], individuo.rand_color())

        hijo = Individuo(individuo.l, individuo.w, self.opcion, False)
        hijo.imagen = img
        hijo.get_fitness(self.target)

        return hijo
    
    def generar_gif(self):
        directorio_imagenes = 'imagenes'

        nombres_imagenes = [(nombre, os.path.getctime(os.path.join(directorio_imagenes, nombre))) for nombre in os.listdir(directorio_imagenes)]
        nombres_imagenes.sort(key=lambda x: x[1])
        
        imagenes = []
        
        directorio_salida = 'result.gif'

        # abre cada imagen y la agrega al gif
        for i in range(len(nombres_imagenes)):
            nombre_imagen = nombres_imagenes[i][0]
            ruta_imagen = os.path.join(directorio_imagenes, nombre_imagen)
            img = cv2.imread(ruta_imagen)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            imagenes.append(img)

        # guarda el gif
        imageio.mimsave(directorio_salida, imagenes, duration=1.0)
