import json
from datos import Municipio, Localidad

def cargar_datos_desde_json(ruta_archivos):
    ''' Lee el archivo JSON y convierte los datos en una estructura de objetos en memoria. ''' 
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

def observar_reportes_cargados(lista_municipios):
    '''Presenta el resumen de datos'''
    print(" ")
    print("===================================================")
    print(" Informe principal de datos municipales ")
    print("===================================================")

    for mun in lista_municipios:
        total = len(mun.localidades)
        con_coords =  0
        for loc in mun.localidades:
            if loc.tiene_coordenadas():
                con_coords = con_coords + 1

        sin_coords = total - con_coords
        if total > 0:
            porcentaje = (con_coords / total)*100
        else:
            porcentaje = 0.0

        print(" ")
        print(f"Municipio: {mun.nombre}")
        print(f" --Total de localidades: {total}")
        print(f" --Con coordenadas validas: {con_coords}")
        print(f" --Sin coordenadas(null): {sin_coords}")
        print(f" --Área de cobertura: {porcentaje:.2f}%")

    print(" ")
    print(" ")

def menu_principal():
    ''' Despliega las opciones del equipo en la pantalla de comandos. ''' 
    print("====================================================")
    print("  Sistema MeteoCaracas - Menú principal")
    print("====================================================")
    print("1. Consultar clima por Municipio o Localidad.")
    print("2. Buscar clima por nombre directo.")
    print("3. Módulo de estadísticas y reportes.")
    print("4. Consulta histórica de datos.")
    print("0. Salir del sistema.")
    print("")

def ejecutar_navegacion(lista_municipios):
    ''' Facilita la consulta del clima por municipio y localidad. '''
    if len(lista_municipios) == 0:
            print("\n No hay municipios cargados en el sistema.")
            return 

    print("=========================")
    print(" Navegación de municipios ")
    print("=========================")

    indice_num = 1
    for mun in lista_municipios:
        print(f"{indice_num}. {mun.nombre}")
        indice_num = indice_num + 1
    print("0. Regresar al menú prinicipal")

    opcion_mun = input("\n Seleccione un municipio: ").strip()

    if opcion_mun == "0":
        return

    if not opcion_mun.isdigit() or not (1 <= int(opcion_mun) <= len(lista_municipios)):
        print("\n Selección invalida. Ingrese un número dentro del rango.")
        return 

    municipio_sel = lista_municipios[int(opcion_mun) - 1]

    print(f"\n ---- Localidades en {municipio_sel.nombre} ----")

    localidades_validas =[]
    for loc in municipio_sel.localidades:
        if loc.tiene_coordenadas():
            localidades_validas.append(loc)

    if len(localidades_validas) == 0:
        print(f"No hay localidades con estas coordenadas registradas para {municipio_sel.nombre}.")
        return 
    indice_loc = 1
    for loc in localidades_validas:
        print(f"{indice_loc} . {loc.nombre}")
        indice_loc = indice_loc + 1
    print("O. Regresar")

    opcion_loc = input("\n Seleccione una localidad:").strip()
    
    if opcion_loc == "0":
        return

    if not opcion_loc.isdigit() or not (1 <= int(opcion_loc) <= len(localidades_validas)):
        print("\n Selección inválida. Ingrese un número dentro del rango.")
        return 

    localidad_sel = localidades_validas[int(opcion_loc) - 1]

    print(f"\n Consultando información meteorológica para '{localidad_sel.nombre}'.....")

    if localidad_sel.consultar_clima(): 
        print("\n ------------------------------------------")
        print("====Reporte del clima en tiempo real====")
        print(localidad_sel)
        print("---------------------------------------------")
    else:
        print("\n Error al conectar con Open-Meteo. Verificar su conexión.")

