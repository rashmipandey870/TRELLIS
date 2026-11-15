import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

// This file is loaded by Angular's @angular/build:application via the
// "plugins" key in angular.json. It wires @tailwindcss/vite so that
// Tailwind v4 properly scans Angular inline templates in .ts files.
export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
});
