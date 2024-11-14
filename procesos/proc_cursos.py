import pandas as pd

cursos = pd.read_csv("cursos.csv")

cursos.insert(0,'id',cursos["area"] + cursos["semestre"].astype(str).str.zfill(2) + cursos["fila"].astype(str).str.zfill(2))

cursos.to_csv('cursosid.csv',index=False)