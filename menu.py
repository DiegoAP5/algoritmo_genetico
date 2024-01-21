import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from moviepy.editor import ImageSequenceClip
import matplotlib.pyplot as plt
import main
import os

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo Genético")
        self.root.geometry("1200x800")

        control_frame = ttk.Frame(root)
        control_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.grafica_frame = ttk.Frame(root)
        self.grafica_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=3)
        root.grid_rowconfigure(0, weight=1)

        # Controles
        self.label_minizar = tk.Label(control_frame, text="Seleccionar qué evaluar:")
        self.label_minizar.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.minimizar_var = tk.BooleanVar(value=True)

        self.radio_minimizar = tk.Radiobutton(control_frame, text="Minimizar", variable=self.minimizar_var, value=True)
        self.radio_minimizar.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        self.radio_maximizar = tk.Radiobutton(control_frame, text="Maximizar", variable=self.minimizar_var, value=False)
        self.radio_maximizar.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        self.label_valores_iniciales = tk.Label(control_frame, text="Valores Iniciales (separar por comas):")
        self.label_valores_iniciales.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.entry_valores_iniciales = tk.Entry(control_frame, width=30)
        self.entry_valores_iniciales.grid(row=4, column=0, padx=5, pady=2, sticky="w")

        self.label_poblacion_maxima = tk.Label(control_frame, text="Población Máxima:")
        self.label_poblacion_maxima.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.entry_poblacion_maxima = tk.Entry(control_frame, width=30)
        self.entry_poblacion_maxima.grid(row=6, column=0, padx=5, pady=2, sticky="w")

        self.label_resolucion = tk.Label(control_frame, text="Resolución:")
        self.label_resolucion.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.entry_resolucion = tk.Entry(control_frame, width=30)
        self.entry_resolucion.grid(row=8, column=0, padx=5, pady=2, sticky="w")

        self.label_limite_inferior = tk.Label(control_frame, text="Límite Inferior:")
        self.label_limite_inferior.grid(row=9, column=0, padx=5, pady=5, sticky="w")

        self.entry_limite_inferior = tk.Entry(control_frame, width=30)
        self.entry_limite_inferior.grid(row=10, column=0, padx=5, pady=2, sticky="w")

        self.label_limite_superior = tk.Label(control_frame, text="Límite Superior:")
        self.label_limite_superior.grid(row=11, column=0, padx=5, pady=5, sticky="w")

        self.entry_limite_superior = tk.Entry(control_frame, width=30)
        self.entry_limite_superior.grid(row=12, column=0, padx=5, pady=2, sticky="w")

        self.label_pc = tk.Label(control_frame, text="Probabilidad de Cruce (pc):")
        self.label_pc.grid(row=13, column=0, padx=5, pady=5, sticky="w")

        self.entry_pc = tk.Entry(control_frame, width=30)
        self.entry_pc.grid(row=14, column=0, padx=5, pady=2, sticky="w")

        self.label_pmi = tk.Label(control_frame, text="Probabilidad de Mutación Individuo (pmi):")
        self.label_pmi.grid(row=15, column=0, padx=5, pady=5, sticky="w")

        self.entry_pmi = tk.Entry(control_frame, width=30)
        self.entry_pmi.grid(row=16, column=0, padx=5, pady=2, sticky="w")

        self.label_pmg = tk.Label(control_frame, text="Probabilidad de Mutación Gen (pmg):")
        self.label_pmg.grid(row=17, column=0, padx=5, pady=5, sticky="w")

        self.entry_pmg = tk.Entry(control_frame, width=30)
        self.entry_pmg.grid(row=18, column=0, padx=5, pady=2, sticky="w")

        self.label_generaciones = tk.Label(control_frame, text="Número de Generaciones:")
        self.label_generaciones.grid(row=19, column=0, padx=5, pady=5, sticky="w")

        self.entry_generaciones = tk.Entry(control_frame, width=30)
        self.entry_generaciones.grid(row=20, column=0, padx=5, pady=2, sticky="w")

        self.button_iniciar = tk.Button(control_frame, text="Iniciar Algoritmo", command=self.ejecutar_algoritmo)
        self.button_iniciar.grid(row=21, column=0, padx=5, pady=5, sticky="ew")

        self.mejor_individuo = tk.Label(control_frame, text="")
        self.mejor_individuo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
    def ejecutar_algoritmo(self):
        texto_ingresado = str(self.minimizar_var.get())
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
            texto_ingresado.lower == 'false',
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

        linea_mejor, = self.ax.plot(generaciones, mejor, label='Mejor')
        linea_peor, = self.ax.plot(generaciones, peor, label='Peor')
        linea_promedio, = self.ax.plot(
            generaciones, promedio, label='Promedio')

        self.ax.legend()
        
        
        image_folder = 'saved_graphs'

        image_files = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".png")])
        clip = ImageSequenceClip(image_files, fps=5)

        video_file = "output_video.mp4"
        clip.write_videofile(video_file)

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.grafica_frame)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
