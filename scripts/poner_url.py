"""Pone la dirección pública del CV en las etiquetas de la vista previa (WhatsApp / LinkedIn), en los dos idiomas.

Uso:  python scripts/poner_url.py https://usuario.github.io/perfil-marcia-catania/

WhatsApp y LinkedIn necesitan la dirección completa de la imagen (no sirve "img/vista-previa.jpg"). Se puede correr
de nuevo si cambia la dirección (por ejemplo, con un dominio propio).
"""
import os
import re
import sys

CARPETA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# (página, dirección de la página dentro del sitio, imagen de la vista previa)
PAGINAS = (
    (os.path.join(CARPETA_BASE, "sitio", "index.html"), "", "vista-previa.jpg"),
    (os.path.join(CARPETA_BASE, "sitio", "en", "index.html"), "en/", "vista-previa-en.jpg"),
)


def main():
    if len(sys.argv) != 2 or not sys.argv[1].startswith("https://"):
        sys.exit("Uso: python scripts/poner_url.py https://usuario.github.io/perfil-marcia-catania/")
    url = sys.argv[1].rstrip("/") + "/"
    for ruta, subcarpeta, imagen in PAGINAS:
        html = open(ruta, encoding="utf-8").read()
        # La imagen: lo que haya antes de img/<imagen> se reemplaza por la URL
        html = re.sub(rf'content="[^"]*img/{re.escape(imagen)}"', f'content="{url}img/{imagen}"', html)
        # og:url: se cambia si ya está, si no se agrega después de og:type
        if 'property="og:url"' in html:
            html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}{subcarpeta}">', html)
        else:
            html = html.replace('<meta property="og:type" content="profile">',
                                f'<meta property="og:type" content="profile">\n    <meta property="og:url" content="{url}{subcarpeta}">')
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(html)
        print(f"OK: {url}{subcarpeta}")


if __name__ == "__main__":
    main()
