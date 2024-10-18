import pandas as pd

porcTC = 0.75

saberes = pd.read_csv("saberes.csv")

areas = saberes[['area','porcTRC']].groupby("area",as_index=False).sum()

areas.to_csv('areas.csv',index=False)

areas = pd.read_csv('areas.csv',index_col='area')

areas['porcINS'] = porcTC*areas['porcTRC']
areas.loc['Instalaciones','porcINS'] = (1 - porcTC)*100
areas['porcAER'] = porcTC*areas['porcTRC']
areas.loc['Aeronáutica','porcAER'] = (1 - porcTC)*100
areas['porcSCB'] = porcTC*areas['porcTRC']
areas.loc['Sistemas ciberfísicos','porcSCB'] = (1 - porcTC)*100

areas.loc["Total"] = areas.sum()
areas.insert(0,"cod",["CIB","FPH","CYD","IEE","IMM","AUT","ADD","INS","AER","SCB","TOT"])

print(areas)

areas.to_csv('areas.csv')

