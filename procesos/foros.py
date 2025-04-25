import pandas as pd

cursos = pd.read_csv("cursos/cursos_malla.csv") 

foro1 = cursos[ (cursos["area"] == "IMM") |\
                (cursos["area"] == "ADD") |\
                (cursos["id"] == "CYD0107") |\
                (cursos["id"] == "CYD0607") \
                ].reset_index(drop=True)

print(foro1.creditos.sum())
print(foro1.shape[0])

for name in foro1.nombre:
    print(name)

foro2 = cursos[ (cursos["area"] == "IEE") |\
                (cursos["area"] == "AUT") |\
                (cursos["id"] == "FPH0108") |\
                (cursos["id"] == "FPH0701") \
                ].reset_index(drop=True)

print(foro2.creditos.sum())
print(foro2.shape[0])


foro3 = cursos[ (cursos["area"] == "INS") &\
                (cursos["id"] != "INS1001") &\
                (cursos["id"] != "INS1002") &\
                (cursos["id"] != "INS0905") &\
                (cursos["id"] != "INS1005") &\
                (cursos["semestre"] <= 10) |\
                (cursos["id"] == "INS1201") |\
                (cursos["id"] == "INS1202") |\
                (cursos["id"] == "INS1203") \
                ].reset_index(drop=True)

print(foro3)


for name in foro3.nombre:
    print(name)

print(foro3.creditos.sum())
print(foro3.shape[0])