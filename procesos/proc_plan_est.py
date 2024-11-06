# Este archivo es para crear la columna esrequisito a partir de la columna requisitos de cada curso
import pandas as pd

cursos = pd.read_csv("./cursos/cursos_malla.csv")

tipCursoDic = {
    0: "No aplica",
    1: "Teórico",
    2: "Práctico",
    3: "Teórico - Práctico"
}

# Semestre, codigo, tipo, requ, corre, cred, horas totales pres, horas trabajo ind
planestudios = pd.DataFrame()
planestudios['id'] = cursos['id']
planestudios['semestre'] = cursos['semestre']
planestudios['codigo'] = cursos['codigo']
planestudios['nombre'] = cursos['nombre']
planestudios['tiponum'] = cursos['horasTeoria'].apply(lambda x: 0 if x == 0 else 1)\
                     + cursos['horasPractica'].apply(lambda x: 0 if x == 0 else 2)
planestudios['tipo'] = planestudios['tiponum'].apply(lambda x: tipCursoDic.get(x))
planestudios.drop('tiponum', axis=1, inplace=True)
planestudios['requisitos'] = cursos['requisitos']
planestudiosreq =planestudios[planestudios['requisitos'].notna()]
for index, row in planestudiosreq.iterrows():
    id = row['id']
    reqs = row['requisitos'].split(';')
    codigos = ''
    counter = 0
    for req in reqs:
        if counter >= 1:
            codigos += '; '
        codigos += planestudios.loc[planestudios['id'] == req, 'codigo'].item()
        counter += 1
    planestudios.loc[planestudios['id'] == id, 'requisitos'] = codigos
planestudios['correquisitos'] = cursos['correquisitos']
planestudioscoreq =planestudios[planestudios['correquisitos'].notna()]
for index, row in planestudioscoreq.iterrows():
    id = row['id']
    coreqs = row['correquisitos'].split(';')
    codigos = ''
    counter = 0
    for coreq in coreqs:
        if counter >= 1:
            codigos += '; '
        codigos += planestudios.loc[planestudios['id'] == coreq, 'codigo'].item()
        counter += 1
    planestudios.loc[planestudios['id'] == id, 'correquisitos'] = codigos
planestudios['creditos'] = cursos['creditos']
planestudios['horasTot'] = cursos['horasTeoria'] + cursos['horasPractica']
planestudios['horasEC'] = (planestudios['creditos'] * 3) - planestudios['horasTot']
planestudios['horasEC'] = planestudios['horasEC'].apply(lambda x: 0 if x < 0 else x)

print(planestudios.head())

planestudios.to_csv('./cursos/plan_de_estudios.csv',index=False)
