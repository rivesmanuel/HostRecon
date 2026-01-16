from functions import *
from config import *
from time import sleep
import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

autoMode = '--auto' in sys.argv

os.makedirs('logs', exist_ok=True)

handler = TimedRotatingFileHandler(
    'logs/monitor.log',
    when=LOG_WHEN,
    interval=LOG_INTERVAL,
    backupCount=LOG_BACKUP_COUNT
)

formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

system = platform.system()

if autoMode:

    logging.info("Ejecutando en modo automático")

    dataRAM = check_memory()
    dataCPU = check_cpu()
    dataDisk = check_disk()
    
    if system == 'Windows':
        servicesList = DEFAULT_SERVICES_WINDOWS
        portsList = DEFAULT_PORTS_WINDOWS
    else:
        servicesList = DEFAULT_SERVICES_LINUX
        portsList = DEFAULT_PORTS_LINUX
    
    resultadosServices = check_services(servicesList)
    display_services(resultadosServices)

    resultadosPorts = check_ports(portsList)
    display_ports(resultadosPorts)

    logging.info("Verificación automática completada")

elif '--help' in sys.argv or '-h' in sys.argv:
    show_help()
    sys.exit(0)

elif '--version' in sys.argv or '-v' in sys.argv:
    show_version()
    sys.exit(0)          
    
else:

    logging.info("="*50)
    logging.info("Health Check Tool iniciado")
    logging.info(f"Sistema operativo: {system}")


    print("================ Bienvenido al Healty Check Tool ================")
    print("Ahora se mostrará información sobre el sistema...")
    sleep(2)

    dataRAM = check_memory()
    dataCPU = check_cpu()
    dataDisk = check_disk()
    host = '127.0.0.1'

    print(f"CPU: {dataCPU['porcentaje']}% - Estado: {dataCPU['estado']}")
    print(f"Disk: {dataDisk['porcentaje']}% - Estado: {dataDisk['estado']}")
    print(f"RAM: {dataRAM['porcentaje']}% - Estado: {dataRAM['estado']}")
    print(f"\tDisponible: {dataRAM['disponible_gb']} GB de {dataRAM['total_gb']} GB")

    print()
    while True:
        opcion = menu()
        if opcion == 'a':
            try:
                if os.name == 'nt':
                    os.system('cls')
                elif os.name == 'posix':
                    os.system('clear')
            except Exception as e:
                print(f"Error clearing screen: {e}")

            print(f"Tu sistema operativo es {system}, solo introduce servicios de tu sistema")

            texto = input("Introduce los servicios separados por comas: ")
            servicesList = [s.strip() for s in texto.split(',')]

            resultadosServices = check_services(servicesList)

            display_services(resultadosServices)

        elif opcion == 'b':
            try:
                if os.name == 'nt':
                    os.system('cls')
                elif os.name == 'posix':
                    os.system('clear')
            except Exception as e:
                print(f"Error clearing screen: {e}")

            print("================ Comprobación de puertos ===============")
            ports = input("Introduce los puertos separados por comas: ")
            try:
                portsList = []
                for p in ports.split(','):
                    puerto = int(p.strip())
                    
                    # Validar rango válido de puertos (1-65535)
                    if puerto < 1 or puerto > 65535:
                        print(f"[!] Puerto inválido: {puerto} (debe estar entre 1 y 65535)")
                        print("Usa -h o --help para más ayuda sobre la utilización de la herramienta")
                        continue
                    
                    portsList.append(puerto)
                
                # Verificar que al menos hay un puerto válido
                if not portsList:
                    print("[!] No se introdujeron puertos válidos")
                    print("Usa -h o --help para más ayuda sobre la utilización de la herramienta")
                    print()
                else:
                    resultadosPorts = check_ports(portsList)
                    display_ports(resultadosPorts)
                    print()
            
            except ValueError:
                print("[!] Error: Debes introducir números separados por comas")
                print("Ejemplo: 80,443,22,3306")
                print("Usa -h o --help para más ayuda sobre la utilización de la herramienta")
                print()


        elif opcion == 'q':
            logging.info("Aplicación cerrada por usuario")
            print("\n¡Hasta luego!")
            exit()
        
        else:
            print("Opción incorrecta")


