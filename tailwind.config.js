module.exports = {
  content: [
    "./src/**/*.{html,js,py}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    colors: {
      // Override default colors
      blue: {
        50: '#E8E8FE',  // Lighter shade of your blue
        100: '#D1D1FD',
        200: '#A3A3FC',
        300: '#7676FA',
        400: '#4A4AF9',  // Your main blue
        500: '#3B3BC7',  // Darker shades
        600: '#2D2D95',
        700: '#1E1E63',
        800: '#0F0F32',
        900: '#09092D',  // Your black
      },
      black: '#09092D',
      white: '#FFFFFF',
      gray: {
        50: '#FFFFFF',
        100: '#FAFAFC',
        200: '#F3F3F7',  // Your gray
        300: '#E6E6ED',
        400: '#D9D9E3',
        500: '#CCCCDA',
        600: '#B3B3C4',
        700: '#9999AE',
        800: '#808098',
        900: '#666682',
      },
      yellow: {
        50: '#FEFDF3',
        100: '#FDFBE7',
        200: '#FBF7CF',
        300: '#F9F3B7',
        400: '#F7EF9F',
        500: '#F9EF77',  // Your yellow
        600: '#C7BF5F',
        700: '#958F47',
        800: '#635F2F',
        900: '#322F18',
      },
      green: {
        50: '#F4FDF8',
        100: '#E9FBF1',
        200: '#D3F7E3',
        300: '#BDF3D5',
        400: '#A7EFC7',
        500: '#8BF0BB',  // Your green
        600: '#6FC095',
        700: '#53906F',
        800: '#37604A',
        900: '#1C3025',
      },
      red: {
        50: '#FFF5F6',
        100: '#FFEBEC',
        200: '#FFD7DA',
        300: '#FFC3C7',
        400: '#FFAFB5',
        500: '#FF8D96',  // Your red
        600: '#CC7178',
        700: '#99555A',
        800: '#66393C',
        900: '#331C1E',
      },
      purple: {
        50: '#F9F6FF',
        100: '#F3EDFF',
        200: '#E7DBFF',
        300: '#DBC9FF',
        400: '#CFB7FF',
        500: '#BFA1FF',  // Your purple
        600: '#9981CC',
        700: '#736199',
        800: '#4C4066',
        900: '#262033',
      },
    },
    extend: {
      // You can add additional custom colors or extend other theme properties here
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}