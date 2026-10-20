// Configuración de Tailwind para el CV. Diseño "A · Editorial cálido" (elegido el 19/10, ver propuestas/).
module.exports = {
  content: [
    './sitio/**/*.html',
    './sitio/js/*.js',
  ],
  theme: {
    extend: {
      colors: {
        fondo: '#f6f2ea',     // marfil
        tinta: '#13363f',     // azul petróleo: títulos, botones, franja de liderazgo
        texto: '#33454b',     // texto corrido
        suave: '#6b7b80',     // fechas, aclaraciones
        acento: '#2f7fa8',    // celeste profundo: volantas, empresas, palabra destacada
        celeste: '#cfe4f1',   // el celeste del blazer: bloque detrás de la foto, rayas de impacto
        linea: '#ddd5c6',     // líneas finas
        papel: '#fbf9f5',     // tarjetas sobre el marfil
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        serif: ['"Source Serif 4"', 'Georgia', 'serif'],
      },
    },
  },
};
