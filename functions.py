import psutil
import subprocess
import platform
import socket
import logging



def check_memory():
    mem = psutil.virtual_memory()
    
    result = {
        'total_gb': round(mem.total / (1024**3), 2),
        'usado_gb': round(mem.used / (1024**3), 2),
        'disponible_gb': round(mem.available / (1024**3), 2),
        'porcentaje': mem.percent,
        'estado': 'OK'
    }
    
    if mem.percent >= 90:
        logging.critical(f"RAM crítica: {mem.percent}%")
        result['estado'] = 'CRITICAL'
    elif mem.percent >= 85:
        logging.warning(f"RAM alta: {mem.percent}%")
        result['estado'] = 'WARNING'
    
    return result

def check_cpu():
    cpu = psutil.cpu_percent(interval=1)

    result = {
        'porcentaje': cpu,
        'estado': 'OK'
    }
    if cpu > 80:
        logging.critical(f"CPU crítica: {cpu}%")
        result['estado'] = 'CRITICAL'
    elif cpu > 40:
        logging.warning(f"CPU alta: {cpu}%")
        result['estado'] = 'WARNING'

    return result

def check_disk():
    disk = psutil.disk_usage('/')

    result = {
        'porcentaje': disk.percent,
        'estado': 'OK'
    }

    if disk.percent > 90:
        logging.critical(f"Disco casi lleno: {disk.percent}%")
        result['estado'] = 'CRITICAL'
    elif disk.percent > 70:
        logging.warning(f"Disco bastante lleno: {disk.percent}%")
        result['estado'] = 'WARNING'

    return result

def check_service_status(service):
    system = platform.system()

    if system == 'Linux':
        cmd = ['systemctl', 'is-active', service]
    elif system == 'Windows':
        cmd = ['sc', 'query', service]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    returnCode = result.returncode

    result = result.stdout

    if returnCode == 0:
        result = parse_service_status(result, system)
    else:
        logging.error(f"Servicio '{service}' no encontrado")
        result = 'NOT_FOUND'

    return result

def parse_service_status(text, os_type):
    if os_type == 'Linux':
        text = text.strip()
        return text
    elif os_type == 'Windows':
        lineas = text.split('\n')
        estado = "UNKNOWN"

        
        for linea in lineas:
            if 'ESTADO' in linea:
                estado = linea
                estado = estado.split(':')[1]
                estado = estado.strip().split()[-1]

        return estado
    
def check_services(servicesList):
    servicesDict = {}

    for service in servicesList:
        servicesDict[service] = check_service_status(service)

    return servicesDict

def display_services(servicesDict):
    print("\nServices Status:")
    for service, status in servicesDict.items():
        print(f"Servicio: {service} || Estado: {status}")
    print()

def check_port(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(3)

        connection = s.connect_ex((host, port))

        if connection == 0:
            result = 'OPEN'
        else:
            result = 'CLOSED'
        s.close()

        return result
    except Exception as e:
        logging.error(f"Error verificando puerto {port}: {e}")
        return 'Error'
    
def check_ports(portsList):
    portsDict = {}

    for port in portsList:
        portsDict[port] = check_port('127.0.0.1', port)

    return portsDict

def display_ports(portsDict):
    
    print("\nPort Status:")
    for port, status in portsDict.items():
        print(f"Puerto: {port} || Estado: {status}")
    print()

def menu():
    print('===================== Menú de opciones ===================')
    print(f"a) Comprobar servicios")
    print(f"b) Comprobar puertos")
    print(f"q) Salir")
    print()
    opcion = input("Selecciona la opción que desees: ").lower()
    return opcion

def show_help():
    """Muestra la ayuda del programa"""
    help_text = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                       HEALTH CHECK TOOL - AYUDA                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

DESCRIPCIÓN:
    Herramienta de monitorización de salud del sistema que verifica CPU, RAM,
    disco, servicios y puertos. Puede ejecutarse en modo interactivo o
    automático para monitorización continua.

USO:
    python3 monitor.py [OPCIONES]

OPCIONES:
    (sin opciones)      Modo interactivo con menú
    --auto              Modo automático (verificación única, para cron)
    --help, -h          Muestra esta ayuda
    --version, -v       Muestra la versión del programa

EJEMPLOS:
    # Modo interactivo
    python3 monitor.py

    # Ejecución automática (usar en cron)
    python3 monitor.py --auto

MODO INTERACTIVO:
    Menú con opciones:
    a) Comprobar servicios personalizados
    b) Comprobar puertos personalizados
    q) Salir

MODO AUTOMÁTICO:
    Verifica automáticamente:
    - CPU, RAM, Disco (umbrales configurables)
    - Servicios y puertos configurados en config.py
    - Registra resultados en logs/monitor.log

UMBRALES:
    CPU:     WARNING > 40% | CRITICAL > 80%
    RAM:     WARNING > 85% | CRITICAL > 90%
    DISCO:   WARNING > 70% | CRITICAL > 90%

LOGS:
    Ubicación: logs/monitor.log
    Rotación:  Diaria (mantiene 7 días)

CONFIGURACIÓN:
    Editar config.py para personalizar servicios y puertos

REQUISITOS:
    - Python 3.6+
    - psutil (pip install psutil)

EJEMPLOS DE CRON:
    # Ejecutar cada 5 minutos
    */5 * * * * cd /ruta/proyecto && python3 monitor.py --auto

╚═══════════════════════════════════════════════════════════════════════════╝
"""
    print(help_text)


def show_version():
    """Muestra la versión del programa"""
    version_text = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                       HEALTH CHECK TOOL                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

    Versión: 1.0.0
    Fecha:   Enero 2026
    Python:  3.6+
    
    Sistema de monitorización multiplataforma.
    
╚═══════════════════════════════════════════════════════════════════════════╝
"""

    print(version_text)


