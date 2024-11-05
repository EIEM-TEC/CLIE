import roman
import numpy as np
import pandas as pd
from pylatex import Document, Package, Command, PageStyle, Head, Foot, NewPage,\
    TextColor, MiniPage, StandAloneGraphic, simple_page_number,\
    TikZ, TikZScope, TikZNode, TikZOptions, TikZCoordinate, TikZNodeAnchor, TikZPath,\
    UnsafeCommand,\
    VerticalSpace, HorizontalSpace, NewLine,\
    LongTable
from pylatex.base_classes import Environment, Arguments
from pylatex.utils import NoEscape, bold, italic

cursos = pd.read_csv("cursos/cursos_malla.csv",
    dtype = {'id':str,'codigo':str,'nombre':str,'area':str,'semestre':int,'fila':int,'horasTeoria':int,'horasPractica':int,'creditos':int})
areas = pd.read_csv("areas.csv")

TRC = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD"]

# black, blue, brown, cyan, darkgray, gray, green, lightgray, lime, magenta, olive, orange, pink, purple, red, teal, violet, white, yellow.

area_colors = {
    "ADD": "blue!20!white",
    "AER": "brown!20!white",
    "AUT": "cyan!20!white",
    "CIB": "green!20!white",
    "CYD": "magenta!20!white",
    "FPH": "olive!20!white",
    "IEE": "orange!20!white",
    "IMM": "red!20!white",
    "INS": "teal!20!white",
    "SCF": "violet!20!white"
}

def textcolor(size,vspace,color,bold,text,hspace="0"):
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

def colocar_titulo(titulo,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"({round(57/2)},{round(4)})")
    dump += NoEscape(f"pic{{titulo={{{titulo},{color}}}}};")
    return dump

def colocar_curso(codigo,nombre,fila,semestre,sesgo,horasteoria,horaspractica,creditos,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+0.5,2)},{round(-4.2*fila-0.5,2)})")
    dump += NoEscape(f"pic{{curso={{{codigo},{nombre},{round(horasteoria)},{round(horaspractica)},{round(creditos)},{color}}}}};")
    return dump

def colocar_semestre(semestre,sesgo,color,horasteoriasemestre,horaspracticasemestre,creditossemestre):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+0.5,2)},{round(0)})")
    if semestre == 0:
        dump += NoEscape(f"pic{{semestre={{{semestre},{color},{horasteoriasemestre},{horaspracticasemestre},{creditossemestre}}}}};")
    else:
        dump += NoEscape(f"pic{{semestre={{{roman.toRoman(semestre)},{color},{horasteoriasemestre},{horaspracticasemestre},{creditossemestre}}}}};")
    return dump

def colocar_arrowreq(semestre,sesgo,fila,sesgovert,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[-{{Stealth[length=3mm,width=2mm]}},{color},line width=0.5mm,]")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)-3.85,2)},{round(-4.2*fila-sesgovert,2)}) -- ")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)-2.03,2)},{round(-4.2*fila-sesgovert,2)});")
    return dump

def colocar_arrowcoreq(semestre,sesgo,fila,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[-{{Stealth[length=3mm,width=2mm]}},{color},line width=0.5mm,]")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+0.5,2)},{round(-4.2*fila+2.08,2)}) -- ")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+0.5,2)},{round(-4.2*fila+1.11,2)});")
    return dump

def colocar_diaesreq(semestre,sesgo,fila,sesgovert,num,color):#1.35 de largo
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[-{{Turned Square[open,length=4mm,line width=0.25mm,width=4mm]}},{color},line width=0.5mm,]")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+3.02,2)},{round(-4.2*fila-sesgovert,2)}) -- ")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+4.37,2)},{round(-4.2*fila-sesgovert,2)}) ")
    dump += NoEscape(r"node[align=center,text width=4mm,xshift=-4.5mm]{\color{black}\fontsize{10pt}{10pt}\selectfont \textbf{")
    dump += NoEscape(f"{num}")
    dump += NoEscape(r"}};")                 
    return dump

