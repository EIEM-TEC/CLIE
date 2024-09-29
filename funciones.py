import textwrap
import numpy as np
import math
from matplotlib import pyplot as plt

def gen_list_porc(N):
    # Verificar que N esté entre 0 y 100
    if N < 0 or N > 100:
        raise ValueError("El número debe estar entre 0 y 100 inclusive.")
    
    # Generar la lista de números múltiplos de 10 hasta N
    lista_numeros = list(range(10, N + 1, 10))
    
    # Generar la lista de cadenas con el signo '%'
    lista_porcentajes = [f"{numero}%" for numero in lista_numeros]
    
    return lista_numeros, lista_porcentajes

def radar_clie(cat,val,title):
    
    rpmax = int(math.ceil(max(val) / 10) * 10)

    N = len(cat)

    # Cerramos el círculo
    val += val[:1]
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    ang += ang[:1]

    # Inicializamos el gráfico polar
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    # Dibujamos el gráfico
    ax.plot(ang, val, linewidth=2, linestyle='solid', color='teal')
    ax.fill(ang, val, color='teal', alpha=0.4)

    # Ajustamos los límites radiales
    ax.set_ylim(0, rpmax)

    # Ajustamos las etiquetas del eje radial
    ax.set_rlabel_position(0)
    list_porc, list_l_porc = gen_list_porc(rpmax) 
    plt.yticks(list_porc, list_l_porc, color="grey", size=10)

    # Ajustamos las etiquetas de las categorías
    # Establecemos los ángulos en grados para las etiquetas
    ang_in_degrees = np.degrees(ang[:-1])
    ax.set_xticks(ang[:-1])
    ax.set_xticklabels([])  # Ocultamos las etiquetas por defecto

    # Añadimos las etiquetas manualmente
    for angle, label in zip(ang[:-1], cat):
        angle_degree = np.degrees(angle)
        if angle_degree >= 90 and angle_degree <= 270:
            alignment = "right"
            angle_text = angle_degree + 180  # Rotamos el texto para que no esté al revés
        else:
            alignment = "left"
            angle_text = angle_degree
        # Posicionamos el texto dentro del gráfico
        ax.text(
            angle,
            ax.get_ylim()[1] * 0.4,  # Ajusta este factor para mover el texto radialmente
            textwrap.fill(label, width=30),
            size=12,
            horizontalalignment=alignment,
            verticalalignment="top",
            rotation=angle_text,
            rotation_mode='anchor'
        )

    # Añadimos título
    plt.title(title, size=14, y=1.08)

    # Añadimos gridlines personalizados
    ax.grid(color='grey', linestyle='dashed', linewidth=0.5)

    # Mejoramos la estética general
    ax.spines['polar'].set_visible(False)
    ax.set_facecolor('#f7f7f7')
    fig.patch.set_facecolor('#f7f7f7')

    plt.show()