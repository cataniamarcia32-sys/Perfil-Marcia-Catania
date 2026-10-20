// Configuración de Tailwind para el CV. Los colores y tipografías del diseño se definen en el paso 2.
module.exports = {
  content: [
    './sitio/**/*.html',
    './sitio/js/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
};
