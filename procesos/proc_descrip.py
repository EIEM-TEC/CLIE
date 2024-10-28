import pandas as pd

datos = pd.read_csv("cursos_descrip copy.csv")
print(datos.head(1))

# descripcion = datos[['id','descripcion']]
# descripcion.to_csv('cursos_descri.csv',index=False)
# objetivoGeneral = datos[['id','objetivoGeneral']]
# objetivoGeneral.to_csv('cursos_objgen.csv',index=False)
# objetivosEspecificos = datos[['id','objetivosEspecificos']]
# objetivosEspecificos.to_csv('cursos_objesp.csv',index=False)
# contenidos = datos[['id','contenidos']]
# contenidos.to_csv('cursos_conten.csv',index=False)
# metodologia = datos[['id','metodologia']]
# metodologia.to_csv('cursos_metodo.csv',index=False)
# evaluacion = datos[['id','evaluacion']]
# evaluacion.to_csv('cursos_evalua.csv',index=False)
# bibtex = datos[['id','bibtex']]
# bibtex.to_csv('cursos_bibtex.csv',index=False)
# profesores = datos[['id','profesores']]
# profesores.to_csv('cursos_profes.csv',index=False)
