import pandas as pd

porcTC = 0.75

saberes = pd.read_csv("saberes.csv")

categorias = saberes[['categoria','porcTRC']].groupby("categoria",as_index=False).sum()

categorias.to_csv('categorias.csv',index=False)

categorias = pd.read_csv('categorias.csv',index_col='categoria')

categorias['porcDIG'] = porcTC*categorias['porcTRC']
categorias.loc['Diseño, instalaciones y gestión','porcDIG'] = (1 - porcTC)*100
categorias['porcAER'] = porcTC*categorias['porcTRC']
categorias.loc['Aeronáutica','porcAER'] = (1 - porcTC)*100
categorias['porcCIB'] = porcTC*categorias['porcTRC']
categorias.loc['Sistemas ciberfísicos','porcCIB'] = (1 - porcTC)*100

categorias.to_csv('categorias.csv')

print(categorias.head(30))