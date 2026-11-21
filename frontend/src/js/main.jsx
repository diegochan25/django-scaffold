import { createInertiaApp } from "@inertiajs/react";
import { createRoot } from "react-dom/client";
import "#css/styles.css";

createInertiaApp({
    pages: { directory: "../views" },
    setup({ el, App, props }) {
        createRoot(el).render(<App {...props} />);
    },
});
