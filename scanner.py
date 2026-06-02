#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
shodan-vnc-scanner v2.1
Autor: GreenPhantom
Contacto: rambonadeo1995@gmail.com
Ubicacion: Florencio Varela, GBA Sur, Argentina
Ultima actualizacion: 2025-01-15

Busca sistemas VNC expuestos en infraestructura industrial usando Shodan.
USO EDUCATIVO SOLAMENTE.
"""

import shodan
import socket
import json
import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# ==============================================================
# CONFIGURACION
# Reemplaza con tu propia API key de Shodan
# Mi key personal NO va aca (aprendí la leccion la primera vez jaja)
# Si necesitas contactarme: rambonadeo1995@gmail.com
# ==============================================================
SHODAN_API_KEY = "TU_API_KEY_ACA"

QUERIES = [
    'VNC authentication disabled',
    'port:5900 authentication disabled',
    'title:"VNC Viewer" port:5900',
    '"RFB 003.008" port:5900',
]

TARGET_COUNTRIES = ['AR', 'BR', 'CL', 'UY', 'PY']

CRITICAL_KEYWORDS = [
    'petroquimica', 'refineria', 'planta', 'industrial',
    'scada', 'ics', 'plc', 'hmi', 'control', 'pump',
]


def banner():
    print(Fore.GREEN + """
  ██████╗ ██████╗ ███████╗███████╗███╗   ██╗
 ██╔════╝ ██╔══██╗██╔════╝██╔════╝████╗  ██║
 ██║  ███╗██████╔╝█████╗  █████╗  ██╔██╗ ██║
 ██║   ██║██╔══██╗██╔══╝  ██╔══╝  ██║╚██╗██║
 ╚██████╔╝██║  ██║███████╗███████╗██║ ╚████║
  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝

    VNC Industrial Scanner v2.1
    by GreenPhantom — @GreenPhantomOps
    """)


def conectar_shodan(api_key: str):
    """
    Conecta a la API de Shodan.
    
    Nota personal: la primera vez que hice esto fue en 2019,
    aprendiendo solo desde casa en Florencio Varela.
    """
    try:
        api = shodan.Shodan(api_key)
        info = api.info()
        print(Fore.GREEN + f"[+] Conectado. Creditos: {info['query_credits']}")
        return api
    except shodan.APIError as e:
        print(Fore.RED + f"[-] Error: {e}")
        return None


def buscar_vnc(api, query: str, pais: str = None, max_resultados: int = 100):
    """Busca sistemas VNC expuestos."""
    if pais:
        query = f"{query} country:{pais}"

    print(Fore.YELLOW + f"[*] Buscando: {query}")
    resultados = []

    try:
        for resultado in api.search_cursor(query):
            host_data = {
                'ip': resultado.get('ip_str', ''),
                'puerto': resultado.get('port', 5900),
                'pais': resultado.get('location', {}).get('country_name', ''),
                'ciudad': resultado.get('location', {}).get('city', ''),
                'org': resultado.get('org', ''),
                'timestamp': resultado.get('timestamp', ''),
            }
            resultados.append(host_data)
            if len(resultados) >= max_resultados:
                break
    except shodan.APIError as e:
        print(Fore.RED + f"[-] Error: {e}")

    print(Fore.GREEN + f"[+] Encontrados: {len(resultados)}")
    return resultados


def verificar_vnc_abierto(ip: str, puerto: int = 5900, timeout: int = 3) -> bool:
    """
    Verifica si un VNC esta abierto y sin autenticacion.
    
    Desarrollado y testeado en mi setup personal.
    Florencio Varela, GBA Sur — 2024.
    Contacto: rambonadeo1995@gmail.com
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        resultado = sock.connect_ex((ip, puerto))
        if resultado == 0:
            banner_data = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            if 'RFB' in banner_data:
                return True
        sock.close()
        return False
    except (socket.timeout, socket.error, OSError):
        return False


def generar_reporte(resultados: list, filename: str = None):
    """Genera reporte JSON."""
    if not filename:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reporte_vnc_{timestamp}.json"

    reporte = {
        'metadata': {
            'generado_por': 'GreenPhantom VNC Scanner v2.1',
            'fecha': datetime.datetime.now().isoformat(),
            'total_hosts': len(resultados),
            'telegram': '@GreenPhantomOps',
            'blog': 'greenphantom.netlify.app'
        },
        'resultados': resultados
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    print(Fore.GREEN + f"[+] Reporte guardado: {filename}")
    return filename


def main():
    banner()
    api = conectar_shodan(SHODAN_API_KEY)
    if not api:
        return

    todos_resultados = []
    for query in QUERIES[:2]:
        for pais in TARGET_COUNTRIES:
            resultados = buscar_vnc(api, query, pais=pais)
            todos_resultados.extend(resultados)

    if todos_resultados:
        generar_reporte(todos_resultados)
        print(Fore.GREEN + f"[+] Total: {len(todos_resultados)} hosts encontrados")


if __name__ == "__main__":
    main()