def buscar_localidad(lista_municipios):
    ''' Encuentra una localidad por su nombre o por búsqueda aproximada. '''
    termino = input("\n ¿Qué localidad o zona deseas consultar?: ").strip().lower()

    if not termino:
        print("\n Debe ingresar un texto válido para realizar la búsqueda.")
        return 

    coincidencias = []
    for mun in lista_municipios:
        for loc in mun.localidades:
            if termino in loc.nombre.lower():
                coincidencias.append(loc)

    if len(coincidencias) == 0:
        print(f"\n No se encontraron localidades que coincidan con '{termino}' ")
        return 

    if len(coincidencias) == 1:
        localidad_sel = coincidencias[0]
    else:
        print(f"\n Se encontraron {len(coincidencias)} coincidencias: ")
        indice = 1
        for loc in coincidencias:
            print(f"{indice}. {loc.nombre} ({loc.municipio_nombre})")
            indice = indice + 1
        print("0. Cancelar")

        opcion = input("\n Seleccione el número de la localidad que desea consultar: ")

        if opcion == "0" or not opcion.isdigit():
            return 
        
        indice_sel = int(opcion) - 1
        if indice_sel >= 0 and indice_sel < len(coincidencias):
            localidad_sel = coincidencias[indice_sel]
        else:
            print("\n Selección inválida...Operación cancelada.")
            return

    if not localidad_sel.tiene_coordenadas():
        print(f"\n La localidad '{localidad_sel.nombre}' no tiene coordenadas registradas en el sistema.")
        return 
 
    print(f"\n Consultando información para '{localidad_sel.nombre}'.....")
    if localidad_sel.consultar_clima():
        print("\n ------------------------------------------")
        print("==== Reporte del clima en tiempo real ====")
        print(localidad_sel)
        print("---------------------------------------------")
    else:
        print("\n Error al conectar con Open-Meteo. Verificar su conexión.")

def estadisticas(lista_municipios):
    ''' Muestra reportes seguros y ranking de temperatura de las localidades consultadas. '''
    print("\n ------------------------------------------")
    print(" Módulo de estadísticas y ranking ")
    print("---------------------------------------------")

    todas_las_localidades = []
    for mun in lista_municipios:
        for loc in mun.localidades:
            todas_las_localidades.append(loc)

    print("\n 1.Localidades sin coordenadas registradas: ")
    sin_coordenadas = []
    for loc in todas_las_localidades:
        if not loc.tiene_coordenadas(): 
            sin_coordenadas.append(loc)

    if len(sin_coordenadas) > 0:
        for loc in sin_coordenadas:
            print(f" - {loc.nombre} ({loc.municipio_nombre})")
    else:
        print("¡Todas las localidades tienen sus coordenadas registradas!.")

    localidades_consultadas = []
    for loc in todas_las_localidades:
        if loc.clima is not None: 
            localidades_consultadas.append(loc)

    print("\n 2.Ranking de temperatura (Mayor a Menor): ")
    if len(localidades_consultadas) == 0:
        print(" No se ha consultado el clima de ninguna localidad. ")
        print(" Consulta algunas localidades en la Opción 1 o 2 por favor para generar las estadísticas.")
    else:
        localidades_ordenadas = sorted(
            localidades_consultadas,
            key = lambda loc: loc.clima.temperatura,
            reverse= True 
        )

        posicion = 1 
        for loc in localidades_ordenadas:
            temp = loc.clima.temperatura
            hum = loc.clima.humedad
            viento = loc.clima.viento
            print(f" {posicion}. {loc.nombre}: {temp}°C (Humedad: {hum} %, Viento: {viento} km/h)")
            posicion += 1

    print("\n 3. Reporte estadístico: ")
    suma_temperaturas = 0
    for loc in localidades_consultadas:
        suma_temperaturas = suma_temperaturas + loc.clima.temperatura

    promedio_temp = suma_temperaturas / len(localidades_consultadas)

    mas_caluroso = localidades_ordenadas[0]
    mas_frio = localidades_ordenadas[len(localidades_ordenadas) - 1]

    print(f" --Temperatura ambiental promedio: {round(promedio_temp,2)}°C ")
    print(f" --Zona más calurosa: {mas_caluroso.nombre} ({mas_caluroso.clima.temperatura}°C)")
    print(f" --Zona más fría: {mas_frio.nombre} ({mas_frio.clima.temperatura}°C)")




if __name__ == "__main__":
    lista_municipios = cargar_datos_desde_json("zonas_caracas.json")

    observar_reportes_cargados(lista_municipios)

    print(" ")
    print("Sistema MeteoCaracas iniciado con éxito")
    print(" ")

    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ejecutar_navegacion(lista_municipios)
        elif opcion == "2":
            buscar_localidad(lista_municipios)
        elif opcion == "3":
            estadisticas(lista_municipios)
        elif opcion == "4":
            print("\n [Ruta 4: Unidad histórico - En construcción....]")
        elif opcion == "0":
            print("\n ¡Gracias por consultar MeteoCaracas! Nos vemos en el próximo reporte.")
            break
        else:
            print("\n Opción no válida. Por favor, introduzca un número del 0 al 4.")
 