def colocar_diareq(semestre,sesgo,fila,sesgovert,num,color):#1.35 de largo
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[{{Turned Square[open,length=4mm,line width=0.25mm,width=4mm]}}-,{color},line width=0.5mm,]")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)-3.38,2)},{round(-4.2*fila-sesgovert,2)}) ")
    dump += NoEscape(r"node[align=center,text width=4mm,xshift=4.5mm]{\color{black}\fontsize{10pt}{10pt}\selectfont \textbf{")
    dump += NoEscape(f"{num}")
    dump += NoEscape(r"}}")  
    dump += NoEscape(f"-- ({round(6.87*(semestre-sesgo)-2.03,2)},{round(-4.2*fila-sesgovert,2)});")
    return dump

def generar_malla():
    #Geometría
    geometry_options = { 
        "left": "0mm",
        "right": "0mm",
        "top": "1mm",
        "bottom": "0mm",
        "headheight": "1mm",
        "footskip": "1mm"
    }
    #Opciones del documento
    doc = Document(documentclass="article", \
                   fontenc=None, \
                   inputenc=None, \
                   lmodern=False, \
                   textcomp=False, \
                   page_numbers=True, \
                   indent=False, \
                   document_options=["letterpaper","landscape"],
                   geometry_options=geometry_options)
    #Paquetes
    doc.packages.append(Package(name="fontspec", options=None))
    doc.packages.append(Package(name="babel", options=['spanish',"activeacute"]))
    doc.packages.append(Package(name="graphicx"))
    doc.packages.append(Package(name="tikz"))
    doc.packages.append(Package(name="anyfontsize"))
    doc.packages.append(Package(name="xcolor",options="dvipsnames"))
    doc.packages.append(Package(name="colortbl"))
    doc.packages.append(Package(name="array"))
    doc.packages.append(Package(name="float"))
    doc.packages.append(Package(name="longtable"))
    doc.packages.append(Package(name="multirow"))
    doc.packages.append(Package(name="fancyhdr"))
    doc.preamble.append(NoEscape(r'\usetikzlibrary{arrows.meta}'))
    #Bloques
    bloqueTitulo = NoEscape(
    r'''\tikzset{
            pics/titulo/.style args={#1,#2}{
            code={
                \def\ancho{57}
                \def\alto{0.7}
                \draw[fill=#2] (-\ancho/2-2,2*\alto) rectangle (\ancho/2+2,-2*\alto) node[midway,align=center,text width=45cm]{\fontsize{30pt}{0pt}\selectfont \textbf{#1}};
            }
        }
    }'''
    )
    bloqueCurso = NoEscape(
    r'''\tikzset{
            pics/curso/.style args={#1,#2,#3,#4,#5,#6}{
            code={
                \def\ancho{5}
                \def\alto{0.8}
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,-\alto) node[midway,align=center,text width=\ancho cm]{\fontsize{16pt}{2pt}\selectfont {#2}};
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,\alto + \alto) node[midway]{\fontsize{14pt}{14pt}\selectfont #1};
                \draw[fill=#6] (-\ancho/2,-\alto) rectangle (-\ancho/2 + \ancho/3, -\alto - \alto) node[midway]{\fontsize{14pt}{14pt}\selectfont #3};
                \draw[fill=#6] (-\ancho/2 + \ancho/3,-\alto) rectangle (-\ancho/2 + 2*\ancho/3, -\alto - \alto) node[midway]{\fontsize{14pt}{14pt}\selectfont #4};
                \draw[fill=#6] (-\ancho/2 + 2*\ancho/3,-\alto) rectangle (-\ancho/2 + 3*\ancho/3, -\alto - \alto) node[midway]{\fontsize{14pt}{14pt}\selectfont #5};
            }
        }
    }''' 
    #1: codigo, #2: nombre, #3: horasteoria, #4: horaspractica, #5: creditos, #6: color
    )
    bloqueSemestre = NoEscape(
    r'''\tikzset{
            pics/semestre/.style args={#1,#2,#3,#4,#5}{
            code={
                \def\ancho{6}
                \def\alto{0.8}
                \draw[fill=#2] (-\ancho/2,1.5*\alto) rectangle (\ancho/2,-1.5*\alto) node[midway,align=center,text width=\ancho cm]{\fontsize{16pt}{12pt}\selectfont \textbf{#1}};
                \draw[fill=#2] (-\ancho/2,-\alto) rectangle (-\ancho/2 + \ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #3};
                \draw[fill=#2] (-\ancho/2 + \ancho/3,-\alto) rectangle (-\ancho/2 + 2*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #4};
                \draw[fill=#2] (-\ancho/2 + 2*\ancho/3,-\alto) rectangle (-\ancho/2 + 3*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #5};
            }
        }
    }'''
    #1: semestre, #2: color, #3: horasteoria, #4: horaspractica, #5: creditos
    )
    circReq = NoEscape(
    r'''\tikzset{
            pics/requi/.style args={#1,#2}{
            code={
                \def\diam{0.4}
                \draw[fill=#2] circle (\diam) node[midway,align=center,text width=\diam cm]{\fontsize{10pt}{10pt}\selectfont \textbf{#1}};
            }
        }
    }'''
    )

    arrowReq = NoEscape(
    r'''\tikzset{
        pics/arrowreq/.style args={#1}{
            code={
                \def\len{0.4} % Arrow length in mm
                \def\wid{0.2} % Arrow width in mm
                \draw[#1] -{Stealth[length=\len mm, width=\wid mm]};
            }
        }
    }'''
    )

    doc.preamble.append(bloqueTitulo)        
    doc.preamble.append(bloqueCurso)
    doc.preamble.append(bloqueSemestre)
    doc.preamble.append(circReq)
    doc.preamble.append(arrowReq)
    doc.append(Command('centering'))
    sesgo = 0
    reqcounter = 0
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla_TRC:
        malla_TRC.append(colocar_titulo("Bachillerato en Ingeniería Electromecánica y tronco común de Licenciatura en Ingeniería Electromecánica - Plan: 2026","lightgray"))
        cursos_TRC = cursos[cursos["area"].isin(TRC)]
        for semestre in range(0,9):
            horasteoriasemestre = cursos_TRC[cursos_TRC.semestre == semestre].horasTeoria.sum()
            horaspracticasemestre = cursos_TRC[cursos_TRC.semestre == semestre].horasPractica.sum()
            creditossemestre = cursos_TRC[cursos_TRC.semestre == semestre].creditos.sum()
            malla_TRC.append(colocar_semestre(semestre,sesgo,"lightgray",horasteoriasemestre,horaspracticasemestre,creditossemestre))            
        for id in cursos_TRC.id:
            codigo = cursos_TRC[cursos_TRC.id == id].codigo.item()
            nombre = cursos_TRC[cursos_TRC.id == id].nombre.item()
            fila = cursos_TRC[cursos_TRC.id == id].fila.item()
            semestre = cursos_TRC[cursos_TRC.id == id].semestre.item()
            horasteoria = cursos_TRC[cursos_TRC.id == id].horasTeoria.item()
            horaspractica = cursos_TRC[cursos_TRC.id == id].horasPractica.item()
            creditos = cursos_TRC[cursos_TRC.id == id].creditos.item()
            area = cursos_TRC[cursos_TRC.id == id].area.item()           
            color = area_colors.get(area)
            requi = cursos_TRC[cursos_TRC.id == id].requisitos.str.split(';',expand=True)
            corequi = str(cursos_TRC[cursos_TRC.id == id].correquisitos.item())
            esrequi = cursos_TRC[cursos_TRC.id == id].esrequisito.str.split(';',expand=True)         
            malla_TRC.append(colocar_curso(codigo,nombre,fila,semestre,sesgo,horasteoria,horaspractica,creditos,color))
            if not(requi[0].isna().item()):
                for column in requi.columns:
                    idreq = requi[column].item()
                    codreq = cursos_TRC[cursos_TRC.id == idreq].codigo.item()
                    semreq = cursos_TRC[cursos_TRC.id == idreq].semestre.item()
                    filareq = cursos_TRC[cursos_TRC.id == idreq].fila.item()
                    if (filareq == fila) and (semreq == semestre - 1):
                        malla_TRC.append(colocar_arrowreq(semestre,sesgo,fila,-0.7,"black"))
                    else:
                        reqcounter +=1
                        malla_TRC.append(colocar_diareq(semestre,sesgo,fila,0,reqcounter,"black"))
                        malla_TRC.append(colocar_diaesreq(semreq,sesgo,filareq,0.9,reqcounter,"black"))
            if not(corequi == 'nan'):
                semcoreq = cursos_TRC[cursos_TRC.id == corequi].semestre.item()
                filacoreq = cursos_TRC[cursos_TRC.id == corequi].fila.item()
                if (semcoreq == semestre) and (filacoreq == fila - 1):
                    malla_TRC.append(colocar_arrowcoreq(semestre,sesgo,fila,"black"))

            # if not(esrequi[0].isna().item()):
            #     for column in esrequi.columns:
            #         idreq = esrequi[column].item()
            #         reqcounter += 1
            #         # codreq = cursos_TRC[cursos_TRC.id == idreq].codigo.item()
            #         # semreq = cursos_TRC[cursos_TRC.id == idreq].semestre.item()
            #         # filareq = cursos_TRC[cursos_TRC.id == idreq].fila.item()
            #         malla_TRC.append(colocar_esreq(semestre,sesgo,fila,column,reqcounter,color))
    doc.append(NoEscape(r"\newpage"))
    sesgo = 8
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla_INS:
        malla_INS.append(colocar_titulo("Licenciatura en Ingeniería Electromecánica con énfasis en Instalaciones (debe cursar primero tronco común)","lightgray"))
        cursos_INS = cursos[cursos["area"] == "INS"]
        for semestre in range(8,11):
            horasteoriasemestre = cursos_INS[cursos_INS.semestre == semestre].horasTeoria.sum()
            horaspracticasemestre = cursos_INS[cursos_INS.semestre == semestre].horasPractica.sum()
            creditossemestre = cursos_INS[cursos_INS.semestre == semestre].creditos.sum()
            malla_INS.append(colocar_semestre(semestre,sesgo,"lightgray",horasteoriasemestre,horaspracticasemestre,creditossemestre))            
        for id in cursos_INS[cursos_INS["area"] == "INS"].id:
            codigo = cursos_INS[cursos_INS.id == id].codigo.item()
            nombre = cursos_INS[cursos_INS.id == id].nombre.item()
            fila = cursos_INS[cursos_INS.id == id].fila.item()
            semestre = cursos_INS[cursos_INS.id == id].semestre.item()
            horasteoria = cursos_INS[cursos_INS.id == id].horasTeoria.item()
            horaspractica = cursos_INS[cursos_INS.id == id].horasPractica.item()
            creditos = cursos_INS[cursos_INS.id == id].creditos.item()
            area = cursos_INS[cursos_INS.id == id].area.item()           
            color = area_colors.get(area)            
            malla_INS.append(colocar_curso(codigo,nombre,fila,semestre,sesgo,horasteoria,horaspractica,creditos,color))
    doc.append(NoEscape(r"\newpage"))
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla_AER:
        malla_AER.append(colocar_titulo("Licenciatura en Ingeniería Electromecánica con énfasis en Aeronáutica (debe cursar primero tronco común)","lightgray"))
        cursos_AER = cursos[cursos["area"] == "AER"]
        for semestre in range(8,11):
            horasteoriasemestre = cursos_AER[cursos_AER.semestre == semestre].horasTeoria.sum()
            horaspracticasemestre = cursos_AER[cursos_AER.semestre == semestre].horasPractica.sum()
            creditossemestre = cursos_AER[cursos_AER.semestre == semestre].creditos.sum()
            malla_AER.append(colocar_semestre(semestre,sesgo,"lightgray",horasteoriasemestre,horaspracticasemestre,creditossemestre))            
        for id in cursos_AER[cursos_AER["area"] == "AER"].id:
            codigo = cursos_AER[cursos_AER.id == id].codigo.item()
            nombre = cursos_AER[cursos_AER.id == id].nombre.item()
            fila = cursos_AER[cursos_AER.id == id].fila.item()
            semestre = cursos_AER[cursos_AER.id == id].semestre.item()
            horasteoria = cursos_AER[cursos_AER.id == id].horasTeoria.item()
            horaspractica = cursos_AER[cursos_AER.id == id].horasPractica.item()
            creditos = cursos_AER[cursos_AER.id == id].creditos.item()
            area = cursos_AER[cursos_AER.id == id].area.item()           
            color = area_colors.get(area)            
            malla_AER.append(colocar_curso(codigo,nombre,fila,semestre,sesgo,horasteoria,horaspractica,creditos,color))
    doc.append(NoEscape(r"\newpage"))
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla_SCF:
        malla_SCF.append(colocar_titulo("Licenciatura en Ingeniería Electromecánica con énfasis en Sistemas Ciberfísicos (debe cursar primero tronco común)","lightgray"))
        cursos_SCF = cursos[cursos["area"] == "SCF"]
        for semestre in range(8,11):
            horasteoriasemestre = cursos_SCF[cursos_SCF.semestre == semestre].horasTeoria.sum()
            horaspracticasemestre = cursos_SCF[cursos_SCF.semestre == semestre].horasPractica.sum()
            creditossemestre = cursos_SCF[cursos_SCF.semestre == semestre].creditos.sum()
            malla_SCF.append(colocar_semestre(semestre,sesgo,"lightgray",horasteoriasemestre,horaspracticasemestre,creditossemestre))            
        for id in cursos_SCF[cursos_SCF["area"] == "SCF"].id:
            codigo = cursos_SCF[cursos_SCF.id == id].codigo.item()
            nombre = cursos_SCF[cursos_SCF.id == id].nombre.item()
            fila = cursos_SCF[cursos_SCF.id == id].fila.item()
            semestre = cursos_SCF[cursos_SCF.id == id].semestre.item()
            horasteoria = cursos_SCF[cursos_SCF.id == id].horasTeoria.item()
            horaspractica = cursos_SCF[cursos_SCF.id == id].horasPractica.item()
            creditos = cursos_SCF[cursos_SCF.id == id].creditos.item()
            area = cursos_SCF[cursos_SCF.id == id].area.item()           
            color = area_colors.get(area)            
            malla_SCF.append(colocar_curso(codigo,nombre,fila,semestre,sesgo,horasteoria,horaspractica,creditos,color))
    doc.generate_pdf(f"malla_EM", clean=True, clean_tex=False, compiler='lualatex',silent=True)



