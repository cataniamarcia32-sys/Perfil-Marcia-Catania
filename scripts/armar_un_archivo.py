"""Arma el CV en UN SOLO archivo HTML por idioma, para mandarlo por WhatsApp o mail.

Uso:  python scripts/armar_un_archivo.py

Genera en para_enviar/ "CV Marcia Catania.html" (castellano) y "CV Marcia Catania (English).html", con todo
adentro: CSS, fuentes y foto (en base64) y los íconos ya dibujados (Chrome headless abre la página, Lucide dibuja los
íconos y se guarda el resultado). Así no hace falta el script de Lucide (440 KB). En el archivo suelto, el selector
ES | EN lleva a la otra versión publicada (sale de og:url). Hay que correrlo de nuevo cada vez que se cambia la página.
"""
import base64
import os
import re
import subprocess
import sys

CARPETA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITIO = os.path.join(CARPETA_BASE, "sitio")
PARA_ENVIAR = os.path.join(CARPETA_BASE, "para_enviar")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# (página, archivo de salida, prefijo de las rutas hacia sitio/ desde esa página)
PAGINAS = (
    ("index.html", "CV Marcia Catania.html", ""),
    (os.path.join("en", "index.html"), "CV Marcia Catania (English).html", "../"),
)

# Solo los pesos de Inter que usa la página (los demás archivos se dejan afuera para que pese menos)
PESOS_INTER = ("400", "500", "600", "700")


def en_base64(ruta, tipo):
    with open(ruta, "rb") as archivo:
        return f"data:{tipo};base64," + base64.b64encode(archivo.read()).decode("ascii")


def fuentes_adentro():
    """fuentes.css con cada .woff2 metido adentro, sin los pesos de Inter que no se usan."""
    carpeta = os.path.join(SITIO, "fuentes")
    css = open(os.path.join(carpeta, "fuentes.css"), encoding="utf-8").read()
    salida = []
    for bloque in re.findall(r"@font-face \{.*?\}", css, re.S):
        archivo = re.search(r"url\((.*?)\)", bloque).group(1)
        if archivo.startswith("Inter-") and archivo.split("-")[1] not in PESOS_INTER:
            continue
        salida.append(bloque.replace(f"url({archivo})", f"url({en_base64(os.path.join(carpeta, archivo), 'font/woff2')})"))
    return "\n".join(salida)


def pagina_con_iconos(pagina):
    """Abre la página en Chrome headless y devuelve el HTML con los íconos de Lucide ya dibujados."""
    url = "file:///" + os.path.join(SITIO, pagina).replace("\\", "/")
    resultado = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--dump-dom", url],
                               capture_output=True, check=True)
    return resultado.stdout.decode("utf-8")


def armar(pagina, salida, prefijo, estilos):
    html = pagina_con_iconos(pagina)
    if "<svg" not in html:
        sys.exit(f"Chrome no dibujó los íconos de {pagina} (¿falla Lucide?)")

    html = re.sub(rf'<link rel="stylesheet" href="{prefijo}fuentes/fuentes.css">\s*<link rel="stylesheet" href="{prefijo}css/app.css">',
                  lambda _: estilos, html)
    # Lucide ya no hace falta: se saca su script y la llamada que dibuja los íconos
    html = html.replace(f'<script src="{prefijo}js/vendor/lucide.min.js"></script>', "")
    html = html.replace("lucide.createIcons();", "")
    # Foto e íconos de la pestaña adentro
    for atributo, archivo, tipo in (("src", "marcia.jpg", "image/jpeg"), ("href", "favicon.svg", "image/svg+xml"),
                                    ("href", "icono-180.png", "image/png")):
        html = html.replace(f'{atributo}="{prefijo}img/{archivo}"', f'{atributo}="{en_base64(os.path.join(SITIO, "img", archivo), tipo)}"')
    # Los avisos de la otra versión (hreflang) no sirven en un archivo suelto
    html = re.sub(r'\s*<link rel="alternate" hreflang="\w+" href="[^"]*">', "", html)
    return html


def main():
    if not os.path.exists(CHROME):
        sys.exit(f"No encuentro Chrome en {CHROME}")
    app_css = open(os.path.join(SITIO, "css", "app.css"), encoding="utf-8").read()
    estilos = f"<style>\n{fuentes_adentro()}\n{app_css}\n</style>"

    armadas = [armar(pagina, salida, prefijo, estilos) for pagina, salida, prefijo in PAGINAS]
    # El selector de idioma lleva a la otra versión publicada (su og:url)
    urls = [re.search(r'<meta property="og:url" content="([^"]*)">', html).group(1) for html in armadas]
    armadas[0] = armadas[0].replace('href="en/"', f'href="{urls[1]}"')
    armadas[1] = armadas[1].replace('href="../"', f'href="{urls[0]}"')

    os.makedirs(PARA_ENVIAR, exist_ok=True)
    for html, (_, salida, _) in zip(armadas, PAGINAS):
        sueltos = re.findall(r'(?:src|href)="(?!data:|#|https?:|mailto:|tel:)([^"]+)"', html)
        if sueltos:
            sys.exit(f"{salida}: quedaron archivos sin meter adentro: {sueltos}")
        ruta = os.path.join(PARA_ENVIAR, salida)
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(html)
        print(f"OK: {ruta} ({os.path.getsize(ruta) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
