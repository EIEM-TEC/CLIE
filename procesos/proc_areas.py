import pandas as pd

saberes = pd.read_csv("saberes.csv")

areas = saberes[['codArea','porcTRC','porcINS','porcAER','porcSCF']].groupby("codArea",as_index=True).sum().round(2)

areas['porcENF'] = areas['porcTRC']

areas.loc["ENF"] = [0,0,0,0,25]

areas.loc["TOT"] = areas.sum().round(2)

areas.insert(0,"nombre",["Analisís de datos",
                         "Aeronáutica",
                         "Automática",
                         "Ciencias básicas",
                         "Comunicación y dibujo",
                         "Formación profesional y habilidades interpersonales",
                         "Ingeniería eléctrica y electrónica",
                         "Ingeniería mecánica y de materiales",
                         "Instalaciones electromecánicas",
                         "Sistemas ciberfísicos",
                         "Énfasis",
                         "Total"])


print(areas)

areas.to_csv('areas.csv')

