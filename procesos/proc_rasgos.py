#Este crea una tabla que relaciona rasgos y cursos

import pandas as pd


cursosraw = pd.read_csv("./cursos/cursos_malla.csv")
cursos = cursosraw[  (cursosraw["semestre"]<=10)\
                   & (cursosraw["nombre"]!="Electiva I")\
                   & (cursosraw["nombre"]!="Electiva II") ]
saberes = pd.read_csv("./saberes.csv")
rasgos = pd.read_csv("./rasgos.csv")
curras = pd.read_csv("./cursos/cursos_rasgos.csv")

rasgos["codSaber"] = rasgos["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
rasgos = rasgos.explode("codSaber") #expadir la lista
curras["codSaber"] = curras["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
curras = curras.explode("codSaber") #expadir la lista


tabla = pd.DataFrame()
tabla["codigo"] = cursos["codigo"].unique()
tabla["nombre"] = tabla["codigo"].apply(lambda x: cursos[cursos["codigo"]==x]["nombre"].tolist()[0]) # el primero de la lista



# Create a new DataFrame from the transposed column
transposed_column = rasgos['codRasgo'].values.reshape(1, -1)
columnas = pd.DataFrame(transposed_column)
columnas.columns = columnas.iloc[0]
columnas = columnas[1:]

tabla = pd.concat([tabla,columnas],axis=1).fillna("")

print(tabla)



# TRC = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD"]
# rTRC = saberes[saberes["codArea"].isin(TRC)]["codSaber"].tolist()

# rasgos["codSaberList"] = rasgos["codSaber"].str.split(';')
# rasgos = rasgos.explode("codSaberList").drop("codSaber",axis=1)
# rasgos.rename(columns={'codSaberList':'codSaber'},inplace=True)

# curras["codSaberList"] = curras["codSaber"].str.split(';')
# curras = curras.explode("codSaberList").drop("codSaber",axis=1)
# curras.rename(columns={'codSaberList':'codSaber'},inplace=True)

# tabla = rasgos.copy()
# # currasTRC = curras[curras["codSaber"].isin(rTRC)]

# for index, row in curras.iterrows():
#     column_name = cursos[cursos["id"]==row["id"]]["codigo"].item()
#     if column_name in tabla.columns:
#         print("repetida")
#     tabla[column_name] = pd.NA 
#     for index2, row2 in tabla.iterrows():
#         if row2["codSaber"] == row["codSaber"]:
#             tabla.loc[index2,column_name] = "X"
    
# print(tabla)

# tablaTRC = tablaTRC[~tablaTRC.index.duplicated(keep='first')]
# print(tablaTRC)
# tablaTRC.to_csv('./cursos/tabla_rasgos_TRC.csv',index=False)
# # print(rasgos)

# INS = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","INS"]
# AER = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","AER"]
# SCF = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","SCF"]

# cursosTRC = cursos[cursos["area"].isin(TRC)]

