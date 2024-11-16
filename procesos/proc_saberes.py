import pandas as pd

porcTC = 0.75

saberes = pd.read_csv("saberes.csv")

TRC = ['CIB','FPH','CYD','IEE','IMM','AUT','ADD']
saberes2 = saberes[saberes["codArea"].isin(TRC)]
saberes2['porcINS'] = porcTC*saberes2['porcTRC']
saberes2['porcAER'] = porcTC*saberes2['porcTRC']
saberes2['porcSCF'] = porcTC*saberes2['porcTRC']
saberes[saberes["codArea"].isin(TRC)] = saberes2[saberes2["codArea"].isin(TRC)]

saberes.to_csv('saberes.csv',index=False)

print(saberes.head(50))