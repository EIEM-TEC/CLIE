import pandas as pd
import funciones as fun


saberes = pd.read_csv("saberes.csv")

categorias = saberes[['categoria','porcBachi']].groupby("categoria",as_index=False).sum()

cat_list = categorias['categoria'].to_list()

# Lista de categorías y valores
cat = categorias['categoria'].to_list()
val = categorias['porcBachi'].to_list()

fun.radar_clie(cat,val,'Bachi')

print(saberes[saberes['categoria']==cat_list[1]])

for categoria in cat_list:
    print(categoria)
    sab = saberes[saberes['categoria']==categoria]
    porc = categorias[categorias['categoria']==categoria]
    porc = porc['porcBachi'].item()
    cat = sab['nombre'].to_list()
    val = sab['porcBachi'].to_list()
    val = [(x / porc)*100 for x in val]
    fun.radar_clie(cat,val,categoria)
