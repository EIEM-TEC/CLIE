import pandas as pd
import funciones as fun
from matplotlib import pyplot as plt

saberes = pd.read_csv("saberes.csv")

areas = pd.read_csv('areas.csv')


# ADD,Analisís de datos,3.0,2.25,2.25,2.25
# AER,Aeronáutica,0.0,0.0,25.0,0.0
# AUT,Automática,11.0,8.25,8.25,8.25
# CIB,Ciencias básicas,27.0,20.25,20.25,20.25
# CYD,Comunicación y dibujo,7.0,5.25,5.25,5.25
# FPH,Formación profesional y habilidades interpersonales,8.0,6.0,6.0,6.0
# IEE,Ingeniería eléctrica y electrónica,20.0,15.0,15.0,15.0
# IMM,Instalaciones,24.0,18.0,18.0,18.0
# INS,Aeronaútica,0.0,25.0,0.0,0.0
# SCF,Sistemas ciberfísicos,0.0,0.0,0.0,25.0
# TOT,Total,100.0,100.0,100.0,100.0

list_trc = ['CIB', 'FPH', 'CYD', 'IEE', 'IMM', 'AUT', 'ADD']

trc = areas[areas['codArea'].isin(list_trc)]

#TRC
catTRC = trc['codArea'].to_list()

valTRC = trc['porcTRC'].to_list()

#INS
list_INS = ['CIB', 'FPH', 'CYD', 'IEE', 'IMM', 'AUT', 'ADD', 'INS']

ins = areas[areas['codArea'].isin(list_INS)]

catINS = ins['codArea'].to_list()

valINS = ins['porcINS'].to_list()

#AER
list_AER = ['CIB', 'FPH', 'CYD', 'IEE', 'IMM', 'AUT', 'ADD', 'AER']

aer = areas[areas['codArea'].isin(list_AER)]

catAER = aer['codArea'].to_list()

valAER = aer['porcAER'].to_list()

#SCF
list_SCF = ['CIB', 'FPH', 'CYD', 'IEE', 'IMM', 'AUT', 'ADD', 'SCF']

scf = areas[areas['codArea'].isin(list_SCF)]

catSCF = scf['codArea'].to_list()

valSCF = scf['porcSCF'].to_list()


fun.radar('TRC',areas,catTRC,valTRC,'Distribución de areas para el tronco común',14,18,30,5,30)

fun.multiradar(list_trc,saberes,areas,'porcTRC',10,12,15,5,20)

#fun.radar('INS',areas,catINS,valINS,'Distribución de areas para el énfasis: Instalaciones electromecánicas',14,18,30,5,30)

fun.radar_saberes('INS',saberes,areas,'porcINS',14,18,12,3,30)

fun.multiradar(list_INS,saberes,areas,'porcINS',10,12,15,5,20)

#fun.radar('AER',areas,catAER,valAER,'Distribución de areas para el énfasis: Aeronaútica',14,18,30,5,30)

fun.radar_saberes('AER',saberes,areas,'porcAER',14,18,12,3,30)

fun.multiradar(list_AER,saberes,areas,'porcAER',10,12,15,5,20)

#fun.radar('SCF',areas,catAER,valAER,'Distribución de areas para el énfasis: Sistemas ciberfísicos',14,18,30,5,30)

fun.radar_saberes('SCF',saberes,areas,'porcSCF',14,18,12,3,30)

fun.multiradar(list_SCF,saberes,areas,'porcSCF',10,12,15,5,20)