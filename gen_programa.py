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
descri = pd.read_csv("cursos/cursos_descri.csv")
objeti = pd.read_csv("cursos/cursos_obj.csv")
conten = pd.read_csv("cursos/cursos_conten.csv")
metodo = pd.read_csv("cursos/cursos_metodo.csv")
evalua = pd.read_csv("cursos/cursos_evalua.csv")
bibtex = pd.read_csv("cursos/cursos_bibtex.csv")
profes = pd.read_csv("cursos/cursos_profes.csv")
rasgos = pd.read_csv("rasgos_ejes/rasgos.csv")
rasgos["codSaber"] = rasgos["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
rasgos = rasgos.explode("codSaber") #expadir la lista
curras = pd.read_csv("cursos/cursos_rasgos.csv")
curras["codSaber"] = curras["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila
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
    1: "Si" 
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
    print(listProf)
    codCurso = cursos[cursos.id == id].codigo.item()
    nomEscue = "Escuela de Ingeniería Electromecánica"
    print(nomEscue)
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
    print(strProgr)
    nomCurso = cursos[cursos.id == id].nombre.item()
    print(f'Curso: {nomCurso}')
    tipCurso = tipCursoDic.get(detall[detall.id == id].tipo.item())
    print(f'Tipo: {tipCurso}')
    eleCurso = eleCursoDic.get(detall[detall.id == id].electivo.item())
    print(f'Obligatorio o electivo: {eleCurso}')
    numCredi = cursos[cursos.id == id].creditos.item()
    horClass = cursos[cursos.id == id].horasTeoria.item() + cursos[cursos.id == id].horasPractica.item()
    horExtra = (numCredi * 3) - horClass
    print(f'Créditos: {numCredi}, Horas clase: {horClass}, Horas extraclase: {horExtra}')
    ubiPlane = ""
    counter = 0
    for programa in lisProgr.programa:
        counter +=1
        semestre = lisProgr[lisProgr['programa'] == programa].semestre.item()
        ubiPlane += "Curso de " + fun.number_to_ordinals(str(int(semestre))) + " semestre en " + programa
        if counter > 1:
            ubiPlane += ". "
    print(ubiPlane)
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
        susRequi += "Ninguno"
    print(f'Requisitos: {susRequi}')
    corRequi = ""
    lisCorre = cursos[cursos.id == id].correquisitos.item()
    if str(lisCorre) != "nan":
        lisCorre = cursos[cursos.id == id].correquisitos.str.split(';').explode().reset_index(drop=True)
        numCorre = len(lisCorre)
        counter = 0
        for correquisito in lisCorre:
            counter += 1
            corRequi += cursos[cursos.id == correquisito].codigo.item()[:2] + "-" + cursos[cursos.id == requisito].codigo.item()[2:]
            corRequi += " "
            corRequi += cursos[cursos.id == correquisito].nombre.item()
            if counter < numCorre:
                corRequi += "; "
    else:
        corRequi += "Ninguno"
    print(f'Correquisitos: {corRequi}')
    essRequi = ""
    lisEsreq = cursos[cursos.id == id].esrequisito.item()
    if str(lisEsreq) != "nan":
        lisEsreq = cursos[cursos.id == id].esrequisito.str.split(';').explode().reset_index(drop=True)
        numEsreq = len(lisEsreq)
        counter = 0
        for esrequisito in lisEsreq:
            counter += 1
            essRequi += cursos[cursos.id == esrequisito].codigo.item()[:2] + "-" + cursos[cursos.id == requisito].codigo.item()[2:]
            essRequi += " "
            essRequi += cursos[cursos.id == esrequisito].nombre.item()
            if counter < numEsreq:
                essRequi += "; "
    else:
        essRequi += "Ninguno"
    print(f'Es requisito de: {essRequi}')
    tipAsist = tipAsistDic.get(detall[detall.id == id].asistencia.item())
    posSufic = sinoDic.get(detall[detall.id == id].suficiencia.item())
    posRecon = sinoDic.get(detall[detall.id == id].reconocimiento.item())
    print(f'Asistencia: {tipAsist}, Suficiencia: {posSufic}, Reconocimiento: {posRecon}') 
    aprCurso = detall[detall.id == id].aprobacion.str.split(';').explode().reset_index(drop=True)
    aprCurso = aprCurso[0] + "/" + aprCurso[1] + "/" + aprCurso[2] + " en sesión de Consejo de Escuela " + aprCurso[3]
    print(f'Aprobación del programa: {aprCurso}\n\n')
    print(curras[curras["id"]==id]["codSaber"])
    codSaber = curras[curras["id"]==id]["codSaber"].item()
    codRasgos = rasgos[rasgos["codSaber"].isin(codSaber)]["rasgo"].unique()
    desGener = NoEscape(r"El curso de " + r"\emph{" + f"{nomCurso}" + r"}" + r" colabora en el desarrollo de los siguientes rasgos del plan de estudios: ")
    for index, rasgo in enumerate(codRasgos):
        desGener += NoEscape(f"{rasgo[0].lower() + rasgo[1:]}")
        if index == len(codRasgos) - 2:
            desGener += NoEscape(f"; y ")
        elif index < len(codRasgos) - 2:
            desGener += NoEscape(f"; ")
    desGener += NoEscape(r". \newline\newline ")
    desGener += NoEscape(r"Los aprendizajes que los estudiantes desarrollarán en el curso son: ")
    #desGener = descri[descri.id == id].descripcion.item().replace("\n", "\n\n")
    lisObjet = objeti[objeti.id == id].reset_index(drop=True).objetivo
    for index, objetivo in lisObjet.items():
        desGener += NoEscape(f"{objetivo[0].lower() + objetivo[1:]}")
        if index == len(lisObjet) - 2:
            desGener += NoEscape(f"; y ")
        elif index < len(lisObjet) - 2:
            desGener += NoEscape(f"; ")
    desGener += NoEscape(r". \newline\newline ")
    desGener += NoEscape(r"Para desempeñarse adecuadamente en este curso, los estudiantes deben poner en práctica lo aprendido en los cursos de: ")
    for consecutivo, objetivo in lisObjet.items():
        if consecutivo == 0:
            objGener = NoEscape(objetivo)
            objEspec = NoEscape(r"\begin{itemize}")
        else:
            objEspec += NoEscape(r"\item ") + NoEscape(objetivo)
    objEspec += NoEscape(r"\end{itemize}")
    objCurso = NoEscape(r"Al final del curso la persona estudiante será capaz de:") 
    objCurso += NoEscape(r"\newline\newline ")
    objCurso += NoEscape(Command("textbf", "Objetivo general").dumps())
    objCurso += NoEscape(r"\begin{itemize}\item ")
    objCurso += objGener
    objCurso += NoEscape(r"\end{itemize} \vspace{2mm}")
    objCurso += NoEscape(Command("textbf", "Objetivos específicos").dumps())
    objCurso += objEspec
    conCurso = NoEscape(r"\par \setlength{\leftskip}{4cm} ")
    conCurso += NoEscape(r"\begin{easylist} \ListProperties(Progressive*=3ex)")
    conCurso += NoEscape(conten[conten.id == id].contenidos.item())
    conCurso += NoEscape(r"\end{easylist} ")
    conCurso += NoEscape(r"\setlength{\leftskip}{0cm} ")
    lisMetod = metodo[metodo.id == id].reset_index(drop=True).metodologia
    for consecutivo, metodos in lisMetod.items():
        if consecutivo == 0:
            metGener = NoEscape(metodos)
            metEspec = NoEscape(r"\begin{itemize}")
        else:
            metEspec += NoEscape(r"\item ") + NoEscape(metodos)
    metEspec += NoEscape(r"\end{itemize}")
    metCurso = metGener
    metCurso += NoEscape(r"\newline\newline ")
    metCurso += NoEscape(Command("textbf", "Los estudiantes:").dumps())
    metCurso += metEspec
    metCurso += NoEscape(r"\vspace*{2mm}")
    metCurso += NoEscape(f"Este enfoque metodológico permitirá a la persona estudiante {objGener[0].lower() + objGener[1:]}")
    metCurso += NoEscape(r"\vspace*{2mm} \newline  ")
    metCurso += NoEscape(r"Si un estudiante requiere apoyos educativos, podrá solicitarlos a través del Departamento de Orientación y Psicología.")
    evaCurso = NoEscape(r"La evaluación se distribuye en los siguientes rubros:")
    evaCurso += NoEscape(r"\vspace*{1mm} \newline  ")
    lisEvalu = evalua[evalua.id == id].reset_index(drop=True)
    for consecutivo, evaluas in lisEvalu.iterrows():
        if consecutivo == 0:
            descriEval = NoEscape(r"\begin{itemize} ")  
        descriEval += NoEscape(r"\item ") + NoEscape(f"{evaluas.evaluacion}: {evaluas.descripcion} ")  
    descriEval += NoEscape(r"\end{itemize}") 
    evaCurso += descriEval
    evaTabla = NoEscape(r" \begin{minipage}{\linewidth} ")
    evaTabla += NoEscape(r" \centering ") 
    evaTabla += NoEscape(r" \begin{tabular}{ p{4cm}  p{1.5cm} } ")
    evaTabla += NoEscape(r" \toprule ") 
    total = 0
    for consecutivo, evaluas in lisEvalu.iterrows():
        evaTabla += NoEscape(f" {evaluas.evaluacion} & {evaluas.porcentaje} \\% \\\ ")
        evaTabla += NoEscape(r" \midrule ")
        total += evaluas.porcentaje
        if consecutivo == len(lisEvalu)-1:
            evaTabla += NoEscape(f"Total & {total} \\% \\\ ")
            evaTabla += NoEscape(r" \bottomrule ")
    # #evaCurso += NoEscape(r" A & B \\ C & D \\ 
    evaTabla += NoEscape(r" \end{tabular} \end{minipage}")
    bibCurso = NoEscape(r'\nocite{' + ('} '+r'\nocite{').join(bibtex[bibtex.id == id].bibtex.item().split(';')) + '} ')
    bibPrint = NoEscape(r'\vspace*{-8mm}\printbibliography[heading=none]')
    dataProf = datProfes[datProfes.Codigo.isin(listProf)]
    print(dataProf)
    proImpar = NoEscape(r"El curso será impartido por:")
    proCurso = NoEscape(r'\vspace*{-4mm}\begin{textoMargen}')
    for consecutivo, profe in dataProf.iterrows():
        match profe.Titulo:
            case "M.Sc." | "Ing." | "Máster" | "Dr.-Ing.":
                proCurso += NoEscape(Command("textbf", f"{profe.Titulo} {profe.Nombre}").dumps())
            case "Ph.D.":
                proCurso += NoEscape(Command("textbf", f"{profe.Nombre}, {profe.Titulo}").dumps())
        proCurso += NoEscape(r" \vspace*{2mm} \newline ")
        for titulo in profe.Titulos.split('\r\n'):
            proCurso += NoEscape(f"{titulo}")
            proCurso += NoEscape(r" \vspace*{1mm} \newline ")   
        proCurso += NoEscape(Command("textbf", "Correo:").dumps())               
        proCurso += NoEscape(f" {profe.Correo}")
        proCurso += NoEscape(Command("textbf", "  Oficina:").dumps())     
        proCurso += NoEscape(f" {int(profe.Oficina)}")
        proCurso += NoEscape(r" \vspace*{1mm} \newline ")
        proCurso += NoEscape(Command("textbf", "Escuela:").dumps())  
        proCurso += NoEscape(f" {profe.Escuela}")
        proCurso += NoEscape(Command("textbf", "  Sede:").dumps())  
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
    doc.preamble.append(Command('addbibresource', '../bibliografia.bib'))
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
    #Left foot # eliminada en nuevo formato
    # with headerfooter.create(Foot("L")) as footer_left:
    #     footer_left.append(TextColor("gris", f"{nomEscue}"))
    #     footer_left.append(NoEscape(r"\par \parbox{0.85\textwidth}{"))
    #     footer_left.append(textcolor
    #         (   
    #         par=False,
    #         size="8",
    #         vspace="0",
    #         color="gris",
    #         bold=False,
    #         text=f"{strProgr}" 
    #         ))
    #     footer_left.append(NoEscape(r"}"))
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
            table.add_row([bold("El curso es requisito de:"), f"{essRequi}"])
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
    doc.append(NewPage())
    with doc.create(Tabularx(table_spec=r"p{3cm}p{13cm}")) as table:
        table.add_row([textcolor
        (   
        size="12",
        vspace="14",
        color="parte",
        bold=True,
        text="4. Contenidos"
        )
        ,"En el curso se desarrollaran los siguientes temas:"])
    doc.append(NewLine())
    doc.append(conCurso)
    doc.append(NewPage())
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
    doc.append(VerticalSpace("4mm", star=True))  
    doc.append(NewLine())
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


generar_programa("IEE0305")
generar_programa("IEE0405")
generar_programa("SCF0801")
# generar_programa("CYD0107",listProf)

subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.aux"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.bbl"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.bcf"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.blg"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.log"], shell=True, check=True)
subprocess.run(["del", f"C:\\Repositories\\CLIE\\programas\\*.run.xml"], shell=True, check=True)