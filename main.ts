// news-image-20261122 entry (Node 22, standard library only).
//
// The entry is a newspaper front page, entry.png beside this file, drawn
// by compose.py from a generated COP31 summit illustration plus the day's
// verified headlines. This program copies it to the output directory
// after checking it is a whole PNG inside the competition's limits
// (at most 1 MiB, at most 1024 by 1024 pixels), so the bytes the judge
// sees are exactly the bytes in the repository.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

const bytes = readFileSync(source);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG (bad magic bytes)');
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
// PNG header: width at bytes 16-19, height at bytes 20-23 (big-endian).
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(target, bytes);
console.log(`wrote ${target}: ${width}x${height} PNG, ${bytes.length} bytes`);
