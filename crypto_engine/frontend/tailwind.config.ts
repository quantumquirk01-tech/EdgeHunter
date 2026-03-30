const config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        background: '#0A0A0A',
        surface: '#111111',
        accent: '#00FF9F',
        electric: '#00C2FF',
        warning: '#FF9F1C',
        danger: '#FF3B3B'
      },
      boxShadow: {
        neon: '0 0 28px rgba(0, 255, 159, 0.28)',
        electric: '0 0 24px rgba(0, 194, 255, 0.26)'
      },
      backdropBlur: {
        xl: '18px'
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 0 rgba(0,255,159,0)' },
          '50%': { boxShadow: '0 0 34px rgba(0,255,159,0.35)' }
        },
        scanLine: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' }
        }
      },
      animation: {
        pulseGlow: 'pulseGlow 1.5s ease-in-out 3',
        scanLine: 'scanLine 2.2s linear infinite'
      }
    }
  },
  plugins: []
};

export default config;
