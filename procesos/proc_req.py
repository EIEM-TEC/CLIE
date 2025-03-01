# Este archivo es para crear la columna esrequisito a partir de la columna requisitos de cada curso
import pandas as pd

cursos = pd.read_csv("./cursos/cursos_malla.csv")

cursos['esrequisito'] = None # borrar los datos de la columna
cursosreq = cursos[cursos['requisitos'].notna()]

for index, row in cursosreq.iterrows():
    id = row['id']
    reqs = row['requisitos'].split(';')
    for req in reqs:
        print(req)
        curr_val = cursos.loc[cursos['id'] == req, 'esrequisito'].item()
        if curr_val == None:
            cursos.loc[cursos['id'] == req, 'esrequisito'] = id
        else:
            cursos.loc[cursos['id'] == req, 'esrequisito'] = cursos[cursos['id'] == req]['esrequisito'].item() + ';' + id

cursoscorreq = cursos[cursos['correquisitos'].notna()]
for index, row in cursoscorreq.iterrows():
    id = row['id']
    correqs = row['correquisitos'].split(';')
    for correq in correqs:
        print(correq)
        curr_val = cursos.loc[cursos['id'] == correq, 'esrequisito'].item()
        if curr_val == None:
            cursos.loc[cursos['id'] == correq, 'esrequisito'] = id
        else:
            cursos.loc[cursos['id'] == correq, 'esrequisito'] = cursos[cursos['id'] == correq]['esrequisito'].item() + ';' + id


cursos.to_csv('./cursos/cursos_malla.csv',index=False)
