import json 
import request

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
      self.clima = 

    def __str__(self):
        if self.clima:
              return f"{self.nombre} - {self.clima}"
        else:
              return f"{slef.nombre} - Clima no disponible"
def consultar_clima(self):
        print(f"Consultando el clima de {self.nombre}...")
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitud}&longitude={self.longitud}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        
        try:
            respuesta = requests.get(url, timeout=10)
            respuesta.raise_for_status() 
            
            datos = respuesta.json()

            # Verificamos que la clave "current" exista en la respuesta de la API
            if "current" in datos:
                temp = datos["current"]["temperature_2m"]
                hum = datos["current"]["relative_humidity_2m"]
                viento = datos["current"]["wind_speed_10m"]
                codigo = datos["current"]["weather_code"]

                self.clima = RegistroClimatico(temp, hum, viento, codigo)
            else:
                print(f"Los datos recibidos para {self.nombre} no tienen el formato esperado.")

        except requests.exceptions.RequestException as e:
            print(f"Error de red al consultar el clima: {e}")
        except KeyError as e:
            print(f"Falta un dato específico en la respuesta del clima: {e}")
        except Exception:
            print("No se pudo consultar el clima por un error inesperado.")
