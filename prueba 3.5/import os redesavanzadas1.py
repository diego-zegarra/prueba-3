import os
import ipaddress  # Importar el módulo ipaddress para validar direcciones IP

# Función para limpiar la pantalla de manera compatible con diferentes sistemas operativos
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para mostrar detalles de un dispositivo a través de archivos
def leer_archivo(nombre_archivo):
    try:
        with open(f"{nombre_archivo}.txt", "r") as file:
            contenido = file.read()
            print(f"Contenido de {nombre_archivo}.txt:")
            print(contenido)
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo}.txt no se encuentra.")

# Diccionario para almacenar los dispositivos por sector y sus correspondientes archivos
dispositivos_por_sector = {
    1: {'nombre': "Sucursal Principal", 'dispositivos': [("Router", "routersucursal"), ("Switch Multicapa", "switchmulticapa"), ("Dispositivos Finales", "dispositivofinal")]},
    2: {'nombre': "Backbone", 'dispositivos': [("Router", "routerblackbone"), ("Switch Multicapa", "switchmulticapa"), ("Dispositivos Finales", "dispositivofinal")]},
    3: {'nombre': "BGP 2345", 'dispositivos': [("Router BGP 2345", "routerbgp2345"), ("Switch Multicapa", "switchmulticapa"), ("Dispositivos Finales", "dispositivofinal")]},
    4: {'nombre': "Oficina Remota", 'dispositivos': [("Oficina Remota 1", "oficinaremota1"), ("Oficina Remota 2", "oficinaremota2"), ("Switch Multicapa", "switchmulticapa"), ("Dispositivos Finales", "dispositivofinal")]},
    5: {'nombre': "OSPF Area 123", 'dispositivos': [("OSPF Area 123", "ospfarea123")]}
}

# Función para mostrar dispositivos de un sector
def mostrar_dispositivos(sector):
    if sector in dispositivos_por_sector:
        print("Dispositivos en el sector seleccionado:")
        dispositivos = dispositivos_por_sector[sector]['dispositivos']
        for i, (nombre, archivo) in enumerate(dispositivos, 1):
            print(f"{i} - {nombre}")
        dispositivo_elegido = int(input("Elija un dispositivo para ver más detalles: "))
        if 1 <= dispositivo_elegido <= len(dispositivos):
            leer_archivo(dispositivos[dispositivo_elegido - 1][1])
        else:
            print("Dispositivo no válido.")
    else:
        print("Sector no válido.")

# Función para generar los archivos solicitados
def generar_archivos_txt():
    archivos_contenidos = {
        "internet": "Contenido del archivo internet.txt",
        "oficina remota 5-6": "Contenido del archivo oficina remota 5-6.txt",
        "oficina remota 3-4": "Contenido del archivo oficina remota 3-4.txt"
    }
    for nombre_archivo, contenido in archivos_contenidos.items():
        with open(f"{nombre_archivo}.txt", "w") as file:
            file.write(contenido)
        print(f"Archivo {nombre_archivo}.txt generado con éxito.")

# Función para borrar dispositivos de un sector
def borrar_dispositivo(sector):
    if sector in dispositivos_por_sector:
        print("Dispositivos en el sector seleccionado:")
        dispositivos = dispositivos_por_sector[sector]['dispositivos']
        for i, (nombre, _) in enumerate(dispositivos, 1):
            print(f"{i} - {nombre}")
        dispositivo_elegido = int(input("Elija el número del dispositivo a borrar: "))
        if 1 <= dispositivo_elegido <= len(dispositivos):
            dispositivo_borrado = dispositivos.pop(dispositivo_elegido - 1)[0]
            print(f"Dispositivo '{dispositivo_borrado}' borrado con éxito.")
        else:
            print("Número de dispositivo no válido.")
    else:
        print("Sector no válido.")

# Función para añadir dispositivos a un sector
def añadir_dispositivo(sector):
    if sector in dispositivos_por_sector:
        nuevo_dispositivo = input("Ingrese el nombre del nuevo dispositivo: ")
        nuevo_archivo = input("Ingrese el nombre del archivo asociado (sin .txt): ")
        while True:
            nueva_direccion_ip = input("Ingrese la dirección IP del dispositivo (formato x.x.x.x): ")
            try:
                ipaddress.ip_address(nueva_direccion_ip)
                break  # Si la dirección IP es válida, salir del bucle
            except ValueError:
                print("Dirección IP inválida. Por favor, ingrese una dirección IP válida.")

        while True:
            nueva_mascara = input("Ingrese la máscara de red del dispositivo (formato x.x.x.x): ")
            try:
                ipaddress.ip_network(f"{nueva_direccion_ip}/{nueva_mascara}", strict=False)
                break  # Si la máscara de red es válida, salir del bucle
            except ValueError:
                print("Máscara de red inválida. Por favor, ingrese una máscara de red válida.")

        dispositivos_por_sector[sector]['dispositivos'].append((nuevo_dispositivo, nuevo_archivo, nueva_direccion_ip, nueva_mascara))
        print(f"Dispositivo '{nuevo_dispositivo}' añadido con éxito al sector {sector}.")
    else:
        print("Sector no válido.")

# Función para borrar sectores
def borrar_sector():
    print("Sectores disponibles:")
    for sector, detalles in dispositivos_por_sector.items():
        print(f"{sector} - {detalles['nombre']}")
    sector_elegido = int(input("Elija el número del sector a borrar: "))
    if sector_elegido in dispositivos_por_sector:
        del dispositivos_por_sector[sector_elegido]
        print(f"Sector {sector_elegido} borrado con éxito.")
    else:
        print("Número de sector no válido.")

# Función para añadir sectores
def añadir_sector():
    nuevo_sector = int(input("Ingrese el número del nuevo sector: "))
    if nuevo_sector not in dispositivos_por_sector:
        nombre_sector = input("Ingrese el nombre del nuevo sector: ")
        dispositivos_por_sector[nuevo_sector] = {
            'nombre': nombre_sector,
            'dispositivos': []
        }
        print(f"Sector {nuevo_sector} ('{nombre_sector}') añadido con éxito.")
    else:
        print(f"El sector {nuevo_sector} ya existe.")

# Función para mostrar sectores
def mostrar_sectores():
    print("Sectores disponibles:")
    for sector, detalles in dispositivos_por_sector.items():
        print(f"{sector} - {detalles['nombre']}")

# Generar los archivos solicitados al inicio del programa
generar_archivos_txt()

# Menú principal del programa
while True:
    clear_screen()
    print("Bienvenido, ¿qué desea hacer?")
    print("1 - Ver sectores\n2 - Ver dispositivos\n3 - Borrar dispositivos\n4 - Borrar sectores\n5 - Añadir sectores\n6 - Añadir dispositivos\n7 - Salir")
    opcion = input("Elija una opción: ")

    if opcion == '1':
        mostrar_sectores()
    elif opcion == '2':
        mostrar_sectores()
        sector_elegido = int(input("Elija un sector: "))
        mostrar_dispositivos(sector_elegido)
    elif opcion == '3':
        mostrar_sectores()
        sector_elegido = int(input("Elija un sector: "))
        borrar_dispositivo(sector_elegido)
    elif opcion == '4':
        borrar_sector()
    elif opcion == '5':
        añadir_sector()
    elif opcion == '6':
        mostrar_sectores()
        sector_elegido = int(input("Elija un sector: "))
        añadir_dispositivo(sector_elegido)
    elif opcion == '7':
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida.")

    input("\nPresione Enter para continuar...")
