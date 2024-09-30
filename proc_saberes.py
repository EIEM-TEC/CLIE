import pandas as pd

porcTC = 0.75

saberes = pd.read_csv("saberes.csv")

saberes['porcDIG'] = porcTC*saberes['porcBachi']
saberes['porcAER'] = porcTC*saberes['porcBachi']
saberes['porcCIB'] = porcTC*saberes['porcBachi']

saberes.to_csv('saberes.csv')

print(saberes.head(30))