# `rasgos_ejes`

Esta carpeta contiene los archivos que definen y relacionan los rasgos del perfil de egreso, los ejes transversales de la universidad y los saberes específicos del programa de estudios.

## Archivos de Datos (.csv)

Estos archivos contienen los datos fundamentales que describen los rasgos, ejes y saberes.

### `ejes.csv`

Este archivo define los ejes transversales institucionales y los atributos específicos de la maestría. Cada entrada tiene un código (`codEje`) y su descripción (`eje`).

- **Ejes Transversales (EJT):** Son directrices institucionales que promueven una formación integral.
- **Objetivos de Desarrollo Sostenible (ODS):** Se incluyen ODS relevantes para el programa.
- **Atributos de la Maestría (MCA):** Describen las competencias y habilidades que los estudiantes deben adquirir.

### `rasgos.csv`

Define los rasgos del perfil de egreso. Cada rasgo está asociado a uno o más saberes (`codSaber`), tiene un código de rasgo (`codRasgo`) y una descripción detallada (`rasgo`).

### `rasgos_ejes.csv`

Este archivo es una tabla de mapeo que conecta los rasgos del perfil de egreso (`codRasgo`) con los ejes transversales y atributos de la maestría (`codEje`). Una misma característica puede estar asociada a varios ejes, que se separan por punto y coma (`;`).

### `saberes.csv`

Contiene la lista de saberes o áreas de conocimiento del plan de estudios. Para cada saber, se especifica:
- `nombre`: El nombre del saber.
- `codArea`: El código del área a la que pertenece.
- `codSaber`: Un código único para el saber.
- `porcTRC`, `porcINS`, `porcAER`, `porcSCF`: El peso porcentual del saber en el tronco común (`TRC`) y en cada una de las áreas de énfasis (Instalaciones, Aeronáutica y Sistemas Ciberfísicos).

## Scripts de Procesamiento (.py)

Estos scripts procesan los archivos de datos para generar tablas y resúmenes.

### `proc_ejes.py`

Este script de Python lee el archivo `rasgos_ejes.csv`, procesa las relaciones entre rasgos y ejes, y genera una nueva tabla llamada `tabla_ejes.csv`. La tabla resultante tiene los rasgos en las filas y los ejes en las columnas, marcando con una "X" las intersecciones correspondientes para visualizar fácilmente las relaciones.

### `proc_saberes.py`

Este script parece estar diseñado para procesar el archivo `cursos/cursos_malla.csv` y generar el archivo `saberes.csv`. Actualmente, el código del script está comentado, por lo que no realiza ninguna acción. Su propósito original parece ser calcular y asignar los pesos porcentuales de los saberes en las diferentes áreas.

## Archivos Generados

Estos archivos son el resultado de la ejecución de los scripts de procesamiento.

### `tabla_ejes.csv`

Este archivo es generado por el script `proc_ejes.py`. Es una matriz que cruza los rasgos del perfil de egreso con los ejes transversales. Las filas corresponden a los códigos de los rasgos y las columnas a los códigos de los ejes. Una "X" en una celda indica que un rasgo particular está asociado con un eje específico, facilitando el análisis de la cobertura de los ejes por parte de los rasgos del perfil.
