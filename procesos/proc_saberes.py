import pandas as pd

porcTC = 0.75

saberes = pd.read_csv("saberes.csv")

# saberes['porcDIG'] = porcTC*saberes['porcTRC']
# saberes['porcAER'] = porcTC*saberes['porcTRC']
# saberes['porcCIB'] = porcTC*saberes['porcTRC']

#saberes.to_csv('saberes.csv',index=False)

print(saberes.head(50))