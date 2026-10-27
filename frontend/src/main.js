import Alpine from "alpinejs";
import htmx from "htmx.org";
import { createIcons, icons } from "lucide";
import "./styles.css";

window.Alpine = Alpine;
window.htmx = htmx;

Alpine.start();

createIcons({ icons });

document.addEventListener("htmx:afterSettle", () => createIcons({ icons })); 
