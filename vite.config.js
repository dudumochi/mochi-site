import { defineConfig } from "vite";
import { globSync } from "node:fs";
import { resolve } from "node:path";

// site com várias páginas: cada index.html (Home, /cases/, /cases/<slug>/ …) é uma entrada
const pages = globSync("**/index.html", { exclude: (p) => /node_modules|dist|\.reanimate/.test(p) });

export default defineConfig({
  build: {
    rollupOptions: { input: Object.fromEntries(pages.map((p) => [p.replace(/\/?index\.html$/, "") || "home", resolve(p)])) },
  },
});
