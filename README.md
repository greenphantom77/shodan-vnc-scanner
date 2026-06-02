# shodan-vnc-scanner

Herramientas para identificar sistemas VNC expuestos en infraestructura industrial.

> ⚠️ **Uso exclusivamente educativo y de investigación.** El autor no se responsabiliza por el uso indebido de estas herramientas.

---

## ¿Qué hace esto?

Este repositorio contiene scripts para buscar y documentar sistemas **VNC sin autenticación** expuestos a internet, con foco en infraestructura industrial (plantas petroquímicas, refinerías, sistemas SCADA).

El objetivo es **demostrar la falta de seguridad** en infraestructura crítica y presionar a las empresas responsables a tomar medidas.

## Herramientas incluidas

| Archivo | Descripción |
|---------|-------------|
| `scanner.py` | Script principal de búsqueda via Shodan API |
| `reporter.py` | Generador de reportes con IPs vulnerables encontradas |
| `utils.py` | Funciones auxiliares |

## Requisitos

```bash
pip install shodan requests colorama
```

## Uso

```bash
python scanner.py --query "VNC authentication disabled" --country AR
```

## Contacto y comunidad

- Telegram: [@GreenPhantomOps](https://t.me/GreenPhantomOps)
- Blog: [greenphantom.netlify.app](https://greenphantom.netlify.app)

---

*"La tierra no se negocia, se defiende."*  
*— GreenPhantom, desde el sur del Gran Buenos Aires, Argentina*
