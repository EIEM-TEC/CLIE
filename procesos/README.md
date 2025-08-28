# Procesos

Esta carpeta contiene scripts de Python para procesar datos relacionados con los cursos y la estructura curricular.

## `alarma_nombre.py`

Este script verifica la consistencia de los identificadores de los cursos en el archivo `cursos/cursos_malla.csv`.

**Funcionalidad:**

1.  Lee el archivo `cursos/cursos_malla.csv`.
2.  Itera sobre cada curso.
3.  Construye un ID de prueba concatenando el área, el semestre y la fila del curso.
4.  Compara el ID generado con el ID existente en el archivo.
5.  Si los IDs no coinciden, imprime un mensaje de error indicando el ID del curso y el ID de prueba que no coinciden.

## `foros.py`

Este script agrupa los cursos en tres foros diferentes basados en su área y ID.

**Funcionalidad:**

1.  Lee el archivo `cursos/cursos_malla.csv`.
2.  Filtra los cursos para crear tres DataFrames (`foro1`, `foro2`, `foro3`) basados en condiciones específicas sobre las columnas "area" e "id".
3.  Para cada foro, calcula e imprime:
    *   La suma de los créditos.
    *   El número de cursos.
    *   Los nombres de los cursos en el foro.

## `nombre_cursos_rasgos.py`

Este script agrega los nombres de los cursos al archivo `cursos/cursos_rasgos.csv`.

**Funcionalidad:**

1.  Lee los archivos `cursos/cursos_rasgos.csv` y `cursos/cursos_malla.csv`.
2.  Inserta una nueva columna llamada "nombre" en el DataFrame de `cursos_rasgos`.
3.  Para cada curso en `cursos_rasgos`, busca su nombre en `cursos_malla` usando el "id" del curso y lo asigna a la nueva columna "nombre".
4.  Guarda el DataFrame actualizado de nuevo en `cursos/cursos_rasgos.csv`, ahora con los nombres de los cursos.

## `proc_areas.py`

Este script procesa un archivo `saberes.csv` para calcular y organizar datos por área.

**Funcionalidad:**

1.  Lee el archivo `saberes.csv`.
2.  Agrupa los datos por `codArea` y calcula la suma de varias columnas de porcentajes (`porcTRC`, `porcINS`, `porcAER`, `porcSCF`).
3.  Añade una nueva fila para el área 'ENF' y una fila 'TOT' que contiene la suma total de las columnas.
4.  Inserta una columna "nombre" con los nombres descriptivos de cada área.
5.  Imprime el DataFrame resultante y lo guarda en `areas.csv`.

## `proc_cursos.py`

Este script genera un nuevo archivo CSV con IDs de curso estandarizados.

**Funcionalidad:**

1.  Lee el archivo `cursos/cursos_malla.csv`.
2.  Elimina la columna "id" existente.
3.  Crea una nueva columna "id" concatenando los valores de las columnas "area", "semestre" (con ceros a la izquierda) y "fila" (con ceros a la izquierda).
4.  Guarda el DataFrame resultante en `cursos/cursos_id.csv`.

## `proc_descrip.py`

Este script parece ser una utilidad para dividir un archivo CSV grande en varios más pequeños.

**Funcionalidad:**

1.  Lee un archivo llamado `cursos_descrip copy.csv`.
2.  Contiene código comentado que, si se ejecutara, dividiría el archivo CSV principal en varios archivos más pequeños, cada uno conteniendo el "id" del curso y una de las siguientes columnas: `descripcion`, `objetivoGeneral`, `objetivosEspecificos`, `contenidos`, `metodologia`, `evaluacion`, `bibtex`, `profesores`.

## `proc_req.py`

Este script procesa los requisitos y correquisitos de los cursos para crear un mapeo inverso.

**Funcionalidad:**

1.  Lee el archivo `cursos/cursos_malla.csv`.
2.  Inicializa una nueva columna llamada `esrequisito`.
3.  Itera sobre los cursos que tienen requisitos y correquisitos definidos.
4.  Para cada requisito/correquisito de un curso, añade el ID del curso actual a la columna `esrequisito` del curso que es requisito/correquisito. Esto crea una lista de cursos para los cuales un curso dado es un requisito.
5.  Guarda el DataFrame actualizado de nuevo en `cursos/cursos_malla.csv`.
