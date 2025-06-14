import pandas as pd

cursos_profes = pd.read_csv("./cursos/cursos_profes.csv")
datos_profes = pd.read_csv("./profes/datos.csv")
cursos_malla = pd.read_csv("./cursos/cursos_malla.csv")

cursos_profes["profesores"] = cursos_profes["profesores"].str.split(";",expand=False)
cursos_profes = cursos_profes.explode("profesores")
cursos_profes = cursos_profes.merge(datos_profes[["codigo", "nombre"]], left_on="profesores", right_on="codigo", how="left").drop(columns=["codigo","profesores"]).copy()
cursos_profes = cursos_profes.merge(cursos_malla[["semestre","id","codigo","nombre"]],left_on="id", right_on="id", how="left").drop(columns="id").copy()
cursos_profes.rename(columns={"nombre_x":"profesor", "nombre_y":"curso"},inplace=True)
cursos_profes = cursos_profes[["semestre","codigo", "curso", "profesor"]]
cursos_profes.to_csv('./cursos/tabla_profes.csv',index=False)
print(cursos_profes)