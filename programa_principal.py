import json 

class Ciudad:
    def __init__(self, nombre, latitud, longitud): 
        self.nombre = nombre 
        self.latitud = latitud 
        self.longitud = longitud 
        
    def __str__(self):
        return f"{self.nombre}({self.latitud},{self.longitud})"

with open("areas.json", "r") as archivo:
    datos = json.load(archivo)
    print("Estructuras de las áreas, cargadas con éxito")

ciudades = []
for c in datos["ciudades"]:
    ciudad_obj = Ciudad(c["nombre"], c["latitud"], c["longitud"])
    ciudades.append(ciudad_obj)
    print(f"Área registrada: {ciudad_obj}")

print(f"\nTotal de ciudades cargadas: {len(ciudades)}")
