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

def generar_programa(id,listProf):
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
        ubiPlane += "Curso de " + roman.toRoman(int(semestre)) + " semestre en " + programa
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
            susRequi += cursos[cursos.id == requisito].codigo.item()
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
            corRequi += cursos[cursos.id == correquisito].codigo.item()
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
            essRequi += cursos[cursos.id == esrequisito].codigo.item()
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
    aprCurso = roman.toRoman(int(aprCurso[0])) + " semestre de " + aprCurso[1]
    print(f'Aprobación del programa: {aprCurso}\n\n')
    desGener = descri[descri.id == id].descripcion.item().replace("\n", "\n\n")
    lisObjet = objeti[objeti.id == id].reset_index(drop=True).objetivo
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
    conCurso = NoEscape(
r'''

''')
    conCurso += NoEscape(r"\setlength{\leftskip}{4cm}\begin{easylist}\ListProperties(Progressive*=3ex)")
    conCurso += NoEscape(conten[conten.id == id].contenidos.item())
    conCurso += NoEscape(r"\end{easylist}\setlength{\leftskip}{0pt}")
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
    metCurso += NoEscape(Command("textbf", "El curso contempla:").dumps())
    metCurso += objEspec

    #+ "La persona estudiante será capaz de:" + r'\\' + '\n'   

    # coaCurso = cursos[cursos.id == id].area.item()
    # noaCurso = areas[areas.codArea == coaCurso].nombre.item()

    
    # evaCurso = evalua[evalua.id == id].evaluacion.str.split('\n',expand=False).explode()
    # evaCurso = evaCurso.str.split(';',expand=True)
    # evaCurso.reset_index(inplace = True, drop = True)
    # evaCurso.columns = ['2','3','4']
    # evaCurso[['0','1','5']] = ""
    # evaCurso.sort_index(axis=1, inplace=True)
    # bibCurso = NoEscape('\n'+ r'\nocite{' + ('}\n'+r'\nocite{').join(bibtex[bibtex.id == id].bibtex.item().split(';')) + '}\n' + r'\printbibliography[heading=none]')
    # filProfe = datProfes[datProfes.Codigo.isin(listProf)]
    # proCurso = r"" 
    # for index, row in filProfe.iterrows():
    #     titulo = row['Titulo']
    #     match titulo:
    #         case "M.Sc." | "Ing." | "Máster":
    #             proCurso += \
    #             row['Titulo'] + " "\
    #             + row['Nombre']
    #         case "Ph.D.":
    #             proCurso += \
    #             row['Nombre'] + " "\
    #             + row['Titulo']
    #     proCurso += r'\\' + '\n'
    #     for i in range(len(row['Titulos'].split('\r\n'))):
    #         proCurso += row['Titulos'].split('\r\n')[i] + r'\\' + '\n'
    #     proCurso += \
    #     'Correo: ' + row['Correo']\
    #     + '. Oficina: ' + str(row['Oficina']) + r'\\' + '\n'\
    #     + 'Escuela de ' + row['Escuela']\
    #     + '. ' + row['Sede'] + r'\\[12pt]' + '\n'                    
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
    #Package options
    doc.preamble.append(Command('setmainfont','Arial'))
    doc.preamble.append(Command('addbibresource', '../bibliografia.bib'))
    doc.preamble.append(NoEscape(r'\renewcommand*{\bibfont}{\fontsize{12}{16}\selectfont}'))
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
    #Left foot
    with headerfooter.create(Foot("L")) as footer_left:
        footer_left.append(TextColor("azulsuaveTEC", f"{nomEscue}"))
        footer_left.append(NoEscape(r"\par \parbox{0.85\textwidth}{"))
        footer_left.append(textcolor
            (   
            par=False,
            size="8",
            vspace="0",
            color="azulsuaveTEC",
            bold=False,
            text=f"{strProgr}" 
            ))
        footer_left.append(NoEscape(r"}"))
    #Right foot
    with headerfooter.create(Foot("R")) as footer_right:
        footer_right.append(TextColor("azulsuaveTEC", NoEscape(r"Página \thepage \hspace{1pt} de \pageref*{LastPage}")))        
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
            text=f"Programa del curso {codCurso}" 
            ))
    doc.append(textcolor
            (
            size="18",
            vspace="25",
            color="azulsuaveTEC",
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
            table.add_row([bold("Código:"), f"{codCurso}"])
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
    doc.append(NewLine())

    # # doc.append(VarCol("5 Metodología de enseñanza y aprendizaje",metCurso))
    # with doc.create(Tabularx(table_spec=r">{\raggedright}m{0.18\textwidth}m{0.07\textwidth}m{0.17\textwidth}m{0.17\textwidth}m{0.17\textwidth}m{0.04\textwidth}")) as table:
    #         #table.add_hline(start=3, end=5)
    #         table.add_row([
    #             textcolor
    #             (
    #             size="12",
    #             vspace="0",
    #             color="parte",
    #             bold=True,
    #             text="6 Evaluación"
    #             ),
    #             '',
    #             textcolor
    #             (
    #             size="12",
    #             vspace="16",
    #             color="black",
    #             bold=True,
    #             text="Tipo"
    #             ),
    #             textcolor
    #             (
    #             size="12",
    #             vspace="16",
    #             color="black",
    #             bold=True,
    #             text="Cantidad"
    #             ),
    #             textcolor
    #             (
    #             size="12",
    #             vspace="16",
    #             color="black",
    #             bold=True,
    #             text="Porcentaje" 
    #             ),
    #             ''
    #         ])
    #         table.append(NoEscape('[12pt]'))
    #         for row in evaCurso.itertuples(index=False):
    #             #table.add_hline(start=3, end=5)
    #             table.add_row(row)
    #             table.append(NoEscape('[12pt]'))
    # # with doc.create(LongTabularx(table_spec=r">{\raggedright}p{0.18\textwidth}p{0.72\textwidth}",row_height=1.5)) as table:
    # #         table.add_row([
    # #             textcolor
    # #             (
    # #             size="12",
    # #             vspace="0",
    # #             color="parte",
    # #             bold=True,
    # #             text="7 Bibliografía"
    # #             ),NoEscape(bibCurso)
    # #         ])
    # doc.append(VarCol("7 Bibliografía",bibCurso))
    # doc.append(VerticalSpace("10mm", star=True))
    # doc.append(textcolor
    #     (   
    #     hspace="4mm",
    #     size="12",
    #     vspace="20",
    #     color="parte",
    #     bold=True,
    #     text="1 Profesor"
    #     ))
    # doc.append(NewLine())
    # doc.append(proCurso)
    #doc.append(VarCol("8 Profesor",proCurso))
    doc.generate_pdf(f"./programas/{codCurso}", clean=False, clean_tex=False, compiler='lualatex')
    subprocess.run(["biber", f"C:\\Repositories\\CLIE\\programas\\{codCurso}"])
    doc.generate_pdf(f"./programas/{codCurso}", clean=True, clean_tex=False, compiler='lualatex')
    doc.generate_pdf(f"./programas/{codCurso}", clean=True, clean_tex=False, compiler='lualatex') 

# for id in cursos.id:
#      generar_programa(id)

listProf = ['JRH0','JMJ0']
generar_programa("SCF0801",listProf)
#generar_programa("CYD0107",listProf)