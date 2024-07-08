import json
import requests
import ipaddress

# Desactivar las advertencias de seguridad SSL
requests.packages.urllib3.disable_warnings()

# URL base para las solicitudes RESTCONF
base_url = "https://192.168.56.101/restconf/data"

# Cabeceras para las solicitudes
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Autenticación básica
basicauth = ("cisco", "cisco123!")

def validar_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validar_netmask(netmask):
    try:
        ipaddress.IPv4Network(f"0.0.0.0/{netmask}")
        return True
    except ValueError:
        return False

def mostrar_running_config():
    # URL para obtener el running-config
    running_config_url = f"{base_url}/Cisco-IOS-XE-native:native"

    # Realizar la solicitud GET
    resp = requests.get(running_config_url, auth=basicauth, headers=headers, verify=False)

    # Verificar si la solicitud fue exitosa
    if resp.status_code == 200:
        response_json = resp.json()
        print(json.dumps(response_json, indent=4))
    else:
        print(f"Error: {resp.status_code} - {resp.reason}")
        print(resp.text)

def mostrar_todas_las_interfases():
    # URL para obtener todas las interfaces
    interfaces_url = f"{base_url}/ietf-interfaces:interfaces"

    # Realizar la solicitud GET
    resp = requests.get(interfaces_url, auth=basicauth, headers=headers, verify=False)

    # Verificar si la solicitud fue exitosa
    if resp.status_code == 200:
        response_json = resp.json()
        print(json.dumps(response_json, indent=4))
    else:
        print(f"Error: {resp.status_code} - {resp.reason}")
        print(resp.text)

def agregar_nueva_interfaz():
    # Pedir al usuario que ingrese el nombre de la interfaz y la dirección IP
    nombre_interfaz = input("Ingrese el nombre de la interfaz (e.g., Loopback0): ")
    descripcion = input("Ingrese una descripción para la interfaz: ")
    
    while True:
        ip = input("Ingrese la dirección IP de la interfaz (e.g., 10.2.1.1): ")
        netmask = input("Ingrese la máscara de red (e.g., 255.255.255.0): ")
        
        if not validar_ip(ip):
            print("IP no válida. Por favor ingrese una nueva IP.")
            continue
        
        if not validar_netmask(netmask):
            print("Máscara de red no válida. Por favor ingrese una nueva máscara de red.")
            continue
        
        break

    # URL para agregar la nueva interfaz
    new_interface_url = f"{base_url}/ietf-interfaces:interfaces/interface={nombre_interfaz}"

    # Configuración YANG para la nueva interfaz
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": nombre_interfaz,
            "description": descripcion,
            "type": "iana-if-type:softwareLoopback",  # Solo permitir interfaces de loopback
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": ip,
                        "netmask": netmask
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    # Realizar la solicitud PUT para agregar la nueva interfaz
    resp = requests.put(new_interface_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

    # Verificar si la solicitud fue exitosa
    if resp.status_code in [200, 201, 204]:
        print("Interfaz agregada exitosamente.")
    else:
        print(f"Error: {resp.status_code} - {resp.reason}")
        print(resp.text)

def eliminar_interfaz():
    # Pedir al usuario que ingrese el nombre de la interfaz a eliminar
    nombre_interfaz = input("Ingrese el nombre de la interfaz a eliminar (e.g., Loopback0): ")

    # URL para eliminar la interfaz
    delete_interface_url = f"{base_url}/ietf-interfaces:interfaces/interface={nombre_interfaz}"

    # Realizar la solicitud DELETE para eliminar la interfaz
    resp = requests.delete(delete_interface_url, auth=basicauth, headers=headers, verify=False)

    # Verificar si la solicitud fue exitosa
    if resp.status_code in [200, 204]:
        print("Interfaz eliminada exitosamente.")
    else:
        print(f"Error: {resp.status_code} - {resp.reason}")
        print(resp.text)

def agregar_ruta_estatica():
    # Pedir al usuario que ingrese los detalles de la ruta estática
    while True:
        red_destino = input("Ingrese la red de destino (e.g., 192.168.1.0): ")
        prefijo = input("Ingrese el prefijo (e.g., 24): ")
        next_hop = input("Ingrese la siguiente dirección de salto (e.g., 10.0.0.1): ")
        
        if not validar_ip(red_destino):
            print("Red de destino no válida. Por favor ingrese una nueva red de destino.")
            continue
        
        if not validar_ip(next_hop):
            print("Next hop no válido. Por favor ingrese un nuevo next hop.")
            continue
        
        break

    # URL para agregar la nueva ruta estática
    static_route_url = f"{base_url}/Cisco-IOS-XE-native:native/ip/route/ip-route-interface-forwarding-list={red_destino},{prefijo}"

    # Configuración YANG para la nueva ruta estática
    yangConfig = {
        "Cisco-IOS-XE-native:ip-route-interface-forwarding-list": {
            "prefix": red_destino,
            "mask": prefijo,
            "fwd-list": [
                {
                    "fwd": next_hop
                }
            ]
        }
    }

    # Realizar la solicitud PUT para agregar la nueva ruta estática
    resp = requests.put(static_route_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

    # Verificar si la solicitud fue exitosa
    if resp.status_code in [200, 201, 204]:
        print("Ruta estática agregada exitosamente.")
    else:
        print(f"Error: {resp.status_code} - {resp.reason}")
        print(resp.text)

def menu():
    while True:
        print("\nMenú")
        print("1. Mostrar running-config")
        print("2. Mostrar todas las interfaces")
        print("3. Agregar nueva interfaz (solo Loopback)")
        print("4. Eliminar interfaz")
        print("5. Agregar ruta estática")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            mostrar_running_config()
        elif opcion == '2':
            mostrar_todas_las_interfases()
        elif opcion == '3':
            agregar_nueva_interfaz()
        elif opcion == '4':
            eliminar_interfaz()
        elif opcion == '5':
            agregar_ruta_estatica()
        elif opcion == '6':
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
