import pandas as pd

profes = pd.read_csv("./profes_datos.csv")


profes.insert(4,"Telefono", profes["Oficina"]*0)

print(profes)

#profes.to_csv("profes_datos.csv",index=False)
