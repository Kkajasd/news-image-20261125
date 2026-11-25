// The World Today — Wednesday, 25 November 2026.
// The front page is pre-rendered by tools/draw_frontpage.py into entry.png;
// this program only copies that image to the output directory, so repeated
// runs write byte-identical output.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error("entry.png not found next to main.ts");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
const bytes = statSync(target).size;
if (bytes !== statSync(source).size) {
  throw new Error("copied entry.png size mismatch");
}
console.log(`Wrote ${target} (${bytes} bytes)`);
