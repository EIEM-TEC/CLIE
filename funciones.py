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

def radar_clie(ax,cat,val,title,fontsize,tfontsize,rpmax,mult,textw):
    
    N = len(cat)

    # Cerramos el círculo
    val += val[:1]
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    ang += ang[:1]

    # Dibujamos el gráfico
    ax.plot(ang, val, linewidth=2, linestyle='solid', color='teal')
    ax.fill(ang, val, color='teal', alpha=0.4)

    # Ajustamos los límites radiales
    ax.set_ylim(0, rpmax)

    # Ajustamos las etiquetas del eje radial
    ax.set_rlabel_position(0)
    # list_porc, list_l_porc = gen_list_porc(rpmax)
    list_porc = list(range(mult, rpmax + 1, mult))
    list_l_porc = [f"{numero}%" for numero in list_porc]

    ax.set_yticks(list_porc, list_l_porc, color="grey", size=fontsize)

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
            textwrap.fill(label, width=int(textw)),
            size=fontsize,
            horizontalalignment=alignment,
            verticalalignment="top",
            rotation=angle_text,
            rotation_mode='anchor'
        )

    # Añadimos título
    ax.set_title(textwrap.fill(title, width=tfontsize*4), size=tfontsize, color='blue', y=1.1)

    # Añadimos gridlines personalizados
    ax.grid(color='grey', linestyle='dashed', linewidth=0.5)

    # Mejoramos la estética general
    ax.spines['polar'].set_visible(False)
    ax.set_facecolor('#f7f7f7')

def multiradar(lista,saberes,areas,columnaPorc,fontsize,tfontsize,rpmax,mult,textw):
    fig, axs = plt.subplots(2, 4, subplot_kw=dict(projection='polar'), figsize=(12, 15))

    row = 0
    column = 0
    for area in lista:
        sab = saberes[saberes['area']==area]
        porc = areas[areas['area']==area]
        porc = porc[columnaPorc].item()
        cat = sab['nombre'].to_list()
        val = sab[columnaPorc].to_list()
        #val = [(x / porc)*100 for x in val]
        radar_clie(axs[row,column],cat,val,area,fontsize,tfontsize,rpmax,mult,textw)
        if column < 3:
            column += 1
        else:
            row += 1
            column = 0
    if len(lista) < 8:
        fig.delaxes(axs[row,column])
    #plt.tight_layout(pad=0.1, w_pad=0.5, h_pad=0.2)
    plt.show()