import os
import roman
import pandas as pd
from pylatex import Document, Package, Command, PageStyle, Head, Foot, NewPage,\
    TextColor, MiniPage, StandAloneGraphic, simple_page_number,\
    TikZ, TikZScope, TikZNode, TikZOptions, TikZCoordinate, TikZNodeAnchor, TikZPath,\
    UnsafeCommand,\
    VerticalSpace, HorizontalSpace, NewLine,\
    LongTable
from pylatex.base_classes import Environment, Arguments
from pylatex.utils import NoEscape, bold, italic

cursos = pd.read_csv("cursos.csv",
    dtype = {'Codigo':str,'Nombre':str,'Area':str,'Semestre':int,'Fila':int,'HorasTeoria':int,'HorasPractica':int,'Creditos':int})
areas = pd.read_csv("areas.csv")

TRC = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD"]

area_colors = {
    "ADD": "Apricot",
    "AER": "Thistle",
    "AUT": "Lavender",
    "CIB": "LimeGreen",
    "CYD": "WildStrawberry",
    "FPH": "Tan",
    "IEE": "YellowOrange",
    "IMM": "Mulberry",
    "INS": "BlueGreen",
    "SCF": "Melon"
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
    dump += NoEscape(f"({round(6.87*(semestre-sesgo),2)+0.5},{round(-4.2*fila,1)-0.5})")
    dump += NoEscape(f"pic{{curso={{{codigo},{nombre},{round(horasteoria)},{round(horaspractica)},{round(creditos)},{color}}}}};")
    return dump

def colocar_semestre(semestre,sesgo,color,horasteoriasemestre,horaspracticasemestre,creditossemestre):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo),2)+0.5},{round(0)})")
    if semestre == 0:
        dump += NoEscape(f"pic{{semestre={{{semestre},{color},{horasteoriasemestre},{horaspracticasemestre},{creditossemestre}}}}};")
    else:
        dump += NoEscape(f"pic{{semestre={{{roman.toRoman(semestre)},{color},{horasteoriasemestre},{horaspracticasemestre},{creditossemestre}}}}};")
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
                \draw[fill=#2] (-\ancho/2,1.5*\alto) rectangle (\ancho/2,-1.5*\alto) node[midway,align=center,text width=6cm]{\fontsize{16pt}{12pt}\selectfont \textbf{#1}};
                \draw[fill=#2] (-\ancho/2,-\alto) rectangle (-\ancho/2 + \ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #3};
                \draw[fill=#2] (-\ancho/2 + \ancho/3,-\alto) rectangle (-\ancho/2 + 2*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #4};
                \draw[fill=#2] (-\ancho/2 + 2*\ancho/3,-\alto) rectangle (-\ancho/2 + 3*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #5};
            }
        }
    }'''
    #1: semestre, #2: color, #3: horasteoria, #4: horaspractica, #5: creditos
    )
    doc.preamble.append(bloqueTitulo)        
    doc.preamble.append(bloqueCurso)
    doc.preamble.append(bloqueSemestre)
    doc.append(Command('centering'))
    sesgo = 0
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
        for codigo in cursos_TRC.codigo:
            nombre = cursos_TRC[cursos_TRC.codigo == codigo].nombre.item()
            fila = cursos_TRC[cursos_TRC.codigo == codigo].fila.item()
            semestre = cursos_TRC[cursos_TRC.codigo == codigo].semestre.item()
            horasteoria = cursos_TRC[cursos_TRC.codigo == codigo].horasTeoria.item()
            horaspractica = cursos_TRC[cursos_TRC.codigo == codigo].horasPractica.item()
            creditos = cursos_TRC[cursos_TRC.codigo == codigo].creditos.item()
            area = cursos_TRC[cursos_TRC.codigo == codigo].area.item()           
            color = area_colors.get(area)            
            malla_TRC.append(colocar_curso(codigo,nombre,fila,semestre,sesgo,horasteoria,horaspractica,creditos,color))
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
        for codigo in cursos_INS[cursos_INS["area"] == "INS"].codigo:
            nombre = cursos_INS[cursos_INS.codigo == codigo].nombre.item()
            fila = cursos_INS[cursos_INS.codigo == codigo].fila.item()
            semestre = cursos_INS[cursos_INS.codigo == codigo].semestre.item()
            horasteoria = cursos_INS[cursos_INS.codigo == codigo].horasTeoria.item()
            horaspractica = cursos_INS[cursos_INS.codigo == codigo].horasPractica.item()
            creditos = cursos_INS[cursos_INS.codigo == codigo].creditos.item()
            area = cursos_INS[cursos_INS.codigo == codigo].area.item()           
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
        for codigo in cursos_AER[cursos_AER["area"] == "AER"].codigo:
            nombre = cursos_AER[cursos_AER.codigo == codigo].nombre.item()
            fila = cursos_AER[cursos_AER.codigo == codigo].fila.item()
            semestre = cursos_AER[cursos_AER.codigo == codigo].semestre.item()
            horasteoria = cursos_AER[cursos_AER.codigo == codigo].horasTeoria.item()
            horaspractica = cursos_AER[cursos_AER.codigo == codigo].horasPractica.item()
            creditos = cursos_AER[cursos_AER.codigo == codigo].creditos.item()
            area = cursos_AER[cursos_AER.codigo == codigo].area.item()           
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
        for codigo in cursos_SCF[cursos_SCF["area"] == "SCF"].codigo:
            nombre = cursos_SCF[cursos_SCF.codigo == codigo].nombre.item()
            fila = cursos_SCF[cursos_SCF.codigo == codigo].fila.item()
            semestre = cursos_SCF[cursos_SCF.codigo == codigo].semestre.item()
            horasteoria = cursos_SCF[cursos_SCF.codigo == codigo].horasTeoria.item()
            horaspractica = cursos_SCF[cursos_SCF.codigo == codigo].horasPractica.item()
            creditos = cursos_SCF[cursos_SCF.codigo == codigo].creditos.item()
            area = cursos_SCF[cursos_SCF.codigo == codigo].area.item()           
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
