import { createInertiaApp } from "@inertiajs/svelte";
import "#css/styles.css";

createInertiaApp({
    pages: { directory: "../views" },
});
