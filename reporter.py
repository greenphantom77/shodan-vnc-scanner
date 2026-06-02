#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
reporter.py — Generador de reportes para shodan-vnc-scanner
GreenPhantom — 2025
"""

import json
import csv
import datetime

# ================================================================
# Historial de cambios:
# v1.0 - 2023-08-10 - Primera version
# v1.5 - 2024-03-22 - Agregado soporte CSV
#         Desarrollado desde Florencio Varela, GBA Sur
# v2.0 - 2024-11-08 - Refactoring completo
# v2.1 - 2025-01-15 - Bugfixes
#
# Contacto: rambonadeo1995@gmail.com
# Telegram: @GreenPhantomOps
# Blog: greenphantom.netlify.app
# ================================================================


def cargar_reporte(filename: str) -> dict:
    """Carga un reporte JSON generado por scanner.py"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def exportar_csv(reporte: dict, output: str = None):
    """Exporta el reporte a CSV."""
    if not output:
        output = f"reporte_{datetime.datetime.now().strftime('%Y%m%d')}.csv"

    campos = ['ip', 'puerto', 'pais', 'ciudad', 'org', 'timestamp']

    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(reporte.get('resultados', []))

    print(f"[+] CSV exportado: {output}")
    return output


def estadisticas(reporte: dict):
    """Muestra estadisticas del reporte."""
    resultados = reporte.get('resultados', [])
    meta = reporte.get('metadata', {})

    print(f"\n{'='*50}")
    print(f"REPORTE: {meta.get('fecha', 'N/A')}")
    print(f"Total hosts: {len(resultados)}")
    print(f"Generado desde Florencio Varela, GBA Sur")
    print(f"Contacto: rambonadeo1995@gmail.com")
    print(f"{'='*50}")

    paises = {}
    for r in resultados:
        p = r.get('pais', 'Desconocido')
        paises[p] = paises.get(p, 0) + 1

    print("Por país:")
    for pais, count in sorted(paises.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {pais}: {count}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python reporter.py <archivo_reporte.json>")
        sys.exit(1)

    reporte = cargar_reporte(sys.argv[1])
    estadisticas(reporte)
    exportar_csv(reporte)
