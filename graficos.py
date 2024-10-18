import pandas as pd
import funciones as fun
from matplotlib import pyplot as plt

saberes = pd.read_csv("saberes.csv")

areas = pd.read_csv('areas.csv')

list_trc = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos']

trc = areas[areas['area'].isin(list_trc)]

#TRC
catTRC = trc['area'].to_list()

valTRC = trc['porcTRC'].to_list()

#INS
list_INS = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos', 'Diseño, instalaciones y gestión']

ins = areas[areas['area'].isin(list_INS)]

catINS = ins['area'].to_list()

valINS = ins['porcDIG'].to_list()

#AER
list_AER = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos', 'Aeronáutica']

aer = areas[areas['area'].isin(list_AER)]

catAER = aer['area'].to_list()

valAER = aer['porcAER'].to_list()

#CIB
list_SCB = ['Ciencias básicas', 'Formación profesional y habilidades interpersonales',
            'Comunicación y dibujo', 'Ingeniería eléctrica y electrónica',
            'Ingeniería mecánica y de materiales', 'Automática',
            'Analisís de datos', 'Sistemas ciberfísicos']

scb = areas[areas['area'].isin(list_SCB)]

catSCB = scb['area'].to_list()

valSCB = scb['porcSCB'].to_list()

# fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

# fun.radar_clie(axs,catTRC,valTRC,'Distribución de areas para el tronco común',12,14,30,5)

fun.multiradar(list_trc,saberes,areas,'porcTRC',9,10,15,5,22)

# fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

# fun.radar_clie(axs,catDIG,valDIG,'Distribución de areas para el énfasis: Diseño, instalaciones y gestión',14,18,30,5,30)

fun.multiradar(list_INS,saberes,areas,'porcINS',9,10,15,5,22)

# fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

# fun.radar_clie(axs,catAER,valAER,'Distribución de areas para el énfasis: Aeronáutica',12,14,30,5,30)

fun.multiradar(list_AER,saberes,areas,'porcAER',9,10,15,5,22)

# fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(10, 10))

# fun.radar_clie(axs,catSCB,valSCB,'Distribución de areas para el énfasis: Sistemas ciberfísicos',12,14,30,5,30)

fun.multiradar(list_SCB,saberes,areas,'porcSCB',9,10,15,5,22)

# fig, axs = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(12, 15))