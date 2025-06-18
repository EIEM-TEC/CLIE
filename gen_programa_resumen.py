import pandas as pd
import csv

cursos = pd.read_csv("cursos/cursos_malla.csv")
detall = pd.read_csv("cursos/cursos_detalles.csv")
objeti = pd.read_csv("cursos/cursos_obj.csv")
conten = pd.read_csv("cursos/cursos_conten.csv")
rasgos = pd.read_csv("rasgos_ejes/rasgos.csv")
rasgos["codSaber"] = rasgos["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
rasgos = rasgos.explode("codSaber") #expadir la lista
curras = pd.read_csv("cursos/cursos_rasgos.csv")
curras["codSaber"] = curras["codSaber"].str.split(';', expand=False)
curcur = pd.read_csv("cursos/cursos_cursos.csv")
curAntes = pd.DataFrame()
curAntes = curcur[["id","antes"]].copy()
curAntes["antes"] = curAntes["antes"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
curAntes = curAntes.explode("antes")
curDespues = pd.DataFrame()
curDespues = curcur[["id","despues"]].copy()
curDespues["despues"] = curDespues["despues"].str.split(';', expand=False)#convertir los valores separados por ; en una lista por fila
curDespues = curDespues.explode("despues")

def construir_descripcion(id):
    codCurso = cursos[cursos.id == id].codigo.item()
    desGener = "" 
    nomCurso = cursos[cursos.id == id].nombre.item()
    semCurso = cursos[cursos.id == id].semestre.item()
    if semCurso <= 10:
        codSaber = curras[curras["id"]==id]["codSaber"].item()
        codRasgos = rasgos[rasgos["codSaber"].isin(codSaber)]["rasgo"].unique()
        desGener += "El curso de " + f"{nomCurso}" + " aporta en el desarrollo "
        if len(codRasgos) > 1:
            desGener += "de los siguientes rasgos del plan de estudios: "
        else:
            desGener += "del siguiente rasgo del plan de estudios: "
        for index, rasgo in enumerate(codRasgos):
            desGener += f"{rasgo[0].lower() + rasgo[1:]}"
            if index == len(codRasgos) - 2:
                desGener += "; y "
            elif index < len(codRasgos) - 2:
                desGener += "; "
    else:
        codSaber = ""
        codRasgos = ""
        desGener = "El curso de " + f"{nomCurso}" + " es del tipo electivo y por esta razón no se incluye en los rasgos del plan de estudios"
    desGener += "\n"
    desGener += "Los aprendizajes que los estudiantes desarrollarán en el curso son: "
    lisObjet = objeti[objeti.id == id].reset_index(drop=True).objetivo
    for index, objetivo in lisObjet.items():
        if index > 0:
            if (index == len(lisObjet) - 1):
                if (objetivo[0].lower() == "i"):
                    desGener += "e "
                else:
                    desGener += "y "
            desGener += f"{objetivo[0].lower() + objetivo[1:]}"
            if index <= len(lisObjet) - 2:
                desGener += "; "
    desGener += "."
    return desGener

def limpiar_contenidos(contenido):
    if pd.isna(contenido):
        return ""
    
    # Separar líneas
    lineas = contenido.strip().splitlines()

    # Filtrar fuera las líneas con &&
    lineas_filtradas = [linea.strip() for linea in lineas if not linea.strip().startswith("&&")]

    # Reemplazar & por bullets o números
    lineas_formateadas = [f"• {linea.lstrip('&').strip()}" for linea in lineas_filtradas]

    # Unir en una sola cadena
    return "\n".join(lineas_formateadas)

lista_prog = ["CYD0107","FPH0108","AUT0205","IMM0207",
              "IEE0303","IEE0304","IEE0305","IMM0307",
              "IEE0403","IEE0404","IEE0405","IMM0407",
              "IEE0503","AUT0504","IMM0507","IMM0508",
              "ADD0602","IEE0604","IMM0605","IMM0607",
              "IMM0608","CYD0609","FPH0701","IEE0702",
              "IEE0703","AUT0704","AUT0705","IMM0706",
              "IMM0707","IMM0708","IEE0802","IEE0803",
              "AUT0804","AUT0805","INS0801","INS0806",
              "INS0807","INS0808","INS0901","INS0903",
              "INS0904","INS0905","INS0906","INS0907",
              "INS0908","INS0909","INS1003","INS1005",
              "INS1006","INS1007","INS1201","INS1202",
              "INS1203","AER0801","AER0807","AER0808",
              "AER0901","AER0902","AER0903","AER0906",
              "AER0908","AER1001","AER1002","AER1003",
              "AER1201","AER1202","AER1203","SCF0801",
              "SCF0806","SCF0807","SCF0808","SCF0901",
              "SCF0902","SCF0903","SCF0906","SCF0907",
              "SCF1001","SCF1002","SCF1007","SCF1201",
              "SCF1202","SCF1203"]

resumen = pd.DataFrame()
resumen[["id","codigo","nombre","creditos"]] = cursos[["id","codigo","nombre","creditos"]]
resumen = resumen[resumen["id"].isin(lista_prog)]
# resumen = resumen[~resumen["id"].isin(["AER0905","AER1005","SCF0905","SCF1005"])]
# resumen = resumen[~resumen["codigo"].isin(["EE1103","EE1104","EE1501"])]
resumen["descripcion"] = resumen["id"].apply(lambda x: construir_descripcion(x))
objeti = objeti[objeti["consecutivo"] == 0].drop(columns="consecutivo")
resumen = resumen.merge(objeti, on="id", how="left")
conten["contenidos"] = conten["contenidos"].apply(limpiar_contenidos)
resumen = resumen.merge(conten, on="id", how="left")

resumen.to_csv("resumen_pograma_cursos.csv", index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')

print(resumen)