import requests
import pandas as pd 

class RegistroClimatico:
    ''' Refleja los datos del clima al instante sobre una zona. '''
    def __init__(self, temperatura, humedad, viento, codigo_wmo):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.codigo_wmo = codigo_wmo

    def obtener_descripcion_wmo(self):
        ''' Transforma el código del clima de Open-Meteo a una descripción textual al español. '''
        codigos = {
        0: "Cielo despegado",
        1: "Principalmente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla", 
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        61: "Lluvia débil",
        65: "Lluvia fuerte",
        95: "Tormenta eléctrica ligera o moderada"
    }
        return codigos.get(self.codigo_wmo, f"Estado desconocido ({self.codigo_wmo})")

    def __str__(self):
        estado = self.obtener_descripcion_wmo()
        return f"Temp: {self.temperatura}°C, Humedad: {self.humedad}%, Viento: {self.viento} km/h, Estado: {estado}"

class Localidad:
    ''' Muestra una localidad que forma parte de un municipio. '''
    def __init__(self, nombre, latitud, longitud, municipio_nombre=""):
        self.nombre = nombre 
        self.latitud = latitud 
        self.longitud = longitud
        self.clima = None
        self.municipio_nombre = municipio_nombre

    def tiene_coordenadas(self): 
        ''' Retorna verdadero si las coordenadas geográfricas son válidas. '''
        return self.latitud is not None and self.longitud is not None 

    def consultar_clima(self):
        ''' Hace la pregunta a la API de Open-Meteo para obtener el clima actual. '''
        if not self.tiene_coordenadas():
            return False
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitud}&longitude={self.longitud}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code" 
        try:
            respuesta = requests.get(url, timeout=5)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                if "current" in datos:
                    actual = datos["current"]
                    self.clima = RegistroClimatico (
                        temperatura= actual.get("temperature_2m"),
                        humedad= actual.get("relative_humidity_2m"),
                        viento= actual.get("wind_speed_10m"),
                        codigo_wmo= actual.get("weather_code")
                    )
                    return True 
                return False 
        except requests.exceptions.RequestException:
            print (f"¡Error de conexión al consultar! {self.nombre}:") 
            return False 
        
    def __str__(self):
        if self.clima:
            return f"{self.nombre} ({self.municipio_nombre}) - Lat: {self.latitud}, Lon: {self.longitud} | {self.clima}"

        coords = f"Lat: {self.latitud}, Lon: {self.longitud}" if self.tiene_coordenadas() else "Sin coordenadas"
        return f"{self.nombre} ({self.municipio_nombre})- {coords}"
    
    def consultar_historico(self, fecha_inicio, fecha_fin):
        ''' Consulta datos historicos de Open-Meteo y retorna un DataFrame.'''
        if not self.tiene_coordenadas():
            return None
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": self.latitud,
            "longitude": self.longitud,
            "start_date": fecha_inicio,
            "end_date": fecha_fin,
            "daily": "temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max",
            "timezone": "auto"
        }
        try:
            respuesta = requests.get(url, params=params, timeout=10)
            if respuesta.status_code == 200:
                datos = respuesta.json()["daily"]
                df = pd.DataFrame(datos)
                df['time'] = pd.to.datetime(df['time'])
                return df
        except Exception as e:
            print(f"Error de conexion:{e}")
        return None
class Municipio: 
     ''' Muestra un municipio compuesto por diferentes localidades. '''
     def __init__(self, nombre):
          self.nombre = nombre 
          self.localidades = []

     def agregar_localidad(self, localidad):
         ''' Incorpora una localidad dentro de la lista municipal. '''
         self.localidades.append(localidad)


