import json 
import request
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


class RegistroClimatico:
    def __init__(self, temperatura, humedad, viento, codigo_wmo)
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        Self.codigo_wmo = codigo_wmo

    def __str__(self):
        return f"{self.temperatura}°C, Humedad: {self.humedad}%, Viento: {self.viento} km/h (Código WMO: {self.codigo_wmo})"


class Ciudad:
    def__init__(self, nombre, latitud, longitud):
      self.nombre = nombre
      self.latitud = latitud
      self.longitud = longitud
      self.clima = none


    def __str__(self):
        if self.clima:
            return f"{self.nombre} - {self.clima}"
        else:
            return f"{self.nombre} - Clima no disponible"

    def consultar_clima(self):
        print(f"Consultando el clima de {self.nombre}...")
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitud}&longitude={self.longitud}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        
        try:
            respuesta = requests.get(url, timeout=10)
           
            respuesta.raise_for_status() 
            
            datos = respuesta.json()

                  if "current" in datos:
                temp = datos["current"]["temperature_2m"]
                hum = datos["current"]["relative_humidity_2m"]
                viento = datos["current"]["wind_speed_10m"]
                codigo = datos["current"]["weather_code"]

                self.clima = RegistroClimatico(temp, hum, viento, codigo)
            else:
                print(f"Los datos recibidos para {self.nombre} no tienen el formato esperado.")
