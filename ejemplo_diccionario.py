
colores = {
    "solar" : "orange",
    "water" : "blue",
    "wind" : "green",
    "fuels" : "purple"
}

labels = ("solar", "wind")

colores_disponibles = list(map(colores.get, labels))
print(colores_disponibles)
