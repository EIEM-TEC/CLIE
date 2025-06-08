import subprocess
import roman
import pandas as pd
import numpy as np
from pylatex import Document, Package, Command, PageStyle, Head, Foot, NewPage, NewLine,\
    TextColor, MiniPage, StandAloneGraphic, simple_page_number,\
    TikZ, TikZNode, TikZOptions, TikZCoordinate,\
    VerticalSpace, HorizontalSpace,\
    LongTabularx, Tabularx,\
    config
from pylatex.base_classes import Arguments
from pylatex.utils import NoEscape, bold
import funciones as fun

cursos = pd.read_csv("cursos/cursos_malla.csv")
detall = pd.read_csv("cursos/cursos_detalles.csv")
progra = pd.read_csv("cursos/cursos_programas.csv")
objeti = pd.read_csv("cursos/cursos_obj.csv")
conten = pd.read_csv("cursos/cursos_conten.csv")
metodo = pd.read_csv("cursos/cursos_metodo.csv")
metdes = pd.read_csv("cursos/descri_metodo.csv")
evalua = pd.read_csv("cursos/cursos_evalua.csv")
evades = pd.read_csv("cursos/descri_evalua.csv")
evatip = pd.read_csv("cursos/tipos_evalua.csv")
bibtex = pd.read_csv("cursos/cursos_bibtex.csv")
profes = pd.read_csv("cursos/cursos_profes.csv")
rasgos = pd.read_csv("rasgos_ejes/rasgos.csv")
rasgos["codSaber"] = rasgos["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
rasgos = rasgos.explode("codSaber") #expadir la lista
curras = pd.read_csv("cursos/cursos_rasgos.csv")
curras["codSaber"] = curras["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
curcur = pd.read_csv("cursos/cursos_cursos.csv")
curAntes = pd.DataFrame()
curAntes = curcur[["id","antes"]].copy()
curAntes["antes"] = curAntes["antes"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
curAntes = curAntes.explode("antes")
curDespues = pd.DataFrame()
curDespues = curcur[["id","despues"]].copy()
curDespues["despues"] = curDespues["despues"].str.split(';', expand=False)#convertir los valores separados por ; en una lista por fila
curDespues = curDespues.explode("despues")
datProfes = pd.read_csv("profes_datos.csv")
areas = pd.read_csv("areas.csv")

tipCursoDic = {
    0: "Teórico",
    1: "Práctico",
    2: "Teórico - Práctico"
}

eleCursoDic = {
    0: "Obligatorio",
    1: "Electivo"
}

tipAsistDic = {
    0: "Libre",
    1: "Obligatoria" 
}

sinoDic = {
    0: "No",
    1: "Sí" 
}


def textcolor(size,vspace,color,bold,text,hspace="0",par=True):
    dump = NoEscape(r"")
    if par==True:
        dump = NoEscape(r"\par")
    if hspace!="0":
        dump += NoEscape(HorizontalSpace(hspace,star=True).dumps())
    dump += NoEscape(Command("fontsize",arguments=Arguments(size,vspace)).dumps())
    dump += NoEscape(Command("selectfont").dumps()) + NoEscape(" ")
    if bold==True:
        dump += NoEscape(Command("textbf", NoEscape(Command("textcolor",arguments=Arguments(color,text)).dumps())).dumps())
    else:
        dump += NoEscape(Command("textcolor",arguments=Arguments(color,text)).dumps())
    return dump

def fontselect(size,vspace):
    dump = NoEscape(r"")
    dump += NoEscape(Command("fontsize",arguments=Arguments(size,vspace)).dumps())
    dump += NoEscape(Command("selectfont").dumps()) + NoEscape(" ")
    return dump

def generar_programa(id):
    listProf = profes[profes.id == id].profesores.str.split(';').item()
    codCurso = cursos[cursos.id == id].codigo.item()
    areCurso = cursos[cursos.id == id].area.item()
    nomEscue = "Escuela de Ingeniería Electromecánica"
    lisProgr = progra[progra.id == id].drop('id',axis=1)
    numProgr = len(lisProgr.programa)
    counter = 0
    if numProgr > 1:
        strProgr = "Carreras de: "
    else:
        strProgr = "Carrera de "
    for programa in lisProgr.programa:
        counter += 1
        strProgr += programa
        if counter < numProgr:
            if numProgr == 2:
                strProgr += " y "
            else:
                strProgr += ", "  
    nomCurso = cursos[cursos.id == id].nombre.item()
    print(f'Curso: {nomCurso}')
    tipo = detall[detall.id == id].tipo.item()
    tipCurso = tipCursoDic.get(detall[detall.id == id].tipo.item())
    eleCurso = eleCursoDic.get(detall[detall.id == id].electivo.item())
    numCredi = cursos[cursos.id == id].creditos.item()
    horClass = cursos[cursos.id == id].horasTeoria.item() + cursos[cursos.id == id].horasPractica.item()
    horExtra = (numCredi * 3) - horClass
    semCurso = cursos[cursos.id == id].semestre.item()
    ubiPlane = ""
    counter = 0
    for programa in lisProgr.programa:
        counter +=1
        semestre = lisProgr[lisProgr['programa'] == programa].semestre.item()
        if semestre <= 10:
            ubiPlane += "Curso de " + fun.number_to_ordinals(str(int(semestre))) + " semestre en " + programa
        elif semestre > 10:
            ubiPlane += "Curso electivo en " + programa
        if counter > 1:
            ubiPlane += " "
    susRequi = ""
    lisRequi = cursos[cursos.id == id].requisitos.item()
    if str(lisRequi) != "nan":
        lisRequi = cursos[cursos.id == id].requisitos.str.split(';').explode().reset_index(drop=True)
        numRequi = len(lisRequi)
        counter = 0
        for requisito in lisRequi:
            counter += 1
            susRequi += cursos[cursos.id == requisito].codigo.item()[:2] + "-" + cursos[cursos.id == requisito].codigo.item()[2:]
            susRequi += " "
            susRequi += cursos[cursos.id == requisito].nombre.item()
            if counter < numRequi:
                susRequi += "; "
            else:
                susRequi += " "
    else:
        susRequi += "Ninguno"
    corRequi = ""
    lisCorre = cursos[cursos.id == id].correquisitos.item()
    if str(lisCorre) != "nan":
        lisCorre = cursos[cursos.id == id].correquisitos.str.split(';').explode().reset_index(drop=True)
        numCorre = len(lisCorre)
        counter = 0
        for correquisito in lisCorre:
            counter += 1
            corRequi += cursos[cursos.id == correquisito].codigo.item()[:2] + "-" + cursos[cursos.id == correquisito].codigo.item()[2:]
            corRequi += " "
            corRequi += cursos[cursos.id == correquisito].nombre.item()
            if counter < numCorre:
                corRequi += "; "
            else:  
                corRequi += " "
    else:
        corRequi += "Ninguno"
    essRequi = NoEscape("")
    lisEsreq = cursos[cursos.id == id].esrequisito.item()
    if str(lisEsreq) != "nan":
        lisEsreq = cursos[cursos.id == id].esrequisito.str.split(';').explode().reset_index(drop=True)
        cTRC = 0
        trcRequi = ""
        cINS = 0
        insRequi = ""
        cAER = 0
        aerRequi = ""
        cSCF = 0
        scfRequi = ""
        for esrequisito in lisEsreq:      
            areaEsreq = cursos[cursos.id == esrequisito].area.item()
            if (areaEsreq not in ["INS","AER","SCF"]):
                if cTRC != 0:
                    trcRequi += "; "
                trcRequi += cursos[cursos.id == esrequisito].codigo.item()[:2] + "-" + cursos[cursos.id == esrequisito].codigo.item()[2:]
                trcRequi += " "
                trcRequi += cursos[cursos.id == esrequisito].nombre.item()
                cTRC += 1  
        for esrequisito in lisEsreq:      
            areaEsreq = cursos[cursos.id == esrequisito].area.item()        
            if areaEsreq == "INS":   
                if cINS == 0:
                    if cTRC != 0:                        
                        insRequi += ". "
                    insRequi += r"\emph{Énfasis en Instalaciones Electromecánicas:} "
                else:
                    insRequi += "; "  
                insRequi += cursos[cursos.id == esrequisito].codigo.item()[:2] + "-" + cursos[cursos.id == esrequisito].codigo.item()[2:]
                insRequi += " "
                insRequi += cursos[cursos.id == esrequisito].nombre.item()
                cINS += 1
            elif areaEsreq == "AER":
                if cAER == 0:
                    if cTRC != 0:
                       aerRequi += ". "
                    aerRequi += r"\emph{Énfasis en Aeronáutica:} "
                else:
                    aerRequi += "; " 
                aerRequi += cursos[cursos.id == esrequisito].codigo.item()[:2] + "-" + cursos[cursos.id == esrequisito].codigo.item()[2:]
                aerRequi += " "
                aerRequi += cursos[cursos.id == esrequisito].nombre.item()             
                cAER += 1
            elif areaEsreq == "SCF":
                if cSCF == 0:
                    if cTRC != 0:
                       scfRequi += ". "
                    scfRequi += r"\emph{Énfasis en Sistemas Ciberfísicos:} "
                else:
                    scfRequi += "; "
                scfRequi += cursos[cursos.id == esrequisito].codigo.item()[:2] + "-" + cursos[cursos.id == esrequisito].codigo.item()[2:]
                scfRequi += " "
                scfRequi += cursos[cursos.id == esrequisito].nombre.item()
                cSCF += 1
        essRequi = NoEscape(trcRequi) + NoEscape(insRequi) + NoEscape(aerRequi) + NoEscape(scfRequi)
    else:
        essRequi += NoEscape("Ninguno")
    tipAsist = tipAsistDic.get(detall[detall.id == id].asistencia.item())
    posSufic = sinoDic.get(detall[detall.id == id].suficiencia.item())
    posRecon = sinoDic.get(detall[detall.id == id].reconocimiento.item())
    aprCurso = detall[detall.id == id].aprobacion.str.split(';').explode().reset_index(drop=True)
    aprCurso = aprCurso[0] + "/" + aprCurso[1] + "/" + aprCurso[2] + " en sesión de Consejo de Escuela " + aprCurso[3]
    if semCurso <= 10:
        codSaber = curras[curras["id"]==id]["codSaber"].item()
        codRasgos = rasgos[rasgos["codSaber"].isin(codSaber)]["rasgo"].unique()
        desGener = NoEscape(r"El curso de " + r"\emph{" + f"{nomCurso}" + r"}" + r" aporta en el desarrollo ")
        if len(codRasgos) > 1:
            desGener += NoEscape(r"de los siguientes rasgos del plan de estudios: ")
        else:
            desGener += NoEscape(r"del siguiente rasgo del plan de estudios: ")
        for index, rasgo in enumerate(codRasgos):
            desGener += NoEscape(f"{rasgo[0].lower() + rasgo[1:]}")
            if index == len(codRasgos) - 2:
                desGener += NoEscape(f"; y ")
            elif index < len(codRasgos) - 2:
                desGener += NoEscape(f"; ")
    else:
        codSaber = ""
        codRasgos = ""
        desGener = NoEscape(r"El curso de " + r"\emph{" + f"{nomCurso}" + r"}" + r" es del tipo electivo y por esta razón no se incluye en los rasgos del plan de estudios")
    desGener += NoEscape(r". \newline\newline ")
    desGener += NoEscape(r"Los aprendizajes que los estudiantes desarrollarán en el curso son: ")
    lisObjet = objeti[objeti.id == id].reset_index(drop=True).objetivo
    for index, objetivo in lisObjet.items():
        if index > 0:
            if (index == len(lisObjet) - 1):
                if (objetivo[0].lower() == "i"):
                    desGener += NoEscape(f"e ")
                else:
                    desGener += NoEscape(f"y ")
            desGener += NoEscape(f"{objetivo[0].lower() + objetivo[1:]}")
            if index <= len(lisObjet) - 2:
                desGener += NoEscape(f"; ")
    desGener += NoEscape(r". \newline\newline ")
    curAntess = curAntes[curAntes["id"]==id]["antes"]
    if codCurso not in ["EE0108"]:
        desGener += NoEscape(r"Para desempeñarse adecuadamente en este curso, los estudiantes deben poner en práctica lo aprendido en ")
        if len(curAntess) > 1:
            desGener += NoEscape(r"los cursos de: ")
        else:
            desGener += NoEscape(r"el curso de: ")
        for index, curAnte in enumerate(curAntess):
            cursoAntes = cursos[cursos["id"]==curAnte].nombre.item()
            if index != 0:
                if index == len(curAntess) - 1:
                    if cursoAntes[0].lower() == "i":
                        desGener += NoEscape(f", e ")
                    else:
                        desGener += NoEscape(f", y ")                
                elif index < len(curAntess) - 1:
                    desGener += NoEscape(f", ")
            desGener += NoEscape(cursoAntes)
        desGener += NoEscape(r".")
    if int(id[3:5]) < 10:
        curDespuess = curDespues[curDespues["id"]==id]["despues"]
        desGener += NoEscape(r" \newline\newline Una vez aprobado este curso, los estudiantes podrán emplear algunos de los aprendizajes adquiridos en ")
        if len(curDespuess) > 1:
            desGener += NoEscape(r"los cursos de: ")
        else:
            desGener += NoEscape(r"el curso de: ")
        for index, curDespue in enumerate(curDespuess):
            cursoDespues = cursos[cursos["id"]==curDespue].nombre.item()
            if index != 0:
                if index == len(curDespuess) - 1:
                    if cursoDespues[0].lower() == "i":
                        desGener += NoEscape(f", e ")
                    else:
                        desGener += NoEscape(f", y ")
                elif index < len(curDespuess) - 1:
                    desGener += NoEscape(f", ")
            desGener += NoEscape(cursoDespues)
        desGener += NoEscape(r". ")
    for consecutivo, objetivo in lisObjet.items():
        if consecutivo == 0:
            objGener = NoEscape(objetivo)
            objEspec = NoEscape(r"\begin{itemize}")
        else:
            objEspec += NoEscape(r"\item ") + NoEscape(objetivo) + NoEscape(r".")
    objEspec += NoEscape(r"\end{itemize}")
    objCurso = NoEscape(r"Al final del curso la persona estudiante será capaz de:") 
    objCurso += NoEscape(r"\newline\newline ")
    objCurso += NoEscape(Command("textbf", "Objetivo general").dumps())
    objCurso += NoEscape(r"\begin{itemize}\item ")
    objCurso += objGener + NoEscape(r".")
    objCurso += NoEscape(r"\end{itemize} \vspace{2mm}")
    objCurso += NoEscape(Command("textbf", "Objetivos específicos").dumps())
    objCurso += objEspec
    if tipo == 1:
        if codCurso not in ["EE9001","EE1102"]:
            conDescr = "En el curso se desarrollaran los siguientes laboratorios:"
        else:
            conDescr = "En el curso se desarrollarán los siguientes temas:"
    else:
        conDescr = "En el curso se desarrollaran los siguientes temas:"
    conCurso = NoEscape(r"\par \setlength{\leftskip}{4cm} ")
    conCurso += NoEscape(r"\begin{easylist} \ListProperties(Progressive*=3ex)")
    conCurso += NoEscape(conten[conten.id == id].contenidos.item())
    conCurso += NoEscape(r"\end{easylist} ")
    conCurso += NoEscape(r"\setlength{\leftskip}{0cm} ")
    lisMetod = metodo[metodo.id == id].reset_index(drop=True).metodologia
    for consecutivo, metodos in lisMetod.items():
        if consecutivo == 0:
            metGener = NoEscape(metdes[metdes["tipo"]==tipo].descripcion.item())
            metEspec = NoEscape(r"\begin{itemize}")
            metEspec += NoEscape(r"\item ") + NoEscape(metodos)
        else:
            metEspec += NoEscape(r"\item ") + NoEscape(metodos)
    metEspec += NoEscape(r"\end{itemize}")
    metCurso = metGener
    metCurso += NoEscape(r"\newline\newline ")
    metCurso += NoEscape(Command("textbf", "Las personas estudiantes podrán desarrollar actividades en las que:").dumps() + r" \newline")
    metCurso += metEspec
    metCurso += NoEscape(r"\vspace*{2mm}")
    metCurso += NoEscape(f"Este enfoque metodológico permitirá a la persona estudiante {objGener[0].lower() + objGener[1:]}")
    metCurso += NoEscape(r"\vspace*{2mm} \newline  ")
    metCurso += NoEscape(r"Si un estudiante requiere apoyos educativos, podrá solicitarlos a través del Departamento de Orientación y Psicología. \newline ")
    evaCurso = NoEscape(r"La evaluación se distribuye en los siguientes rubros:")
    evaCurso += NoEscape(r" \newline ")
    tipEvalu = evalua[evalua.id == id].tipoEval.item()
    lisEvalu = evatip[(evatip.tipo == tipo) & (evatip.tipoEval == tipEvalu)].reset_index(drop=True)
    for consecutivo, evaluas in lisEvalu.iterrows():
        if consecutivo == 0:
            descriEval = NoEscape(r"\begin{itemize} ")  
        descriEval += NoEscape(r"\item ") + NoEscape(f"{evaluas.evaluacion}: {evades[evades["evaluacion"]==evaluas.evaluacion].descripcion.item()}")  
    descriEval += NoEscape(r"\end{itemize}") 
    evaCurso += descriEval
    evaTabla = NoEscape(r" \begin{minipage}{\linewidth} ")
    evaTabla += NoEscape(r" \centering ") 
    evaTabla += NoEscape(r" \begin{tabular}{ p{4.5cm}  p{1.5cm} } ")
    evaTabla += NoEscape(r" \toprule ") 
    total = 0
    for consecutivo, evaluas in lisEvalu.iterrows():
        evaTabla += NoEscape(f" {evaluas.evaluacion} ({evaluas.cantidad}) & {evaluas.porcentaje} \\%") + NoEscape(r" \\ ")
        evaTabla += NoEscape(r" \midrule ")
        total += evaluas.porcentaje
        if consecutivo == len(lisEvalu)-1:
            evaTabla += NoEscape(f"Total & {total} \\%") + NoEscape(r" \\ ")
            evaTabla += NoEscape(r" \bottomrule ")
    evaTabla += NoEscape(r" \end{tabular} \end{minipage}")
    evaRepo = NoEscape(r"De conformidad con el artículo 78 del Reglamento del Régimen Enseñanza-Aprendizaje del Instituto Tecnológico de Costa Rica y sus Reformas, en este curso la persona estudiante ")
    if tipCurso != "Teórico":
        evaRepo += NoEscape(Command("textbf", "no").dumps())
    evaRepo += NoEscape(r" tiene derecho a presentar un examen de reposición")
    if tipCurso == "Teórico":
        evaRepo += NoEscape(r" si su nota luego de redondeo es 60 o 65.")
    else:
        evaRepo += NoEscape(r".")
    bibCurso = NoEscape(r'\nocite{' + ('} '+r'\nocite{').join(bibtex[bibtex.id == id].bibtex.item().split(';')) + '} ')
    bibPrint = NoEscape(r'\vspace*{-8mm}\printbibliography[heading=none]')
    dataProf = datProfes[datProfes.Codigo.isin(listProf)]
    proImpar = NoEscape(r"El curso será impartido por:")
    proCurso = NoEscape(r'\vspace*{-4mm}\begin{textoMargen}')
    for consecutivo, profe in dataProf.iterrows():
        print(f'Profesor: {profe.Nombre}')
        match profe.Titulo:
            case "M.Sc." | "Ing." | "Máster" | "Dr.-Ing." | "Mag.":
                proCurso += NoEscape(Command("textbf", f"{profe.Titulo} {profe.Nombre}").dumps())
            case "Ph.D.":
                proCurso += NoEscape(Command("textbf", f"{profe.Nombre}, {profe.Titulo}").dumps())
        proCurso += NoEscape(r" \newline ")
        for titulo in profe.Titulos.split(';'):
            proCurso += NoEscape(f"{titulo}")
            proCurso += NoEscape(r" \newline \newline ")   
        proCurso += NoEscape(Command("emph", "Correo:").dumps())               
        proCurso += NoEscape(f" {profe.Correo}")
        proCurso += NoEscape(Command("emph", "  Teléfono:").dumps())     
        proCurso += NoEscape(f" {int(profe.Telefono)}")
        proCurso += NoEscape(r" \vspace*{1mm} \newline ")
        proCurso += NoEscape(Command("emph", "  Oficina:").dumps())    
        proCurso += NoEscape(f" {int(profe.Oficina)}")
        proCurso += NoEscape(Command("emph", "  Escuela:").dumps())  
        proCurso += NoEscape(f" {profe.Escuela}")
        proCurso += NoEscape(Command("emph", "  Sede:").dumps())  
        proCurso += NoEscape(f" {profe.Sede}")
        proCurso += NoEscape(r" \vspace*{4mm} \newline ")             
    proCurso += NoEscape(r"\end{textoMargen}")
    #Config
    config.active = config.Version1(row_heigth=1.5)
    #Geometry
    geometry_options = { 
        "left": "22.5mm",
        "right": "16.1mm",
        "top": "48mm",
        "bottom": "25mm",
        "headheight": "12.5mm",
        "footskip": "12.5mm"
    }
    #Document options
    doc = Document(documentclass="article", \
                   fontenc=None, \
                   inputenc=None, \
                   lmodern=False, \
                   textcomp=False, \
                   page_numbers=True, \
                   indent=False, \
                   document_options=["letterpaper"],
                   geometry_options=geometry_options)
    #Packages
    doc.packages.append(Package(name="fontspec", options=None))
    doc.packages.append(Package(name="babel", options=['spanish','activeacute']))
    doc.packages.append(Package(name="anyfontsize"))
    doc.packages.append(Package(name="fancyhdr"))
    doc.packages.append(Package(name="csquotes"))
    doc.packages.append(Package(name="easylist", options=['ampersand']))
    doc.packages.append(Package(name="biblatex", options=['style=ieee','backend=biber']))
    doc.packages.append(Package(name="tcolorbox",options=['skins','breakable']))
    doc.packages.append(Package(name="booktabs"))
    #Package options
    doc.preamble.append(Command('setmainfont','Arial'))
    doc.preamble.append(Command('addbibresource', '../bibFPH.bib'))
    doc.preamble.append(Command('addbibresource', '../bibADD.bib'))
    doc.preamble.append(Command('addbibresource', '../bibAUT.bib'))
    doc.preamble.append(Command('addbibresource', '../bibCYD.bib'))
    doc.preamble.append(Command('addbibresource', '../bibIEE.bib'))
    doc.preamble.append(Command('addbibresource', '../bibIMM.bib'))
    doc.preamble.append(Command('addbibresource', '../bibINS.bib'))
    doc.preamble.append(Command('addbibresource', '../bibAER.bib'))
    doc.preamble.append(Command('addbibresource', '../bibSCF.bib'))
    doc.preamble.append(NoEscape(r'\renewcommand*{\bibfont}{\fontsize{10}{14}\selectfont}'))
    doc.preamble.append(NoEscape(r'''
\defbibenvironment{bibliography}
    {\list
    {\printfield[labelnumberwidth]{labelnumber}}
    {\setlength{\leftmargin}{4cm}
    \setlength{\rightmargin}{1.1cm}
    \setlength{\itemindent}{0pt}
    \setlength{\itemsep}{\bibitemsep}
    \setlength{\parsep}{\bibparsep}}}
    {\endlist}
{\item}
'''))
    doc.preamble.append(NoEscape(r'''
\newenvironment{textoMargen}
    {%
    \begin{list}{}{%
        \setlength{\leftmargin}{3.6cm}%
        \setlength{\rightmargin}{1.1cm}%
    }%
    \item[]%
  }
  {%
    \end{list}%
  }
'''))
    doc.add_color('gris','rgb','0.27,0.27,0.27') #70,70,70
    doc.add_color('parte','rgb','0.02,0.204,0.404') #5,52,103
    doc.add_color('azulsuaveTEC','rgb','0.02,0.455,0.773') #5,116,197
    doc.add_color('fila','rgb','0.929,0.929,0.929') #237,237,237
    doc.add_color('linea','rgb','0.749,0.749,0.749') #191,191,191

    headerfooter = PageStyle("headfoot")

    #Left header
    with headerfooter.create(Head("L")) as header_left:
        with header_left.create(MiniPage(width=r"0.5\textwidth",align="l")) as logobox:
            logobox.append(StandAloneGraphic(image_options="width=62.5mm", filename='../figuras/Logo.png'))
    #Right foot
    with headerfooter.create(Foot("R")) as footer_right:
        footer_right.append(TextColor("black", NoEscape(r"Página \thepage \hspace{1pt} de \pageref*{LastPage}")))        
    #Add header and footer 
    doc.preamble.append(headerfooter)
    doc.change_page_style("empty")
    #Set logo in first page
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "overlay",
                "remember picture"
                )
        )) as logo:
        logo.append(TikZNode(\
            options=TikZOptions
                (
                "inner sep = 0mm",
                "outer sep = 0mm",
                "anchor = north west",
                "xshift = -23mm",
                "yshift = 22mm"
                ),
            text=StandAloneGraphic(image_options="width=21cm", filename='../figuras/Logo_portada.png').dumps(),\
            at=TikZCoordinate(0,0)
        ))
    doc.append(VerticalSpace("100mm", star=True))
    doc.append(textcolor
            (   
            size="14",
            vspace="0",
            color="black",
            bold=False,
            text=f"Programa del curso {str(codCurso)[:2]}-{str(codCurso)[2:]}"
            ))
    doc.append(textcolor
            (
            size="18",
            vspace="25",
            color="black",
            bold=True,
            text=f"{nomCurso}" 
            ))
    doc.append(VerticalSpace("15mm", star=True))
    doc.append(NewLine())
    with doc.create(Tabularx(table_spec=r"m{0.02\textwidth}m{0.98\textwidth}")) as table:
            table.add_row(["", textcolor
            (   
            par=False,
            hspace="0mm",
            size="12",
            vspace="0",
            color="gris",
            bold=True,
            text=f"{nomEscue}"
            )])
            table.append(NoEscape('[-12pt]'))
            table.add_row(["", textcolor
            (   
            par=False,
            hspace="0mm",
            size="12",
            vspace="0",
            color="gris",
            bold=True,
            text=f"{strProgr}" 
            )])
    doc.append(NewPage())
    doc.change_document_style("headfoot")
    doc.append(textcolor
            (   
            size="14",
            vspace="0",
            color="parte",
            bold=True,
            text="I parte: Aspectos relativos al plan de estudios"
            ))
    doc.append(textcolor
            (   
            hspace="2mm",
            size="12",
            vspace="14",
            color="parte",
            bold=True,
            text="1. Datos generales"
            ))
    doc.append(VerticalSpace("3mm", star=True))
    doc.append(NewLine())
    doc.append(fontselect
            (
            size="10",
            vspace="12"      
            ))
    with doc.create(Tabularx(table_spec=r"p{6cm}p{10cm}")) as table:
            table.add_row([bold("Nombre del curso:"), f"{nomCurso}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Código:"), f"{str(codCurso)[:2]}-{str(codCurso)[2:]}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Tipo de curso:"), f"{tipCurso}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Obligatorio o electivo:"), f"{eleCurso}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Nº de créditos:"), f"{numCredi}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Nº horas de clase por semana:"), f"{horClass}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Nº horas extraclase por semana:"), f"{horExtra}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Ubicación en el plan de estudios:"), NoEscape(f"{ubiPlane}")])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Requisitos:"), f"{susRequi}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Correquisitos:"), f"{corRequi}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("El curso es requisito de:"), NoEscape(f"{essRequi}")])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Asistencia:"), f"{tipAsist}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Suficiencia:"), f"{posSufic}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Posibilidad de reconocimiento:"), f"{posRecon}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Aprobación y actualización del programa:"), f"{aprCurso}"])
            table.append(NoEscape('[10pt]'))
    doc.append(NewPage())
    with doc.create(Tabularx(table_spec=r"p{3cm}p{13cm}")) as table:
            table.add_row([textcolor
            (   
            size="12",
            vspace="14",
            color="parte",
            bold=True,
            text="2. Descripción general"
            )
            ,desGener])  
    doc.append(VerticalSpace("4mm", star=True))  
    doc.append(NewLine())
    with doc.create(Tabularx(table_spec=r"p{3cm}p{13cm}")) as table:
            table.add_row([textcolor
            (   
            size="12",
            vspace="14",
            color="parte",
            bold=True,
            text="3. Objetivos"
            )
            ,objCurso])
    doc.append(VerticalSpace("4mm", star=True)) 
    if id in ["CYD0609"]:
        doc.append(NewPage())
    else:
        doc.append(NewLine())
    with doc.create(Tabularx(table_spec=r"p{3cm}p{13cm}")) as table:
        table.add_row([textcolor
        (   
        size="12",
        vspace="14",
        color="parte",
        bold=True,
        text="4. Contenidos"
        )
        ,conDescr])
    doc.append(NewLine())
    doc.append(conCurso)
    doc.append(textcolor
        (   
        size="14",
        vspace="0",
        color="parte",
        bold=True,
        text="II parte: Aspectos operativos"
        ))
    doc.append(VerticalSpace("4mm", star=True))  
    doc.append(NewLine())
    doc.append(fontselect
        (
        size="10",
        vspace="12"      
        ))
    with doc.create(Tabularx(table_spec=r"p{3cm}p{13cm}")) as table:
        table.add_row([textcolor
        (   
        size="12",
        vspace="14",
        color="parte",
        bold=True,
        text="5. Metodología"
        )
        ,metCurso])
    doc.append(VerticalSpace("2mm", star=True))  
    doc.append(NewLine())
    with doc.create(Tabularx(table_spec=r"p{3cm}p{13cm}")) as table:
        table.add_row([textcolor
        (   
        size="12",
        vspace="14",
        color="parte",
        bold=True,
        text="6. Evaluación"
        )
        ,evaCurso])
    doc.append(VerticalSpace("2mm", star=True))  
    doc.append(NewLine())
    doc.append(evaTabla)
    doc.append(VerticalSpace("2mm", star=True))  
    doc.append(NewLine())
    with doc.create(Tabularx(table_spec=r"p{3cm}p{13cm}")) as table:
        table.add_row([""
        ,evaRepo])
    doc.append(VerticalSpace("4mm", star=True))  
    doc.append(NewLine()) #antes era newline
    with doc.create(Tabularx(table_spec=r"p{3cm}p{13cm}")) as table:
        table.add_row([textcolor
        (   
        size="12",
        vspace="14",
        color="parte",
        bold=True,
        text="7. Bibliografía"
        )
        ,bibCurso]) 
    doc.append(bibPrint)
    # doc.append(VerticalSpace("2mm", star=True))  
    # doc.append(NewLine())
    with doc.create(Tabularx(table_spec=r"p{3cm}p{13cm}")) as table:
        table.add_row([textcolor
        (   
        size="12",
        vspace="14",
        color="parte",
        bold=True,
        text="8. Persona docente"
        )
        ,proImpar])
    doc.append(proCurso)

    doc.generate_pdf(f"./programas/{codCurso}", clean=False, clean_tex=False, compiler='lualatex')
    subprocess.run(["biber", f"C:\\Repositories\\CLIE\\programas\\{codCurso}"])
    doc.generate_pdf(f"./programas/{codCurso}", clean=False, clean_tex=False, compiler='lualatex')
    doc.generate_pdf(f"./programas/{codCurso}", clean=False, clean_tex=False, compiler='lualatex') 
    subprocess.run(f'move "C:\\Repositories\\CLIE\\programas\\{codCurso}.pdf" "C:\\Repositories\\CLIE\\programas\\{codCurso}-{nomCurso}.pdf"', shell=True, check=True)

