#Este crea una tabla que relaciona rasgos y cursos

import pandas as pd


cursos = pd.read_csv("./cursos/cursos_malla.csv")
saberes = pd.read_csv("./saberes.csv")
rasgos = pd.read_csv("./rasgos.csv")
curras = pd.read_csv("./cursos/cursos_rasgos.csv")


TRC = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD"]
rTRC = saberes[saberes["codArea"].isin(TRC)]["codSaber"].tolist()

rasgos["codSaberList"] = rasgos["codSaber"].str.split(';')
rasgos = rasgos.explode("codSaberList").drop("codSaber",axis=1)
rasgos.rename(columns={'codSaberList':'codSaber'},inplace=True)

curras["codSaberList"] = curras["codSaber"].str.split(';')
curras = curras.explode("codSaberList").drop("codSaber",axis=1)
curras.rename(columns={'codSaberList':'codSaber'},inplace=True)

tablaTRC = rasgos[rasgos["codSaber"].isin(rTRC)].copy()
currasTRC = curras[curras["codSaber"].isin(rTRC)]

for index, row in currasTRC.iterrows():
    column_name = cursos[cursos["id"]==row["id"]]["codigo"].item()
    if column_name in tablaTRC.columns:
        print("repetida")
    tablaTRC[column_name] = pd.NA 
    for index2, row2 in tablaTRC.iterrows():
        if row2["codSaber"] == row["codSaber"]:
            tablaTRC.loc[index2,column_name] = "X"
    
tablaTRC = tablaTRC[~tablaTRC.index.duplicated(keep='first')]
print(tablaTRC)
tablaTRC.to_csv('./cursos/tabla_rasgos_TRC.csv',index=False)
# print(rasgos)

INS = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","INS"]
AER = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","AER"]
SCF = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","SCF"]

cursosTRC = cursos[cursos["area"].isin(TRC)]

