import json
from datos import Municipio, Localidad

def cargar_datos_desde_json(ruta_archivos):
    ' Lee el archivo JSON y convierte los datos en una estructura de objetos en memoria. ' 
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
                municipios_obj.agregar_localidad(localidades_obj)

            municipios_lista.append(municipios_obj)

    return municipios_lista

def menu_principal():
    ' Despliega las opciones del equipo en la pantalla de comandos. ' 
    print("\n" + "="*45)
    print("    Sistema MeteoCaracas - Menú principal")
    print("="*45)
    print("1. Consultar clima por Municipio o Localidad.")
    print("2. Buscar clima por nombre directo.")
    print("3. Módulo de estadísticas y reportes.")
    print("4. Consulta histórica de datos.")
    print("0. Salir del sistema.")
    print("="*45)

def ejecutar_navegacion(lista_municipios):
    ' Facilita la consulta del clima por municipio y localidad. '
    if not lista_municipios:
            print("\n no hay municipios cargados en el sistema.")
            return

    print("\n" + "="*45)
    print(" Navegación de municipios ")
    print("="*45)

    for idx, mun in enumerate(lista_municipios, start=1):
        print(f"{idx}. {mun.nombre}")
    print("0. Regresar al menú prinicipal")

    opcion_mun = input("\n Seleccione un municipio: ").strip()

    if opcion_mun == "0":
        return

    if not opcion_mun.isdigit() or not (1 <= int(opcion_mun) <= len(lista_municipios)):
        print("\n Selección invalida. Ingrese un número dentro del rango.")
        return 

    municipio_sel = lista_municipios[int(opcion_mun) - 1]

    print(f"\n ---- Localidades en {municipio_sel.nombre} ----")
    if not municipio_sel.localidades:
        print("No hay localidades registradas para este municipio.")
        return 

    for idx, loc in enumerate(municipio_sel.localidades, start=1):
        print(f"{idx}. {loc.nombre}")
    print("0. Regresar")

    opcion_loc = input("\n Seleccione una localidad: ").strip()

    if opcion_loc == "0":
        return 

    if not opcion_loc.isdigit() or not (1 <= int(opcion_loc) <= len(municipio_sel.localidades)):
        print("\n Selección inválida. Ingrese un número dentro del rango.")
        return 

    localidad_sel = municipio_sel.localidades[int(opcion_loc) - 1]

    print(f"\n Consultando información meteorológica para '{localidad_sel.nombre}'.....")

    if not localidad_sel.tiene_coordenadas():
        print(f"\n La localidad '{localidad_sel.nombre}' no tiene coordenadas registradas en el sistema.")
        return 

    if localidad_sel.consultar_clima(): 
        print("\n" + "-"*45)
        print("====Reporte del clima en tiempo real====")
        print(localidad_sel)
        print("-"*45)
    else:
        print("\n Error al conectar con Open-Meteo. Verificar su conexion.")

def buscar_localidad(lista_municipios):
    ' Encuentra una localidad por su nombre o por búsqueda aproximada. ' 
    termino = input("\n ¿Qué localidad o zona deseas consultar?: ").strip().lower()

    if not termino: 
        print("\n Debe ingresar un texto válido para realizar la búsqueda.")
        return 

    coincidencias = []
    for mun in lista_municipios:
        for loc in mun.localidades:
            if termino in loc.nombre.lower():
                coincidencias.append(loc)

    if not coincidencias:
        print(f"\n No se encontraron localidades que coincidan con '{termino}' ")
        return 

    if len(coincidencias) == 1:
        localidad_sel = coincidencias[0]
    else:
        print(f"\n Se encontraron {len(coincidencias)} coincidencias: ")
        for idx, loc in enumerate(coincidencias, start= 1):
            print(f"{idx}. {loc.nombre} ({loc.municipio_nombre})")
        print("0. Cancelar")

        opcion = input("\n Seleccione el número de la localidad que desea consultar: ")

        if opcion == "0": 
            return 

        if not opcion.isdigit() or not (1 <= int(opcion) <= len(coincidencias)):
            print("\n Selección inválida...Operación cancelada.")
            return 

        localidad_sel = coincidencias[int(opcion) - 1]

    print(f"\n Consultando información para '{localidad_sel.nombre}'.....")

    if not localidad_sel.tiene_coordenadas():
        print(f"\n La localidad '{localidad_sel.nombre}' no tiene coordenadas registradas en el sistema.")
        return 

    if localidad_sel.consultar_clima():
        print("\n" + "-"*45)
        print("==== Reporte del clima en tiempo real ====")
        print(localidad_sel)
        print("-"*45)
    else:
        print("\n Error al conectar con Open-Meteo. Verificar su conexión.")

def estadisticas(lista_municipios):
    print("\n" + "="*45)
    print(" Módulo de estadísticas y ranking ")
    print("="*45)

    todas_las_localidades = []
    for mun in lista_municipios:
        for loc in mun.localidades:
            todas_las_localidades.append(loc)

    print("\n 1.Localidades sin coordenadas registradas: ")
    sin_coordenadas = []
    for loc in todas_las_localidades:
        if loc in todas_las_localidades():
            sin_coordenadas.append(loc)

    if len(sin_coordenadas) > 0:
        for loc in sin_coordenadas:
            print(f" - {loc.nombre} ({loc.municipio_nombre})")
    else:
        print("¡Todas las localidades tienen sus coordenadas registradas!.")

    









if __name__ == "__main__":
    lista_municipios = cargar_datos_desde_json("areas.json")
    print("Sistema MeteoCaracas iniciado con éxito")

    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ejecutar_navegacion(lista_municipios)
        elif opcion == "2":
            buscar_localidad(lista_municipios)
        elif opcion == "3":
            print("\n [Ruta: Unidad de estadística - En construcción....]")
        elif opcion == "4":
            print("\n [Ruta 4: Unidad histórico - En construcción....]")
        elif opcion == "0":
            print("\n ¡Gracias por consultar MeteoCaracas! Nos vemos en el próximo reporte.")
            break
        else:
            print("\n Opción no válida. Por favor, introduzca un número del 0 al 4.")
 