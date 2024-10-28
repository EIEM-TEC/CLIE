import pandas as pd

porcTC = 0.75

saberes = pd.read_csv("saberes.csv")

areas = saberes[['codArea','porcTRC']].groupby("codArea",as_index=False).sum()

areas.to_csv('areas.csv',index=False)

areas = pd.read_csv('areas.csv',index_col='codArea')

areas['porcINS'] = porcTC*areas['porcTRC']
areas.loc['INS','porcINS'] = (1 - porcTC)*100
areas['porcAER'] = porcTC*areas['porcTRC']
areas.loc['AER','porcAER'] = (1 - porcTC)*100
areas['porcSCF'] = porcTC*areas['porcTRC']
areas.loc['SCF','porcSCF'] = (1 - porcTC)*100

areas.loc["TOT"] = areas.sum()

areas.insert(0,"nombre",["Analisís de datos",
                         "Aeronáutica",
                         "Automática",
                         "Ciencias básicas",
                         "Comunicación y dibujo",
                         "Formación profesional y habilidades interpersonales",
                         "Ingeniería eléctrica y electrónica",
                         "Instalaciones",
                         "Aeronaútica",
                         "Sistemas ciberfísicos",
                         "Total"])

print(areas)

areas.to_csv('areas.csv')

