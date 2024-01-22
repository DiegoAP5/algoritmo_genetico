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
        
        self.minimizar_var = tk.BooleanVar(value=True)

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=3)
        root.grid_rowconfigure(0, weight=1)

        self.label_valores_iniciales = tk.Label(control_frame, text="Cantidad de la población inicial:")
        self.label_valores_iniciales.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.entry_initial_values = tk.Entry(control_frame, width=30)
        self.entry_initial_values.grid(row=4, column=0, padx=5, pady=2, sticky="w")

        self.label_poblacion_maxima = tk.Label(control_frame, text="Población máxima:")
        self.label_poblacion_maxima.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.entry_max_population = tk.Entry(control_frame, width=30)
        self.entry_max_population.grid(row=6, column=0, padx=5, pady=2, sticky="w")

        self.label_resolucion = tk.Label(control_frame, text="Resolución:")
        self.label_resolucion.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.entry_resolucion = tk.Entry(control_frame, width=30)
        self.entry_resolucion.grid(row=8, column=0, padx=5, pady=2, sticky="w")

        self.label_limite_inferior = tk.Label(control_frame, text="Intervalo a:")
        self.label_limite_inferior.grid(row=9, column=0, padx=5, pady=5, sticky="w")

        self.entry_limit_a = tk.Entry(control_frame, width=30)
        self.entry_limit_a.grid(row=10, column=0, padx=5, pady=2, sticky="w")

        self.label_limite_superior = tk.Label(control_frame, text="Intervalo b:")
        self.label_limite_superior.grid(row=11, column=0, padx=5, pady=5, sticky="w")

        self.entry_limit_b = tk.Entry(control_frame, width=30)
        self.entry_limit_b.grid(row=12, column=0, padx=5, pady=2, sticky="w")

        self.label_pc = tk.Label(control_frame, text="Probabilidad de cruce:")
        self.label_pc.grid(row=13, column=0, padx=5, pady=5, sticky="w")

        self.entry_pc = tk.Entry(control_frame, width=30)
        self.entry_pc.grid(row=14, column=0, padx=5, pady=2, sticky="w")

        self.label_pmi = tk.Label(control_frame, text="Probabilidad de mutación individuo:")
        self.label_pmi.grid(row=15, column=0, padx=5, pady=5, sticky="w")

        self.entry_pmi = tk.Entry(control_frame, width=30)
        self.entry_pmi.grid(row=16, column=0, padx=5, pady=2, sticky="w")

        self.label_pmg = tk.Label(control_frame, text="Probabilidad de mutación gen:")
        self.label_pmg.grid(row=17, column=0, padx=5, pady=5, sticky="w")

        self.entry_pmg = tk.Entry(control_frame, width=30)
        self.entry_pmg.grid(row=18, column=0, padx=5, pady=2, sticky="w")

        self.label_generaciones = tk.Label(control_frame, text="Número de generaciones:")
        self.label_generaciones.grid(row=19, column=0, padx=5, pady=5, sticky="w")

        self.entry_generations = tk.Entry(control_frame, width=30)
        self.entry_generations.grid(row=20, column=0, padx=5, pady=2, sticky="w")

        self.radio_minimizar = tk.Radiobutton(control_frame, text="Minimizar", variable=self.minimizar_var, value=False)
        self.radio_minimizar.grid(row=21, column=0, padx=5, pady=2, sticky="w")

        self.radio_maximizar = tk.Radiobutton(control_frame, text="Maximizar", variable=self.minimizar_var, value=True)
        self.radio_maximizar.grid(row=22, column=0, padx=5, pady=2, sticky="w")

        self.button_iniciar = tk.Button(control_frame, text="Iniciar", command=self.ejecutar_algoritmo)
        self.button_iniciar.grid(row=23, column=0, padx=5, pady=5, sticky="ew")

        self.best_pop = tk.Label(control_frame, text="")
        self.best_pop.grid(row=24, column=0, padx=5, pady=5, sticky="w")
        
    def ejecutar_algoritmo(self):
        initial_values = int(self.entry_initial_values.get())
        max_population = int(self.entry_max_population.get())
        limit_a = float(self.entry_limit_a.get())
        limit_b = float(self.entry_limit_b.get())
        pc = float(self.entry_pc.get())
        pmi = float(self.entry_pmi.get())
        pmg = float(self.entry_pmg.get())
        num_generaciones = int(self.entry_generations.get())
        resolucion = float(self.entry_resolucion.get())

        best_pop, history = main.iniciar_algoritmo_genetico(
            self.minimizar_var.get(),
            initial_values,
            max_population,
            resolucion,
            limit_a,
            limit_b,
            pc,
            pmi,
            pmg,
            num_generaciones
        )

        self.make_graphics(history, best_pop)

    def make_graphics(self, history, best_pop):
        self.figura, self.ax = plt.subplots()

        generations_final = list(range(1, len(history) + 1))
        best = [item['mejor'] for item in history]
        worst = [item['peor'] for item in history]
        average = [item['promedio'] for item in history]

        linea_mejor, = self.ax.plot(generations_final, best, label='Mejor')
        linea_peor, = self.ax.plot(generations_final, worst, label='Peor')
        linea_promedio, = self.ax.plot(
            generations_final, average, label='Promedio')
        
        self.ax.legend()
        self.ax.set_title(f'Mejor: {best_pop}')
        
        image_folder = 'saved_graphs'

        image_files = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".png")])
        clip = ImageSequenceClip(image_files, fps=1)

        video_file = "output_video.mp4"
        clip.write_videofile(video_file)

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.grafica_frame)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
