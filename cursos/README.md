# `cursos`

Esta carpeta contiene los datos y scripts relacionados con la definición de los cursos de la carrera de Ingeniería Electromecánica.

Algunas tablas en esta carpeta son editadas automáticamente por los scripts de la carpeta `procesos` o los scripts de esta misma carpeta.

## Scripts de Procesamiento

Estos scripts se utilizan para procesar los datos de los cursos y generar tablas consolidadas.

### `proc_cursos_profes.py`

Este script genera la tabla `tabla_profes.csv`. Su función es la siguiente:
1.  Lee los archivos `cursos_profes.csv` (que asigna profesores a cursos por ID), `cursos_malla.csv` (con la información general de los cursos) y un archivo CSV con los datos de los profesores desde un repositorio remoto.
2.  Expande la lista de profesores por curso, ya que un curso puede tener varios profesores asignados.
3.  Fusiona los datos para obtener los nombres de los profesores y de los cursos.
4.  Genera el archivo `tabla_profes.csv` con las columnas: `semestre`, `codigo`, `curso`, y `profesor`.

### `proc_plan_est.py`

Este script genera el archivo `plan_de_estudios.csv`. Sus principales funciones son:
1.  Lee el archivo `cursos_malla.csv`.
2.  Determina el tipo de curso (Teórico, Práctico, Teórico-Práctico) basándose en las horas de teoría y práctica.
3.  Convierte los IDs de los requisitos y correquisitos a los códigos de curso correspondientes para mayor legibilidad.
4.  Calcula las horas de trabajo independiente (HE) a partir de los créditos y las horas de contacto (HC).
5.  Guarda el resultado en `plan_de_estudios.csv`.

### `proc_rasgos.py`

Este script genera la tabla `tabla_rasgos.csv`, que mapea los cursos con los rasgos del perfil del egresado.
1.  Lee los archivos `cursos_malla.csv`, `cursos_rasgos.csv`, `rasgos.csv` y `saberes.csv`.
2.  Filtra los cursos para incluir solo los de la malla curricular principal (semestres 1-10, excluyendo electivas).
3.  Crea una tabla donde las filas son los cursos y las columnas son los rasgos.
4.  Marca con una 'X' si un curso contribuye a un rasgo específico, basándose en la relación entre cursos, saberes y rasgos.
5.  Guarda la tabla resultante en `tabla_rasgos.csv`.

## Archivos de Datos (CSV)

Estos archivos contienen la información base sobre los cursos.

-   **`cursos_atributo.csv`**: Asocia un curso (`id`) con un atributo específico (`atributo`) y un nivel de dominio (`nivel`).
-   **`cursos_bibtex.csv`**: Contiene las referencias bibliográficas (`bibtex`) para cada curso (`id`).
-   **`cursos_conten.csv`**: Almacena los contenidos temáticos detallados (`contenidos`) para cada curso (`id`).
-   **`cursos_cursos.csv`**: Define las relaciones de prerrequisitos y cursos posteriores. Contiene las columnas `id`, `antes` (cursos que se toman antes) y `despues` (cursos que se toman después).
-   **`cursos_detalles.csv`**: Proporciona detalles administrativos de los cursos, como `tipo` (teórico, práctico), si es `electivo`, y políticas de `asistencia`, `suficiencia`, `reconocimiento` y `aprobacion`.
-   **`cursos_equiv.csv`**: Mapea el `id` interno de un curso con su `codigo` y `nombre` oficial, posiblemente para gestionar equivalencias.
-   **`cursos_evalua.csv`**: Asigna un tipo de evaluación (`tipoEval`) a cada curso (`id`).
-   **`cursos_malla.csv`**: Archivo central con la estructura de la malla curricular. Incluye `id`, `codigo`, `nombre`, `area`, `semestre`, `fila` (posición en la malla), horas, créditos y requisitos.
-   **`cursos_malla_MI.csv`**: Parece ser una versión de la malla curricular para el énfasis de Mantenimiento Industrial.
-   **`cursos_metodo.csv`**: Describe la metodología de enseñanza (`metodologia`) para cada curso (`id`).
-   **`cursos_obj.csv`**: Define los objetivos de aprendizaje (`objetivo`) para cada curso (`id`).
-   **`cursos_profes.csv`**: Asigna uno o más profesores (`profesores`) a cada curso (`id`). Los códigos de los profesores están separados por punto y coma.
-   **`cursos_programas.csv`**: Indica a qué programa o énfasis (`programa`) pertenece cada curso (`id`) y en qué `semestre` se imparte.
-   **`cursos_rasgos.csv`**: Vincula cada curso (`id`) con uno o más códigos de saber (`codSaber`) asociados a los rasgos del perfil del egresado.
-   **`descri_evalua.csv`**: Contiene la descripción de los diferentes tipos de evaluación (`evaluacion`).
-   **`descri_metodo.csv`**: Describe los diferentes tipos de metodologías de enseñanza (`tipo`).
-   **`plan_de_estudios.csv`**: Tabla generada por `proc_plan_est.py`. Contiene un resumen del plan de estudios con códigos de curso legibles.
-   **`tabla_profes.csv`**: Tabla generada por `proc_cursos_profes.py`. Muestra la relación entre semestre, curso y profesor.
-   **`tabla_rasgos.csv`**: Tabla generada por `proc_rasgos.py`. Muestra la matriz de cursos vs. rasgos del egresado.
-   **`tipos_evalua.csv`**: Define la ponderación y cantidad de las diferentes evaluaciones para cada tipo de curso.
