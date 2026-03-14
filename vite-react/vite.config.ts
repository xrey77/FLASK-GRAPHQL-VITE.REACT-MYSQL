import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  ssr: {
    noExternal: ['@apollo/client'],
  },  
  server: {
    origin: 'http://localhost:5173',
    port: 5173,
  },  
})
