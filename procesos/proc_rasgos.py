#Este crea una tabla que relaciona rasgos y cursos

import pandas as pd


cursosraw = pd.read_csv("./cursos/cursos_malla.csv")
cursos = cursosraw[  (cursosraw["semestre"]<=10)\
                   & (cursosraw["nombre"]!="Electiva I")\
                   & (cursosraw["nombre"]!="Electiva II") ]
saberes = pd.read_csv("./saberes.csv")
rasgos = pd.read_csv("./rasgos.csv")
rasgos["codSaber"] = rasgos["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
rasgos = rasgos.explode("codSaber") #expadir la lista
curras = pd.read_csv("./cursos/cursos_rasgos.csv")
curras["codSaber"] = curras["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
curras = curras.explode("codSaber") #expadir la lista


tabla = pd.DataFrame()

tabla["codigo"] = cursos["codigo"].unique()
tabla["nombre"] = tabla["codigo"].apply(lambda x: cursos[cursos["codigo"]==x]["nombre"].tolist()[0]) # el primero de la lista



# Create a new DataFrame from the transposed column
transposed_column = rasgos['codRasgo'].unique().reshape(1, -1)
columnas = pd.DataFrame(transposed_column)
columnas.columns = columnas.iloc[0]
columnas = columnas[1:]

tabla = pd.concat([tabla,columnas],axis=1).fillna("")


for index, row in tabla.iterrows():
    ids = cursos[cursos["codigo"] == row["codigo"]]["id"].tolist()
    listSaberes = []
    listRasgos = []
    for id in ids:
        listSaberes.extend(curras[curras["id"]==id]["codSaber"].unique())
    for saber in listSaberes:
        listRasgos.extend(rasgos[rasgos["codSaber"]==saber]["codRasgo"].unique())
    for rasgo in listRasgos:
        tabla.loc[index,rasgo] = "X"


print(tabla)

tabla.to_csv('./cursos/tabla_rasgos.csv',index=False)


