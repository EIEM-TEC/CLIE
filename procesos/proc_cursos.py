import pandas as pd

cursos = pd.read_csv("./cursos/cursos_malla.csv").drop(columns="id")

cursos.insert(0,'id',cursos["area"] + cursos["semestre"].astype(str).str.zfill(2) + cursos["fila"].astype(str).str.zfill(2))

cursos.to_csv("./cursos/cursos_id.csv",index=False)