import pandas as pd

cursos = pd.read_csv("./cursos/cursos_malla.csv")

for index, curso in cursos.iterrows():
    idtest = curso["area"] + str(curso["semestre"]).zfill(2) + str(curso["fila"]).zfill(2)
    if curso["id"] != idtest:
        print("Error en el id del curso", curso["id"], idtest)
