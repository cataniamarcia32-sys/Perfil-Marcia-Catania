"""Arma las imágenes para compartir el link.

Uso:  python scripts/armar_imagenes.py

- sitio/img/vista-previa.jpg (1200 × 630): la imagen que muestran WhatsApp / LinkedIn al pegar el link.
  Sale de scripts/vista_previa.html.
- sitio/img/icono-180.png: el ícono para cuando se guarda el link en la pantalla de inicio del celular.
  Sale de sitio/img/favicon.svg.

Las capturas las saca Chrome headless; el pasaje a JPG lo hace Windows (System.Drawing, por PowerShell), así no
hace falta instalar ninguna librería.
"""
import os
import subprocess
import sys
import tempfile

CARPETA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG = os.path.join(CARPETA_BASE, "sitio", "img")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def url(ruta):
    return "file:///" + ruta.replace("\\", "/")


def captura(pagina, ancho, alto, destino):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--force-device-scale-factor=1", f"--window-size={ancho},{alto}", f"--screenshot={destino}",
                    url(pagina)], check=True, capture_output=True)


def png_a_jpg(origen, destino, calidad=85):
    script = (
        "Add-Type -AssemblyName System.Drawing;"
        f"$img = [System.Drawing.Image]::FromFile('{origen}');"
        "$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' };"
        "$parametros = New-Object System.Drawing.Imaging.EncoderParameters(1);"
        f"$parametros.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]{calidad});"
        f"$img.Save('{destino}', $codec, $parametros); $img.Dispose()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", script], check=True, capture_output=True)


def main():
    if not os.path.exists(CHROME):
        sys.exit(f"No encuentro Chrome en {CHROME}")
    with tempfile.TemporaryDirectory() as temporal:
        # Vista previa para compartir
        png = os.path.join(temporal, "vista-previa.png")
        captura(os.path.join(CARPETA_BASE, "scripts", "vista_previa.html"), 1200, 630, png)
        destino = os.path.join(IMG, "vista-previa.jpg")
        png_a_jpg(png, destino)
        print(f"OK: sitio/img/vista-previa.jpg ({os.path.getsize(destino) / 1024:.0f} KB)")

        # Ícono 180 × 180: el SVG dibujado a pantalla completa
        envoltorio = os.path.join(temporal, "icono.html")
        with open(envoltorio, "w", encoding="utf-8") as archivo:
            archivo.write('<link rel="stylesheet" href="' + url(os.path.join(CARPETA_BASE, "sitio", "fuentes", "fuentes.css")) + '">'
                          '<body style="margin:0;background:#13363f">'
                          f'<img src="{url(os.path.join(IMG, "favicon.svg"))}" style="width:180px;height:180px;display:block">')
        captura(envoltorio, 180, 180, os.path.join(IMG, "icono-180.png"))
        print("OK: sitio/img/icono-180.png")


if __name__ == "__main__":
    main()
