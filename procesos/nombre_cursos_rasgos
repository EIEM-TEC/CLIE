import pandas as pd

cursosrasgos = pd.read_csv("./cursos/cursos_rasgos.csv")
cursos = pd.read_csv("./cursos/cursos_malla.csv")


cursosrasgos.insert(1,"nombre", cursosrasgos["id"].apply(lambda x: cursos[cursos["id"]==x]["nombre"].item()))

cursosrasgos.to_csv("./cursos/cursos_rasgos.csv",index=False)
