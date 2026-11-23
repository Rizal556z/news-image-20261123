// Entrypoint for the Monday 23 November 2026 news poster.
//
// Checks that entry.png sitting next to this file is a real 1024x1024
// PNG under the 1 MiB limit and readable, then writes an identical copy
// to the output folder the grader reads (second argument, else
// MAKEFUN_OUTPUT_DIR, else ./out) with mode 0644, and exits 0.
// Any problem exits 1. Pure Node, no network, no randomness.
import { accessSync, chmodSync, constants, copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const POSTER = "entry.png";
const WANT_WIDTH = 1024;
const WANT_HEIGHT = 1024;
const SIZE_LIMIT = 1024 * 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function scriptDir() {
  return dirname(fileURLToPath(import.meta.url));
}

function findPoster() {
  const besideScript = join(scriptDir(), POSTER);
  if (existsSync(besideScript)) return besideScript;
  return resolve(process.cwd(), POSTER);
}

function posterSize(path) {
  const head = readFileSync(path).subarray(0, 33);
  if (!head.subarray(0, 8).equals(PNG_MAGIC)) {
    throw new Error("not a PNG file: bad signature");
  }
  if (head.toString("ascii", 12, 16) !== "IHDR") {
    throw new Error("not a PNG file: first chunk is not IHDR");
  }
  return { width: head.readUInt32BE(16), height: head.readUInt32BE(20) };
}

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function main() {
  const source = findPoster();
  accessSync(source, constants.R_OK);
  const size = posterSize(source);
  if (size.width !== WANT_WIDTH || size.height !== WANT_HEIGHT) {
    throw new Error(`poster is ${size.width}x${size.height}, expected ${WANT_WIDTH}x${WANT_HEIGHT}`);
  }
  const bytes = statSync(source).size;
  if (bytes > SIZE_LIMIT) {
    throw new Error(`poster is ${bytes} bytes, over the 1 MiB limit`);
  }
  const outDir = process.argv[2] || process.env.MAKEFUN_OUTPUT_DIR || "out";
  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, POSTER);
  copyFileSync(source, dest);
  chmodSync(dest, 0o644);
  const before = sha256(source);
  const after = sha256(dest);
  if (before !== after) {
    throw new Error("copy digest mismatch: output is not identical");
  }
  console.log(`entry.png ${size.width}x${size.height} (${bytes} bytes) -> ${dest} sha256 ${after}`);
}

try {
  main();
} catch (err) {
  console.error(`main.ts: ${err.message}`);
  process.exit(1);
}