datos_malla = pd.DataFrame()
datos_malla["cred_TRC"] = cursos.groupby("area")["creditos"].sum(numeric_only=True)
datos_malla.loc[["INS","AER","SCF"],"cred_TRC"] = 0
datos_malla["pt_TRC"] = areas["porcTRC"].to_list()[:-1]
datos_malla["pm_TRC"] = round((datos_malla["cred_TRC"] / datos_malla["cred_TRC"].sum())*100,1)
datos_malla["cred_INS"] = cursos.groupby("area")["creditos"].sum(numeric_only=True)
datos_malla.loc[["AER","SCF"],"cred_INS"] = 0
datos_malla["pt_INS"] = areas["porcINS"].to_list()[:-1]
datos_malla["pm_INS"] = round(((datos_malla["cred_INS"]/180)*100),1)
datos_malla["cred_AER"] = cursos.groupby("area")["creditos"].sum(numeric_only=True)
datos_malla.loc[["INS","SCF"],"cred_AER"] = 0
datos_malla["pt_AER"] = areas["porcAER"].to_list()[:-1]
datos_malla["pm_AER"] = round(((datos_malla["cred_AER"]/180)*100),1)
datos_malla["cred_SCF"] = cursos.groupby("area")["creditos"].sum(numeric_only=True)
datos_malla.loc[["AER","INS"],"cred_SCF"] = 0
datos_malla["pt_SCF"] = areas["porcSCF"].to_list()[:-1]
datos_malla["pm_SCF"] = round(((datos_malla["cred_SCF"]/180)*100),1)
datos_malla.loc["TOT"] = datos_malla.sum(numeric_only=True)
datos_malla.to_csv('datos_malla.csv')
print(datos_malla)

generar_malla()
