#Este crea una tabla que relaciona rasgos y ejes

import pandas as pd

raseje = pd.read_csv("./rasgos_ejes/rasgos_ejes.csv")
raseje["codEje"] = raseje["codEje"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
raseje = raseje.explode("codEje") #expadir la lista

print(raseje)

tabla = pd.DataFrame()

tabla["rasgo"] = raseje["codRasgo"].unique()

# # Create a new DataFrame from the transposed column
transposed_column = raseje['codEje'].sort_values().unique().reshape(1, -1)
columnas = pd.DataFrame(transposed_column)
columnas.columns = columnas.iloc[0]
columnas = columnas[1:]

tabla = pd.concat([tabla,columnas],axis=1).fillna("")


for index, row in tabla.iterrows():
    ejes = raseje[raseje["codRasgo"] == row["rasgo"]]["codEje"].tolist()
    for eje in ejes:
        tabla.loc[index,eje] = "X"

print(tabla)

tabla.to_csv('./rasgos_ejes/tabla_ejes.csv',index=False)