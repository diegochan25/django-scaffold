import { resolve } from "node:path";
import inertia from "@inertiajs/vite";
import tailwindcss from "@tailwindcss/vite";
import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

export default defineConfig({
    plugins: [tailwindcss(), vue(), inertia({ ssr: false })],
    base: "/static/vite/",
    build: {
        manifest: true,
        outDir: resolve(import.meta.dirname, "../static/vite"),
        emptyOutDir: true,
        rollupOptions: {
            input: resolve(import.meta.dirname, "src/js/main.js"),
        },
    },
    server: {
        host: "localhost",
        port: 5173,
        strictPort: true,
        cors: true,
    },
});
