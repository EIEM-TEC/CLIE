#Este crea una tabla que relaciona rasgos y ejes

import pandas as pd

rasgos = pd.read_csv("./rasgos.csv")
rasgos.drop("codSaber",axis=1,inplace=True) 
raseje = pd.read_csv("./rasgos_ejes.csv")
raseje["codEje"] = raseje["codEje"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
raseje = raseje.explode("codEje") #expadir la lista

print(rasgos)
print(raseje)

tabla = pd.DataFrame()

tabla["rasgo"] = raseje["codRasgo"].unique()
#tabla["nombre"] = tabla["codigo"].apply(lambda x: cursos[cursos["codigo"]==x]["nombre"].tolist()[0]) # el primero de la lista



# # Create a new DataFrame from the transposed column
transposed_column = raseje['codEje'].sort_values().unique().reshape(1, -1)
columnas = pd.DataFrame(transposed_column)
columnas.columns = columnas.iloc[0]
columnas = columnas[1:]

tabla = pd.concat([tabla,columnas],axis=1).fillna("")


# for index, row in tabla.iterrows():
#     ids = cursos[cursos["codigo"] == row["codigo"]]["id"].tolist()
#     listSaberes = []
#     listRasgos = []
#     for id in ids:
#         listSaberes.extend(curras[curras["id"]==id]["codSaber"].unique())
#     for saber in listSaberes:
#         listRasgos.extend(rasgos[rasgos["codSaber"]==saber]["codRasgo"].unique())
#     for rasgo in listRasgos:
#         tabla.loc[index,rasgo] = "X"


print(tabla)

tabla.to_csv('./cursos/tabla_ejes.csv',index=False)


