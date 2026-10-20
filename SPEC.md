# SPEC: CV digital de Marcia Catania

## Objetivo
Una página web estática (un solo HTML, sin servidor ni base de datos) con el perfil profesional de Marcia Catania,
publicada en internet con un link para mandar a reclutadores y poner en LinkedIn. Diseño nuevo, manteniendo el
contenido del borrador actual.

## Contexto
- Ya hay (en esta carpeta):
  - `perfil_digital_profesional (1).html`: el borrador con todo el contenido (perfil, casos de éxito, liderazgo,
    competencias, trayectoria, educación). Usa Tailwind y Lucide desde CDN.
  - `WhatsApp Image 2026-10-19 at 21.51.25.jpeg`: la foto de perfil (fondo gris, blazer celeste).
- Problemas del borrador que se arreglan en el camino:
  - Trayectoria: los ítems están en `<td>` dentro de `<ul>` (tienen que ser `<li>`), no se ven como lista.
  - Usa `brand-200`, `brand-300` y `brand-500`, que no están definidos en los colores, así que no pintan.
  - Busca la foto como `Photo.01.jpg` (no existe) y por eso muestra un dibujo SVG hecho por la IA. El dibujo se saca.
  - Carga Tailwind, Lucide y la fuente desde internet.
- El formato del proyecto se copia de `E:\EnDesarrollo\Apuestas`:
  - `CLAUDE.md`, `SPEC.md`, `.claude/settings.json`, `.gitignore`, git
  - Tailwind compilado con `tailwindcss.exe` (sin CDN), fuentes y Lucide en la carpeta del proyecto
  - Nombres y comentarios en castellano

## Qué hacer (paso a paso, de a uno)
1. **Base del proyecto**:
   - `CLAUDE.md`, `.claude/settings.json`, `.gitignore`
   - Carpetas: `sitio/` (lo que se publica), `tailwind/` (configuración y entrada), `herramientas/` (el .exe, no va
     a git), `scripts/`, `borrador/` (el HTML viejo como referencia)
   - Copiar de Apuestas: `tailwindcss.exe`, las fuentes Inter y `lucide.min.js`
   - `scripts/compilar_css.py` (genera `sitio/css/app.css`)
   - La foto pasa a `sitio/img/marcia.jpg`, achicada para web
   - `git init`
2. **Propuesta de diseño**: 2 o 3 direcciones visuales (colores, tipografía, cómo se ve el encabezado) en una página
   de muestra para elegir antes de armar todo.
   - Idea inicial: sobrio y editorial. Fondo claro cálido, tinta azul petróleo y el celeste del blazer como acento;
     títulos con una tipografía serif y el texto con Inter.
3. **La página** (`sitio/index.html`), con el diseño elegido y en este orden:
   - Encabezado: nombre, cargo, foto real, ubicación, idiomas, botones Email / WhatsApp / LinkedIn
   - Números destacados (24 personas a cargo, +14 años, 4 áreas)
   - Casos de éxito (los 6)
   - Liderazgo por área (Exportaciones, Importaciones, Depósito, Atención al cliente)
   - Competencias y herramientas
   - Trayectoria (línea de tiempo)
   - Formación y certificaciones
   - Pie con contacto
   - Menú arriba fijo que lleva a cada sección (en el celular, un menú desplegable)
4. **Detalles para compartir**:
   - Ícono de la pestaña (favicon) con las iniciales
   - Vista previa al pegar el link en LinkedIn / WhatsApp (título, descripción y foto: etiquetas Open Graph)
   - Que se lea bien en celular, tablet y computadora
5. **Publicación** en internet (gratis):
   - Recomendado: GitHub Pages (publica la carpeta `sitio/`, link tipo `usuario.github.io/cv-marcia`)
   - Alternativa: Netlify (se arrastra la carpeta `sitio/`)
   - Más adelante, si quieren, un dominio propio (tipo `marciacatania.com`, ~USD 10-15 por año)

## Detalles / reglas
- Nada se carga desde internet: CSS, JS, fuentes e imágenes viven en `sitio/`.
- El contenido es el del borrador. No se inventan datos, números ni logros; si algo falta o no cierra, se pregunta.
- Idioma: castellano (la versión en inglés queda para después, si se pide).
- La página tiene que pesar poco (la foto optimizada) para que abra rápido en el celular.

## Para confirmar con Marcia antes de publicar
- **WhatsApp**: el link es `wa.me/549230154361225`. En formato internacional va sin el 15 (¿`5492304361225`?).
- **Teléfono y email a la vista**: al publicar quedan visibles para cualquiera (y para robots de spam). ¿Los dejamos o
  solo el botón de WhatsApp / email?
- **LinkedIn**: falta el link a su perfil.
- **Fechas**: el último puesto termina en mayo 2026. ¿Está buscando trabajo ahora (y lo decimos, tipo "Disponible") o
  hay un puesto nuevo para agregar?

## Cómo sé que está bien (criterios de aceptación)
- [ ] Abro `sitio/index.html` con doble clic y se ve completo, sin internet.
- [ ] Se ve la foto real, no el dibujo.
- [ ] Trayectoria se ve como lista y todos los colores pintan.
- [ ] En el celular se lee bien y el menú funciona.
- [ ] Pego el link en WhatsApp y aparece la vista previa con la foto y el nombre.
- [ ] Los botones de Email y WhatsApp abren bien.
- [ ] El link público funciona desde otra computadora.
