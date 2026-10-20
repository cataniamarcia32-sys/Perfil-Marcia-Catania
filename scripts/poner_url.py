"""Pone la dirección pública del CV en las etiquetas de la vista previa (WhatsApp / LinkedIn).

Uso:  python scripts/poner_url.py https://usuario.github.io/cv-marcia/

WhatsApp y LinkedIn necesitan la dirección completa de la imagen (no sirve "img/vista-previa.jpg"). Se puede correr
de nuevo si cambia la dirección (por ejemplo, con un dominio propio).
"""
import os
import re
import sys

CARPETA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAGINA = os.path.join(CARPETA_BASE, "sitio", "index.html")


def main():
    if len(sys.argv) != 2 or not sys.argv[1].startswith("https://"):
        sys.exit("Uso: python scripts/poner_url.py https://usuario.github.io/cv-marcia/")
    url = sys.argv[1].rstrip("/") + "/"
    html = open(PAGINA, encoding="utf-8").read()

    # La imagen: lo que haya antes de img/vista-previa.jpg se reemplaza por la URL
    html = re.sub(r'content="[^"]*img/vista-previa\.jpg"', f'content="{url}img/vista-previa.jpg"', html)
    # og:url: se cambia si ya está, si no se agrega después de og:type
    if 'property="og:url"' in html:
        html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', html)
    else:
        html = html.replace('<meta property="og:type" content="profile">',
                            f'<meta property="og:type" content="profile">\n    <meta property="og:url" content="{url}">')

    with open(PAGINA, "w", encoding="utf-8") as archivo:
        archivo.write(html)
    print(f"OK: vista previa apuntando a {url}")


if __name__ == "__main__":
    main()
