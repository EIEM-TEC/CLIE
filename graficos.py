import pandas as pd
import funciones as fun
from matplotlib import pyplot as plt

saberes = pd.read_csv("saberes.csv")

categorias = pd.read_csv('categorias.csv')

# cat_list = categorias['categoria'].to_list()
list_trc = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos']

trc = categorias[categorias['categoria'].isin(list_trc)]

#TRC
cat = trc['categoria'].to_list()

val = trc['porcTRC'].to_list()

fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

fun.radar_clie(axs,cat,val,'Distribución de areas para el tronco común',12,14,30,5)

fun.multiradar(list_trc,saberes,categorias,'porcTRC')

#DIG
list_DIG = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos', 'Diseño, instalaciones y gestión']

dig = categorias[categorias['categoria'].isin(list_DIG)]

cat = dig['categoria'].to_list()

val = dig['porcDIG'].to_list()

fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

fun.radar_clie(axs,cat,val,'Distribución de areas para el énfasis: Diseño, instalaciones y gestión',12,14,30,5)

fun.multiradar(list_DIG,saberes,categorias,'porcDIG')

#AER
list_AER = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos', 'Aeronáutica']

aer = categorias[categorias['categoria'].isin(list_AER)]

cat = aer['categoria'].to_list()

val = aer['porcAER'].to_list()

fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

fun.radar_clie(axs,cat,val,'Distribución de areas para el énfasis: Aeronáutica',12,14,30,5)

fun.multiradar(list_AER,saberes,categorias,'porcAER')

#CIB
list_CIB = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos', 'Sistemas ciberfísicos']

cib = categorias[categorias['categoria'].isin(list_CIB)]

cat = cib['categoria'].to_list()

val = cib['porcCIB'].to_list()

fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

fun.radar_clie(axs,cat,val,'Distribución de areas para el énfasis: Sistemas ciberfísicos',12,14,30,5)

fun.multiradar(list_CIB,saberes,categorias,'porcCIB')
