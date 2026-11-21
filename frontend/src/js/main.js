import { createInertiaApp } from "@inertiajs/vue3";
import { createApp, h } from "vue";
import "#css/styles.css";

createInertiaApp({
    pages: { directory: "../views" },
    setup({ el, App, props, plugin }) {
        createApp({ render: () => h(App, props) })
            .use(plugin)
            .mount(el);
    },
});
