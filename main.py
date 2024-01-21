import math
import random
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import os

def iniciar_algoritmo_genetico(minimizar, individuos_iniciales, poblacion_max, resolucion, limite_inferior, limite_superior, pc, pmi, pmg, num_generaciones):

    historial_generaciones = []

    intervalos = [limite_inferior, limite_superior]
    rango = limite_superior - limite_inferior
    puntos = int((rango / resolucion) + 1)
    print(puntos)
    bits = math.ceil(math.log2(puntos))
    dX = rango / (2 ** bits - 1)

    def convertir_bit_a_numero(binario):
        return int(binario, 2)

    def generar_x(binario):
        return intervalos[0] + convertir_bit_a_numero(binario) * dX

    def evaluar_funcion(x):
        return ((pow(x, 3) * math.sin(x) / 100) + (pow(x, 2) * math.cos(x)))

    def generar_fx_con_binario(binario):
        x = generar_x(binario)
        return evaluar_funcion(x)

    def generar_poblacion_inicial(valores_iniciales):
        max_bits = max(puntos.bit_length()
                        for valor in valores_iniciales)

        binarios = [format(valor, f'0{max_bits}b')
                    for valor in valores_iniciales]
        return binarios

    def ordenar_poblacion(poblacion):
        poblacion_ordenada = sorted(
            poblacion, key=generar_fx_con_binario, reverse=minimizar)
        return poblacion_ordenada

    def imprimir_poblacion(poblacion):

        table = PrettyTable(['Individuo', 'Bits', 'i', 'x', 'f(x)'])
        iterate = 1
        x_vals = []
        fx_vals = []
        for individuo in poblacion:
            i = convertir_bit_a_numero(individuo)
            x = generar_x(individuo)
            fx = generar_fx_con_binario(individuo)
            x_vals.append(x)
            fx_vals.append(fx)
            table.add_row([iterate, individuo,
                            i, round(x, 5), round(fx, 5)])
            iterate += 1

        print(table)
        plt.figure()
        plt.scatter(x_vals, fx_vals, marker='o')
        plt.title(f'Generación {generacion}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True)

        image_folder = 'saved_graphs'
        os.makedirs("saved_graphs", exist_ok=True)
        plt.savefig(f'{image_folder}/grafica_generacion_{generacion:03}.png')

        plt.close()

    def evaluar_poblacion(poblacion):

        poblacion_ordenada = ordenar_poblacion(poblacion)

        poblacion = poblacion_ordenada

        tabla_valores = PrettyTable(
            ['Intervalos', 'Rango', 'bits', 'resolucion', 'puntos', 'dX'])
        tabla_valores.add_row(
            [intervalos, rango, bits, resolucion, puntos, dX])
        print(tabla_valores)

        imprimir_poblacion(poblacion)

        mejor_individuo = poblacion[0]
        mejor_fx = generar_fx_con_binario(mejor_individuo)

        peor_individuo = poblacion[-1]
        peor_fx = generar_fx_con_binario(peor_individuo)

        promedio_fx = sum(generar_fx_con_binario(ind)
                            for ind in poblacion) / len(poblacion)

        historial_generaciones.append({'mejor': round(mejor_fx, 5), 'peor': round(
            peor_fx, 5), 'promedio': round(promedio_fx, 5)})

        table_historial = PrettyTable(
            ['Generación', 'Mejor', 'Peor', 'Promedio'])
        index = 0
        for generacion in historial_generaciones:
            table_historial.add_row(
                [index, generacion['mejor'], generacion['peor'], generacion['promedio']])
            index += 1
        print(table_historial)
        return poblacion

    def seleccionar_por_umbral(poblacion, umbral):
        seleccionados = []
        index = 1
        for ind in poblacion:
            if random.random() <= umbral:
                seleccionados.append({'bits': ind, 'index': index})
            index += 1
        return seleccionados

    def generar_parejas(seleccionados):
        parejas = [(ind, random.choice(seleccionados))
                    for ind in seleccionados]
        return parejas

    def cruzar_parejas(parejas):
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

    def seleccionar_para_mutacion(hijos):
        individuos_seleccionados = []
        for hijo in hijos:
            if random.random() <= pmi:
                individuos_seleccionados.append(hijo)
        return individuos_seleccionados

    def mutar_bits(elemento, prob_mutacion_bits):
        bits = list(elemento['bits'])
        for i in range(len(bits)):
            if random.random() <= prob_mutacion_bits:
                otro_indice = random.randint(0, len(bits) - 1)
                bits[i], bits[otro_indice] = bits[otro_indice], bits[i]
        elemento['bits'] = ''.join(bits)
        return elemento

    def mutar_hijos(lista):
        lista_mutada = []
        for ind in lista:
            ind_mutado = mutar_bits(ind, pmg)
            lista_mutada.append(ind_mutado)
        return lista_mutada

    def eliminar_duplicados_y_podar(poblacion):
        poblacion = list(set(poblacion))
        poblacion_ordenada = ordenar_poblacion(poblacion)
        poblacion_podada = poblacion_ordenada[:poblacion_max]
        return poblacion_podada

    poblacion = generar_poblacion_inicial(individuos_iniciales)

    for generacion in range(num_generaciones):
        print(f"\nGeneración {generacion}:")

        poblacion = evaluar_poblacion(poblacion)

        seleccionados = seleccionar_por_umbral(poblacion, pc)

        print("\nIndividuos seleccionados por umbral para cruza:")
        table_seleccionados = PrettyTable(['Individuo', 'Bits'])
        for ind in seleccionados:
            table_seleccionados.add_row(
                [ind['index'], ind['bits']])
        print(table_seleccionados)

        parejas = generar_parejas(seleccionados)

        print("\nParejas generadas para cruza:")
        table_parejas = PrettyTable(
            ['Individuo 1', 'Bits 1', 'Individuo 2', 'Bits 2'])
        for pareja in parejas:
            table_parejas.add_row(
                [pareja[0]['index'], pareja[0]['bits'], pareja[1]['index'], pareja[1]['bits']])
        print(table_parejas)

        hijos = cruzar_parejas(parejas)

        print("\nHijos generados después del cruce:")
        table_hijos = PrettyTable(['Individuo', 'Bits'])
        for i, hijo in enumerate(hijos, 1):
            table_hijos.add_row([i, hijo['bits']])
        print(table_hijos)

        hijos_seleccionado_para_mutar = seleccionar_para_mutacion(hijos)

        print("\nHijos después de selección de quienes mutan:")
        table_hijos_seleccionados_para_mutar = PrettyTable(
            ['Individuo', 'Bits'])
        for i, hijo_seleccionado_para_mutar in enumerate(hijos_seleccionado_para_mutar, 1):
            table_hijos_seleccionados_para_mutar.add_row(
                [hijos.index(hijo_seleccionado_para_mutar) + 1, hijo_seleccionado_para_mutar['bits']])
        print(table_hijos_seleccionados_para_mutar)

        hijos_mutados_bits = mutar_hijos(
            hijos_seleccionado_para_mutar)

        print("\nHijos después de la mutación a nivel de bits (intercambio de genes):")
        table_hijos_mutados_bits = PrettyTable(['Individuo', 'Bits'])
        for i, hijo_mutado_bits in enumerate(hijos_mutados_bits, 1):
            table_hijos_mutados_bits.add_row(
                [hijos.index(hijo_mutado_bits) + 1, hijo_mutado_bits['bits']])
        print(table_hijos_mutados_bits)

        poblacion.extend([hijo['bits'] for hijo in hijos_mutados_bits])

        print("\nPoblación resultante después de agregar los hijos mutados:")
        imprimir_poblacion(poblacion)

        poblacion = eliminar_duplicados_y_podar(poblacion)

    print("\nPoblación final después de la generación "+str(num_generaciones)+" :")
    evaluar_poblacion(poblacion)

    print(historial_generaciones)
    print("minimizar: ",minimizar)
    mejor_individuo = {
        "Binario": poblacion[0], 'i': convertir_bit_a_numero(poblacion[0]), 'f(x):': generar_fx_con_binario(poblacion[0])}

    return [mejor_individuo, historial_generaciones]
