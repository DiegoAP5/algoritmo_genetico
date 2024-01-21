import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from moviepy.editor import ImageSequenceClip
import matplotlib.pyplot as plt
import numpy as np
import main
import os

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo Genético")
        self.root.geometry("800x1000")

        self.label_titulo = tk.Label(
            root, text="Presiona el botón para empezar")
        self.label_titulo.pack(pady=1)
        
        self.label_minizar = tk.Label(
            root, text="Minimizar (por defecto):")
        self.label_minizar.pack()

        self.entry_texto = tk.Entry(root, width=30)
        self.entry_texto.pack(pady=1)

        self.label_valores_iniciales = tk.Label(
            root, text="Valores Iniciales (separar por comas):")
        self.label_valores_iniciales.pack()

        self.entry_valores_iniciales = tk.Entry(root, width=30)
        self.entry_valores_iniciales.pack(pady=1)

        self.label_poblacion_maxima = tk.Label(root, text="Población Máxima:")
        self.label_poblacion_maxima.pack()

        self.entry_poblacion_maxima = tk.Entry(root, width=30)
        self.entry_poblacion_maxima.pack(pady=1)
        
        self.label_resolucion = tk.Label(root, text="Resolución:")
        self.label_resolucion.pack()

        self.entry_resolucion = tk.Entry(root, width=30)
        self.entry_resolucion.pack(pady=1)

        self.label_limite_inferior = tk.Label(root, text="Límite Inferior:")
        self.label_limite_inferior.pack()

        self.entry_limite_inferior = tk.Entry(root, width=30)
        self.entry_limite_inferior.pack(pady=1)

        self.label_limite_superior = tk.Label(root, text="Límite Superior:")
        self.label_limite_superior.pack()

        self.entry_limite_superior = tk.Entry(root, width=30)
        self.entry_limite_superior.pack(pady=1)

        self.label_pc = tk.Label(root, text="Probabilidad de Cruce:")
        self.label_pc.pack()

        self.entry_pc = tk.Entry(root, width=30)
        self.entry_pc.pack(pady=1)

        self.label_pmi = tk.Label(
            root, text="Probabilidad de Mutación:")
        self.label_pmi.pack()

        self.entry_pmi = tk.Entry(root, width=30)
        self.entry_pmi.pack(pady=1)

        self.label_pmg = tk.Label(
            root, text="Probabilidad de Mutación en gen:")
        self.label_pmg.pack()

        self.entry_pmg = tk.Entry(root, width=30)
        self.entry_pmg.pack(pady=1)

        self.label_generaciones = tk.Label(
            root, text="Generaciones:")
        self.label_generaciones.pack()

        self.entry_generaciones = tk.Entry(root, width=30)
        self.entry_generaciones.pack(pady=1)

        self.button_obtener_mensaje = tk.Button(
            root, text="Comenzar", command=self.ejecutar_algoritmo)
        self.button_obtener_mensaje.pack()

        self.mejor_individuo = tk.Label(root, text="")
        self.mejor_individuo.pack(pady=1)

        self.frame_grafica = ttk.Frame(root)
        self.frame_grafica.pack(pady=1)

    def ejecutar_algoritmo(self):
        texto_ingresado = self.entry_texto.get()
        valores_iniciales_str = self.entry_valores_iniciales.get().split(',')

        try:
            valores_iniciales = [int(valor) for valor in valores_iniciales_str]
        except ValueError:
            self.label_mensaje.config(
                text="Error: Ingresa valores iniciales válidos (números enteros).")
            return

        poblacion_maxima = int(self.entry_poblacion_maxima.get())
        limite_inferior = float(self.entry_limite_inferior.get())
        limite_superior = float(self.entry_limite_superior.get())
        pc = float(self.entry_pc.get())
        pmi = float(self.entry_pmi.get())
        pmg = float(self.entry_pmg.get())
        num_generaciones = int(self.entry_generaciones.get())
        resolucion = float(self.entry_resolucion.get())

        mejor_individuo, historial_generaciones = main.iniciar_algoritmo_genetico(
            texto_ingresado.lower() == 'false',
            valores_iniciales,
            poblacion_maxima,
            resolucion,
            limite_inferior,
            limite_superior,
            pc,
            pmi,
            pmg,
            num_generaciones
        )

        self.mejor_individuo.config(
            text="Mejor individuo"+str(mejor_individuo))

        self.inicializar_grafica(historial_generaciones)

    def inicializar_grafica(self, historial_generaciones):
        self.figura, self.ax = plt.subplots()

        generaciones = list(range(1, len(historial_generaciones) + 1))
        mejor = [item['mejor'] for item in historial_generaciones]
        peor = [item['peor'] for item in historial_generaciones]
        promedio = [item['promedio'] for item in historial_generaciones]

        self.ax.legend()
        
        
        image_folder = 'saved_graphs'

        image_files = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".png")])
        clip = ImageSequenceClip(image_files, fps=5)

        video_file = "output_video.mp4"
        clip.write_videofile(video_file)

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_grafica)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
