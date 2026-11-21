import { resolve } from "node:path";
import inertia from "@inertiajs/vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
    plugins: [tailwindcss(), react(), inertia({ ssr: false })],
    base: "/static/vite/",
    build: {
        manifest: true,
        outDir: resolve(import.meta.dirname, "../static/vite"),
        emptyOutDir: true,
        rollupOptions: {
            input: resolve(import.meta.dirname, "src/js/main.jsx"),
        },
    },
    server: {
        host: "localhost",
        port: 5173,
        strictPort: true,
        cors: true,
    },
});
