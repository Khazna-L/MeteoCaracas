import json
from datos import Municipio, Localidad

def cargar_datos_desde_json(ruta_archivos):
    """Lee el archivo JSON y convierte los datos en una estructura de objetos en memoria."""
    municipios_lista = []

    with open(ruta_archivos, "r", encoding="utf-8") as archivo:
        datos_json = json.load(archivo)

        for mun_data in (datos_json.get("municipios") or []):
            municipios_obj = Municipio(mun_data["nombre"])

            for loc_data in (mun_data.get("localidades") or []):
                localidades_obj = Localidad(
                    nombre=loc_data["nombre"],
                    latitud=loc_data["latitud"],
                    longitud=loc_data["longitud"],
                    municipio_nombre=municipios_obj.nombre
                )
                municipios_obj.agregar_localidades(localidades_obj)

            municipios_lista.append(municipios_obj)

    return municipios_lista

if __name__ == "__main__":
    print("==========================================")
    print("      Sistema Meteocaracas - Fase de Carga")
    print("==========================================\n")

    lista_municipios = cargar_datos_desde_json("areas.json")
    print("Estructura de áreas cargada exitosamente en objetos.\n")

    todas_las_localidades = []
    for mun in lista_municipios:
        todas_las_localidades.extend(mun.localidades)

    print("=== Reporte inicial de localidades ===")
    print("--------------------------------------")
    for loc in todas_las_localidades:
        print(loc)
    print("--------------------------------------\n")

    print("=== Consultando clima en tiempo real para zonas disponibles ===")
    for loc in todas_las_localidades:
        if loc.tiene_coordenadas():
            print(f"\nConsultando API para {loc.nombre}...")
            if loc.consultar_clima():
                print(f"¡Éxito! -> {loc}")