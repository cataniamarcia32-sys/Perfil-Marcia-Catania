# Proyecto: CV digital de Marcia Catania

Página web estática con el perfil profesional de Marcia Catania, para publicar en internet y mandar el link a
reclutadores / LinkedIn. El plan está en `SPEC.md`.

## Stack
- Un HTML estático (`sitio/index.html`), sin servidor ni base de datos
- Tailwind CSS v3 compilado con el CLI standalone (`herramientas/tailwindcss.exe`, sin Node, sin CDN)
- Íconos Lucide (`sitio/js/vendor/lucide.min.js`) y fuente Inter (`sitio/fuentes/`), copiados de
  `E:\EnDesarrollo\Apuestas`

## Reglas que NO se rompen
- Nada se carga desde internet: CSS, JS, fuentes e imágenes viven en `sitio/`.
- El contenido sale del borrador (`borrador/perfil_digital_profesional.html`). No inventes datos, números ni logros;
  si algo falta o no cierra, preguntame.
- Nombres y comentarios en castellano.
- No agregues ninguna librería ni herramienta nueva sin avisarme y explicarme para qué.
- Todo lo que se publica va dentro de `sitio/`; afuera queda solo lo de trabajo.

## Cómo está armado
- `sitio/`: lo que se publica (la página, `css/app.css` compilado, fuentes, Lucide, `img/marcia.jpg`).
- `tailwind/`: `config.js` (colores y tipografías) y `entrada.css` (estilos propios).
- `borrador/`: el HTML original y la foto original, como referencia. No se publican.
- `herramientas/`: `tailwindcss.exe` (no va a git, se copia de Apuestas).

## Comandos
- Si tocás clases de Tailwind en el HTML, recompilá el CSS: `python scripts/compilar_css.py`
- Para verla: abrir `sitio/index.html` con doble clic.

## Cómo quiero que trabajes conmigo
- Trabajá en pasos chicos. Después de cada cambio, explicame en una o dos líneas qué hiciste.
- Si algo no lo entiendo y te lo pregunto, explicámelo sin dar por sentado que sé.
- No inventes datos. Si te falta info, preguntame.
- Antes de un cambio grande, contame el plan y esperá que te diga que sí.

## Estilo
- Solución simple y directa antes que elegante y compleja.
