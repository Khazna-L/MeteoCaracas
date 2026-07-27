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
    print("   Sistema Meteocaracas - Fase de Carga"   )
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

def menu_principal():
    """ Despliega las opciones del equipo en la pantalla de comandos."""
    print("\n" + "="*45)
    print(" Sistema MeteoCaracas - Menú principal")
    print("="*45)
    print("1. Consultar clima de tu municipio")
    print("2. Buscar el tiempo por localidad")
    print("3. Ver regristo por nombre directo")
    print("4. Consulta historica de datos")
    print("0. Salir del sistema")
    print("="*45)

if __name__ == "__main__":
    lista_municipios = cargar_datos_desde_json("areas.json")
    print("Sistema MeteoCaracas iniciado con éxito")

    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n [Ruta 1: Navegación - En construcción....]")
        elif opcion == "2":
            print("\n [Ruta 2: Búsqueda directa - En construcción....]")
        elif opcion == "3":
            print("\n [Ruta: Unidad de estadística - En construcción....]")
        elif opcion == "4":
            print("\n [Ruta 4: Unidad histórico - En construcción....]")
        elif opcion == "0":
            print("\n ¡Gracias por consultar MeteoCaracas! Nos vemos en el próximo reporte.")
            break
        else:
            print("\n Opción no válida. Por favor, introduzca un número del 0 al 4.")


            




