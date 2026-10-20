"""Arma el CV en UN SOLO archivo HTML, para mandarlo por WhatsApp o mail.

Uso:  python scripts/armar_un_archivo.py

Genera para_enviar/CV Marcia Catania.html con todo adentro: CSS, fuentes y foto (en base64) y los íconos ya
dibujados (Chrome headless abre la página, Lucide dibuja los íconos y se guarda el resultado). Así no hace falta
el script de Lucide (440 KB). Hay que correrlo de nuevo cada vez que se cambia sitio/index.html.
"""
import base64
import os
import re
import subprocess
import sys

CARPETA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITIO = os.path.join(CARPETA_BASE, "sitio")
SALIDA = os.path.join(CARPETA_BASE, "para_enviar", "CV Marcia Catania.html")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Solo los pesos de Inter que usa la página (los demás archivos se dejan afuera para que pese menos)
PESOS_INTER = ("400", "500", "600", "700")


def en_base64(ruta, tipo):
    with open(ruta, "rb") as archivo:
        return f"data:{tipo};base64," + base64.b64encode(archivo.read()).decode("ascii")


def fuentes_adentro():
    """fuentes.css con cada .woff2 metido adentro, sin los pesos de Inter que no se usan."""
    carpeta = os.path.join(SITIO, "fuentes")
    css = open(os.path.join(carpeta, "fuentes.css"), encoding="utf-8").read()
    bloques = re.findall(r"@font-face \{.*?\}", css, re.S)
    salida = []
    for bloque in bloques:
        archivo = re.search(r"url\((.*?)\)", bloque).group(1)
        if archivo.startswith("Inter-") and archivo.split("-")[1] not in PESOS_INTER:
            continue
        salida.append(bloque.replace(f"url({archivo})", f"url({en_base64(os.path.join(carpeta, archivo), 'font/woff2')})"))
    return "\n".join(salida)


def pagina_con_iconos():
    """Abre sitio/index.html en Chrome headless y devuelve el HTML con los íconos de Lucide ya dibujados."""
    if not os.path.exists(CHROME):
        sys.exit(f"No encuentro Chrome en {CHROME}")
    url = "file:///" + os.path.join(SITIO, "index.html").replace("\\", "/")
    resultado = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--dump-dom", url],
                               capture_output=True, check=True)
    return resultado.stdout.decode("utf-8")


def main():
    html = pagina_con_iconos()
    if "<svg" not in html:
        sys.exit("Chrome no dibujó los íconos (¿falla Lucide?)")

    # CSS: fuentes + app.css, metidos en un <style>
    app_css = open(os.path.join(SITIO, "css", "app.css"), encoding="utf-8").read()
    estilos = f"<style>\n{fuentes_adentro()}\n{app_css}\n</style>"
    html = re.sub(r'<link rel="stylesheet" href="fuentes/fuentes.css">\s*<link rel="stylesheet" href="css/app.css">',
                  lambda _: estilos, html)

    # Lucide ya no hace falta: se saca su script y la llamada que dibuja los íconos
    html = html.replace('<script src="js/vendor/lucide.min.js"></script>', "")
    html = html.replace("lucide.createIcons();", "")

    # Foto e íconos de la pestaña adentro
    for atributo, archivo, tipo in (("src", "marcia.jpg", "image/jpeg"), ("href", "favicon.svg", "image/svg+xml"),
                                    ("href", "icono-180.png", "image/png")):
        html = html.replace(f'{atributo}="img/{archivo}"', f'{atributo}="{en_base64(os.path.join(SITIO, "img", archivo), tipo)}"')

    # Control: que no quede nada apuntando a archivos de al lado
    sueltos = re.findall(r'(?:src|href)="(?!data:|#|https?:|mailto:|tel:)([^"]+)"', html)
    if sueltos:
        sys.exit(f"Quedaron archivos sin meter adentro: {sueltos}")

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as archivo:
        archivo.write(html)
    print(f"OK: {SALIDA} ({os.path.getsize(SALIDA) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
