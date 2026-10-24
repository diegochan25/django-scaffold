import Alpine from "alpinejs";
import htmx from "htmx.org";
import { createIcons } from "lucide";
import "./styles.css";

window.Alpine = Alpine;
window.htmx = htmx;

Alpine.start();

createIcons();

document.addEventListener("htmx:afterSettle", () => createIcons()); 
