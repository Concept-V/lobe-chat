import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  root: 'src',
  server: {
    host: true, // Needed for proper Docker networking
    port: 3000,
    strictPort: true, // Fail if port is in use
    watch: {
      usePolling: true, // Needed for Docker on Windows
    },
  },
  build: {
    outDir: '../dist',
    sourcemap: true,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});