import pandas as pd
import csv

df = pd.read_csv("resumen_programa_servicio.csv")

df.to_csv("resumen_programa_servicio.csv", index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')