import pandas as pd
import funciones as fun
from matplotlib import pyplot as plt

saberes = pd.read_csv("saberes.csv")

categorias = pd.read_csv('categorias.csv')

list_trc = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos']

trc = categorias[categorias['categoria'].isin(list_trc)]

#TRC
catTRC = trc['categoria'].to_list()

valTRC = trc['porcTRC'].to_list()

list_enf = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos','Énfasis']

enf = categorias[categorias['categoria'].isin(list_enf)]

#TRC
catENF = enf['categoria'].to_list()

valENF = enf['porcENF'].to_list()

#DIG
list_DIG = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos', 'Diseño, instalaciones y gestión']

dig = categorias[categorias['categoria'].isin(list_DIG)]

catDIG = dig['categoria'].to_list()

valDIG = dig['porcDIG'].to_list()

#AER
list_AER = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos', 'Aeronáutica']

aer = categorias[categorias['categoria'].isin(list_AER)]

catAER = aer['categoria'].to_list()

valAER = aer['porcAER'].to_list()

#CIB
list_CIB = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos', 'Sistemas ciberfísicos']

cib = categorias[categorias['categoria'].isin(list_CIB)]

catCIB = cib['categoria'].to_list()

valCIB = cib['porcCIB'].to_list()

# fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

# fun.radar_clie(axs,catTRC,valTRC,'Distribución de areas para el tronco común',12,14,30,5)

fun.multiradar(list_trc,saberes,categorias,'porcTRC',9,10,15,5,22)

# fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

# fun.radar_clie(axs,catDIG,valDIG,'Distribución de areas para el énfasis: Diseño, instalaciones y gestión',14,18,30,5,30)

fun.multiradar(list_DIG,saberes,categorias,'porcDIG',9,10,15,5,22)

# fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

# fun.radar_clie(axs,catAER,valAER,'Distribución de areas para el énfasis: Aeronáutica',12,14,30,5,30)

fun.multiradar(list_AER,saberes,categorias,'porcAER',9,10,15,5,22)

# fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

# fun.radar_clie(axs,catCIB,valCIB,'Distribución de areas para el énfasis: Sistemas ciberfísicos',12,14,30,5,30)

fun.multiradar(list_CIB,saberes,categorias,'porcCIB',9,10,15,5,22)

# fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(12, 15))

# fun.radar_clie(axs,catENF,valENF,'Licenciatura con énfasis',14,18,30,5,30)
# plt.show()