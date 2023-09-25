import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageSequence
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Genetico import Genetico
import threading
import time

class Interfaz:
    def __init__(self, root):
        self.running = False
        self.cantidad_individuos = 0
        self.num_generaciones = 0
        self.cantidad_seleccionados = 0
        self.porcentaje_mutacion = 0.0
        self.mostrar_cada = 0
        self.genetico = None
        
        self.frames = []
        self.file_path = ''
        self.gif_path = "result.gif"

        self.root = root
        self.root.title("Algoritmo Genético")


        self.imagen_seleccionada = None
        self.imagen_generada = None
        self.imagen_tk_generada = None
        self.imagen_tk = None

        # panel izquierdo con imagen fija
        self.panel_izquierdo = tk.Frame(root, width=200, height=400)
        self.panel_izquierdo.pack(side=tk.LEFT, padx=10, pady=10)
        self.imagen_label = tk.Label(self.panel_izquierdo, image=None)
        self.imagen_label.pack()

        # panel derecho con imagen fija
        self.panel_derecho = tk.Frame(root, width=200, height=400)
        self.panel_derecho.pack(side=tk.RIGHT, padx=10, pady=10)
        self.imagen_label2 = tk.Label(self.panel_derecho, image=None)
        self.imagen_label2.pack()

        # panel central con gráfico Matplotlib
        self.panel_central = tk.Frame(root, width=800, height=400)
        self.panel_central.pack(padx=10, pady=10)
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.panel_central)
        self.canvas.get_tk_widget().pack()

        # botón para seleccionar una imagen
        self.boton_imagen = tk.Button(root, text="Seleccionar Imagen", command=self.cargar_imagen)
        self.boton_imagen.pack()

        # entradas de parámetros
        self.parametros_frame = tk.Frame(root)
        self.parametros_frame.pack(padx=10, pady=10)
        tk.Label(self.parametros_frame, text="Cantidad de Individuos:").grid(row=0, column=0)
        tk.Label(self.parametros_frame, text="Número de Generaciones:").grid(row=1, column=0)
        tk.Label(self.parametros_frame, text="Cantidad de Seleccionados:").grid(row=2, column=0)
        tk.Label(self.parametros_frame, text="% de Mutación:").grid(row=3, column=0)
        tk.Label(self.parametros_frame, text="Mostrar cada n generaciones:").grid(row=4, column=0)
        self.cantidad_individuos_entry = tk.Entry(self.parametros_frame)
        self.cantidad_individuos_entry.grid(row=0, column=1)
        self.num_generaciones_entry = tk.Entry(self.parametros_frame)
        self.num_generaciones_entry.grid(row=1, column=1)
        self.cantidad_seleccionados_entry = tk.Entry(self.parametros_frame)
        self.cantidad_seleccionados_entry.grid(row=2, column=1)
        self.porcentaje_mutacion_entry = tk.Entry(self.parametros_frame)
        self.porcentaje_mutacion_entry.grid(row=3, column=1)
        self.mostrar_cada_entry = tk.Entry(self.parametros_frame)
        self.mostrar_cada_entry.grid(row=4, column=1)

        # botón para iniciar la ejecución
        self.botones_frame = tk.Frame(root)
        self.botones_frame.pack(padx=10, pady=10)
        self.boton_iniciar1 = tk.Button(self.botones_frame, text="Ejecución a Color", command=lambda: self.iniciar_ejecucion(1))
        self.boton_iniciar1.grid(row=0, column=0)
        self.boton_iniciar2 = tk.Button(self.botones_frame, text="Ejecución a Grises", command=lambda: self.iniciar_ejecucion(2))
        self.boton_iniciar2.grid(row=0, column=1)
        self.boton_iniciar3 = tk.Button(self.botones_frame, text="Ejecución a Esquema Rojo", command=lambda: self.iniciar_ejecucion(3))
        self.boton_iniciar3.grid(row=0, column=2)
        self.boton_iniciar4 = tk.Button(self.botones_frame, text="Ejecución a Esquema Verde", command=lambda: self.iniciar_ejecucion(4))
        self.boton_iniciar4.grid(row=0, column=3)
        self.boton_iniciar5 = tk.Button(self.botones_frame, text="Ejecución a Esquema Azul", command=lambda: self.iniciar_ejecucion(5))
        self.boton_iniciar5.grid(row=0, column=4)

        self.boton_gif = tk.Button(root, text="Reproducir GIF de Resultado", command=lambda: self.reproducir_gif())
        self.boton_gif.pack()
        self.boton_gif.config(state="disabled")

        self.genetico = None

    def cargar_imagen(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if self.file_path:

            imagen_original = Image.open(self.file_path)

            # reescalar la imagen manteniendo la proporción
            max_size = (500, 500)
            imagen_original.thumbnail(max_size, Image.BILINEAR)

            self.imagen_seleccionada = imagen_original

            # convertir la imagen a un formato compatible con Tkinter
            self.imagen_tk = ImageTk.PhotoImage(self.imagen_seleccionada)

            # actualizar los paneles con la imagen seleccionada
            self.imagen_label.config(image=self.imagen_tk)
            self.imagen_label2.config(image=self.imagen_tk)

    def iniciar_ejecucion(self, opcion):

        self.cantidad_individuos = int(self.cantidad_individuos_entry.get())
        self.num_generaciones = int(self.num_generaciones_entry.get())
        self.cantidad_seleccionados = int(self.cantidad_seleccionados_entry.get())
        self.porcentaje_mutacion = float(self.porcentaje_mutacion_entry.get())
        self.mostrar_cada = int(self.mostrar_cada_entry.get())

        if self.file_path != '':
            self.boton_iniciar1.config(state="disabled")
            self.boton_iniciar2.config(state="disabled")
            self.boton_iniciar3.config(state="disabled")
            self.boton_iniciar4.config(state="disabled")
            self.boton_iniciar5.config(state="disabled")
            self.boton_imagen.config(state="disabled")
            self.boton_gif.config(state="disabled")

            self.genetico = Genetico(self.file_path, self.cantidad_individuos, self.num_generaciones, self.cantidad_seleccionados, self.porcentaje_mutacion, self.mostrar_cada, self.ax, self.canvas, self.imagen_label, self.imagen_generada, self.imagen_tk_generada, opcion)
            thread = threading.Thread(target=self.ejecucion)
            thread.start()

            resultados = []
            
            self.ax.clear()
            self.ax.plot(resultados)
            self.canvas.draw()
    
    def ejecucion(self):
        thread = threading.Thread(target=self.genetico.run)
        thread.start()
        thread.join()
        self.boton_iniciar1.config(state="normal")
        self.boton_iniciar2.config(state="normal")
        self.boton_iniciar3.config(state="normal")
        self.boton_iniciar4.config(state="normal")
        self.boton_iniciar5.config(state="normal")
        self.boton_imagen.config(state="normal")
        self.boton_gif.config(state="normal")

    def reproducir_gif(self):
        self.boton_iniciar1.config(state="disabled")
        self.boton_iniciar2.config(state="disabled")
        self.boton_iniciar3.config(state="disabled")
        self.boton_iniciar4.config(state="disabled")
        self.boton_iniciar5.config(state="disabled")
        self.boton_imagen.config(state="disabled")
        self.boton_gif.config(state="disabled")

        gif = Image.open(self.gif_path)
        self.frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]
        
        for i, frame in enumerate(self.frames):
            self.imagen_label.config(image=frame)
            self.panel_izquierdo.update_idletasks() 
            self.panel_izquierdo.after(500)
        
        self.boton_iniciar1.config(state="normal")
        self.boton_iniciar2.config(state="normal")
        self.boton_iniciar3.config(state="normal")
        self.boton_iniciar4.config(state="normal")
        self.boton_iniciar5.config(state="normal")
        self.boton_imagen.config(state="normal")
        self.boton_gif.config(state="normal")

        return


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
