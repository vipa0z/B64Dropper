const fs = require("fs");
const path = require("path");

// Array of base64 chunks
const chunks = [{ chunks }];

// Join chunks and decode from base64
const b64 = chunks.join("");
const payload = Buffer.from(b64, "base64");

// Resolve output path and write file
const dest = path.resolve("{filename}");
fs.writeFileSync(dest, payload);

console.log("Wrote " + payload.length + " bytes to " + dest);
