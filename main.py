import math
import numpy as np
import random
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import os

def iniciar_algoritmo_genetico(mini, initial, max_population, resolucion, limit_a, limit_b, pc, pmi, pmg, generations):

    history = []

    interval = [limit_a, limit_b]
    rango = limit_b - limit_a
    points = int((rango / resolucion) + 1)
    initial_pop = []
    bits = math.ceil(math.log2(points))
    dX = rango / (2 ** bits - 1)

    def change_to_num(binario):
        return int(binario, 2)

    def gen_x(binario):
        return interval[0] + change_to_num(binario) * dX

    def eval_func(x):
        return ((pow(x, 3) * np.sin(x) / 100) + (pow(x, 2) * np.cos(x)))

    def gen_binary(binario):
        x = gen_x(binario)
        return eval_func(x)

    def gen_initial_populate(valores_iniciales):
        max_bits = max(points.bit_length()
                        for valor in valores_iniciales)

        binarios = [format(valor, f'0{max_bits}b')
                    for valor in valores_iniciales]
        return binarios

    def sort_population(poblacion):
        poblacion_ordenada = sorted(
            poblacion, key=gen_binary, reverse=mini)
        return poblacion_ordenada

    def make_tables(poblacion):

        iterate = 1
        x_vals = []
        fx_vals = []
        for individuo in poblacion:
            i = change_to_num(individuo)
            x = gen_x(individuo)
            fx = gen_binary(individuo)
            x_vals.append(x)
            fx_vals.append(fx)
            iterate += 1
            
        poblacion_ordenada = sort_population(poblacion)

        populate = poblacion_ordenada
        best = populate[0]
        mejor_fx = gen_binary(best)

        peor_individuo = populate[-1]
        peor_fx = gen_binary(peor_individuo)
        x_valsP = np.linspace(limit_a, limit_b, 400)
        y_valsP = eval_func(x_valsP)
        
        mejor_valor_fx = mejor_fx
        peor_valor_fx = peor_fx
        mejor_x = x_vals[fx_vals.index(mejor_valor_fx)]
        peor_x = x_vals[fx_vals.index(peor_valor_fx)]
        
        plt.figure()
        plt.scatter(x_vals, fx_vals, marker='o', label='Población')
        plt.scatter(mejor_x, mejor_fx, color='green', marker='o', label='Mejor')
        plt.scatter(peor_x, peor_fx, color='red', marker='o', label='Peor')
        plt.plot(x_valsP, y_valsP, label='funcion', color='magenta', linewidth=2)
        plt.title(f'Generación {generacion}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True)
        plt.legend()

        image_folder = 'saved_graphs'
        os.makedirs("saved_graphs", exist_ok=True)
        plt.savefig(f'{image_folder}/grafica_generacion_{generacion:03}.png')

        plt.close()

    def eval_population(poblacion):

        poblacion_ordenada = sort_population(poblacion)

        poblacion = poblacion_ordenada

        make_tables(poblacion)

        best = poblacion[0]
        mejor_fx = gen_binary(best)

        peor_individuo = poblacion[-1]
        peor_fx = gen_binary(peor_individuo)

        promedio_fx = sum(gen_binary(ind)
                            for ind in poblacion) / len(poblacion)

        history.append({'mejor': round(mejor_fx, 5), 'peor': round(
            peor_fx, 5), 'promedio': round(promedio_fx, 5)})

        table_historial = PrettyTable(
            ['Generación', 'Mejor', 'Peor', 'Promedio'])
        index = 0
        for generacion in history:
            table_historial.add_row(
                [index, generacion['mejor'], generacion['peor'], generacion['promedio']])
            index += 1
        return poblacion

    def select_rnd(poblacion, umbral):
        seleccionados = []
        index = 1
        for ind in poblacion:
            if random.random() <= umbral:
                seleccionados.append({'bits': ind, 'index': index})
            index += 1
        return seleccionados

    def gen_couples(seleccionados):
        parejas = [(ind, random.choice(seleccionados))
                    for ind in seleccionados]
        return parejas

    def pair_couples(parejas):
        hijos = []
        index = 1
        for pareja in parejas:
            aux = random.randint(0, bits)
            ind1, ind2 = pareja
            if len(ind1['bits']) >= aux and len(ind2['bits']) >= aux:
                nuevo_ind1 = ind1['bits'][:aux] + ind2['bits'][aux:]
                nuevo_ind2 = ind2['bits'][:aux] + ind1['bits'][aux:]
                hijos.extend([{'bits': nuevo_ind1, 'index': index}, {
                            'bits': nuevo_ind2, 'index': index + 1}])
                index += 2
        return hijos

    def select_mut(hijos):
        individuos_seleccionados = []
        for hijo in hijos:
            if random.random() <= pmi:
                individuos_seleccionados.append(hijo)
        return individuos_seleccionados

    def mut_bits(elemento, prob_mutacion_bits):
        bits = list(elemento['bits'])
        for i in range(len(bits)):
            if random.random() <= prob_mutacion_bits:
                otro_indice = random.randint(0, len(bits) - 1)
                bits[i], bits[otro_indice] = bits[otro_indice], bits[i]
        elemento['bits'] = ''.join(bits)
        return elemento

    def mut_children(lista):
        lista_mutada = []
        for ind in lista:
            ind_mutado = mut_bits(ind, pmg)
            lista_mutada.append(ind_mutado)
        return lista_mutada

    def eliminate(poblacion):
        poblacion = list(set(poblacion))
        poblacion_ordenada = sort_population(poblacion)
        poblacion_podada = poblacion_ordenada[:max_population]
        return poblacion_podada
    
    for i in range(initial):
        initial_pop = [random.randint(0,points)]

    poblacion = gen_initial_populate(initial_pop)

    for generacion in range(generations):

        poblacion = eval_population(poblacion)

        seleccionados = select_rnd(poblacion, pc)

        parejas = gen_couples(seleccionados)

        hijos = pair_couples(parejas)

        hijos_seleccionado_para_mutar = select_mut(hijos)

        hijos_mutados_bits = mut_children(
            hijos_seleccionado_para_mutar)

        poblacion.extend([hijo['bits'] for hijo in hijos_mutados_bits])

        make_tables(poblacion)

        poblacion = eliminate(poblacion)

    eval_population(poblacion)

    best = {
        'valor': change_to_num(poblacion[0]), 'f(x)': gen_binary(poblacion[0])}

    return [best, history]