# for id in cursos.id:
#      generar_programa(id)

# generar_programa("CYD0107") #Dibujo Tec
# generar_programa("FPH0108") # int ing. electromecanica
# #generar_programa("AUT0205") #Int. Compu
# generar_programa("IMM0207") #estatica
# generar_programa("IEE0303") #circuitos I
# generar_programa("IEE0304") #Lab Circuitos I
# generar_programa("IEE0305") #Transductores
# generar_programa("IMM0307") #Dinamica
# generar_programa("IEE0403") #circuitos II
# generar_programa("IEE0404") #Lab Circuitos II
# generar_programa("IEE0405")
# generar_programa("IMM0407")
# generar_programa("ADD0502") #estadistica
# generar_programa("IEE0503")
# generar_programa("AUT0504")
# #generar_programa("IMM0506") #materiales
# generar_programa("IMM0507") #manufactura
# generar_programa("IMM0508") #lab manufactura
# generar_programa("ADD0602")
# generar_programa("IEE0604")
# generar_programa("IMM0605") #resi
# generar_programa("IMM0607") #mec fluidos
# generar_programa("IMM0608") #lab mec fluidos
# generar_programa("CYD0609") #dib ind
# generar_programa("FPH0701") #proyectos
# generar_programa("IEE0702") #Maquinas I
# generar_programa("IEE0703") #Lab Maquinas I
# generar_programa("AUT0704") #control
# generar_programa("AUT0705") #micros
# generar_programa("IMM0706") #elementos maq
# generar_programa("IMM0707") #sist termicos
# generar_programa("IEE0802") #Maquinas II
# generar_programa("IEE0803") #Lab Maquinas II
# generar_programa("AUT0804") #Control por event.
# generar_programa("AUT0805") #Lab control
# generar_programa("INS0801") #Trans y distr
# generar_programa("INS0806") #Instalaciones
# generar_programa("INS0807") #Vent y aire comprimido
# generar_programa("INS0808") #Mant elec
# generar_programa("INS0901") #Gen y almacenamiento energia
# generar_programa("INS0903") #ref y AC
# generar_programa("INS0904") #lab ref y AC
# generar_programa("INS0905") #Sem I
# generar_programa("INS0906") #Inst mec-san
# generar_programa("INS0907") #Lab Sist Flu
# generar_programa("INS0908") #Vapor
# generar_programa("INS0909") # Lab Vapor
# generar_programa("INS1005") # Sem II
# generar_programa("INS1006") # Gestion ciclo vida electromecanica
# generar_programa("INS1007") # Neumática
# generar_programa("INS1201") # Sist puesta tierra
# generar_programa("INS1202") # Sist contra incendios
# generar_programa("INS1203") # Ed Inte
# generar_programa("AER0801") # sist de aeronaves
# generar_programa("AER0807") # mat en aeronáutica
# generar_programa("AER0808") # met aer
# generar_programa("AER0902") # aerodinamica
# generar_programa("AER0903") # dinamica de vuelo
# generar_programa("AER0906") # analisis estructural aeronaves
# generar_programa("AER0908") # seg y aeronav
# generar_programa("AER1001") # Gestion ciclo vida aeronaves
# generar_programa("AER1002") # Sist propuls
# generar_programa("AER1003") # Control de vuelo
# generar_programa("AER1202") # Com en aer
# generar_programa("AER1203") # man cad valor aer
# generar_programa("SCF0801") #Ing. Sistemas
# generar_programa("SCF0806") # maq y meca
generar_programa("SCF0807") # ap sist emb
# generar_programa("SCF0808") # fund de cibers
# generar_programa("SCF0901") # mod num
# generar_programa("SCF1001") # taller inte
# generar_programa("SCF1002") # HMI
# generar_programa("SCF1201") # sist autonomos y multiagente
# generar_programa("SCF1202") # an pred series
# generar_programa("SCF1203") # des soft ap crit


subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.tex"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.aux"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.bbl"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.bcf"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.blg"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.log"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.run.xml"], shell=True, check=True)