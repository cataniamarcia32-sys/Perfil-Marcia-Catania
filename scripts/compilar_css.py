"""Compila el CSS de Tailwind con el CLI standalone (herramientas/tailwindcss.exe).

Uso:  python scripts/compilar_css.py

Genera sitio/css/app.css. Hay que correrlo cada vez que se agregan clases de Tailwind nuevas en el HTML.
"""
import os
import subprocess
import sys

# Carpeta raíz del proyecto (donde está este SPEC.md)
CARPETA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TAILWIND = os.path.join(CARPETA_BASE, "herramientas", "tailwindcss.exe")


def main():
    if not os.path.exists(TAILWIND):
        sys.exit("Falta herramientas/tailwindcss.exe (se copia de la carpeta de Apuestas).")
    subprocess.run(
        [TAILWIND, "-c", "tailwind/config.js", "-i", "tailwind/entrada.css",
         "-o", "sitio/css/app.css", "--minify"],
        cwd=CARPETA_BASE, check=True, capture_output=True,
    )
    print("OK: sitio/css/app.css")


if __name__ == "__main__":
    main()
