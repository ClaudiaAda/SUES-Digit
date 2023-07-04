import csv

ruta = "csv_vacio.csv"  #es un ruta relativa


archivo_abierto = open (ruta, "w")  
writer = csv.writer(archivo_abierto, delimiter=",")
archivo_abierto.close()