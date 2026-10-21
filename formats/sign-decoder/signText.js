// signText.js: decode and encode Graal sign text. No dependencies.
//
// Sign text uses the same packed alphabet in level files (.graal / .zelda sign
// section) and on the wire (PLO_LEVELSIGN). Each text byte is a GCHAR, so
// byte - 32 is an index into ALPHABET below. Its slots marked '#' are glyph and
// escape codes.
//
// Sources:
//  - the alphabet string as it appears in the 2.05 client and in GServer-v2
//    (TLevelSign); the table is data, and this code is an original implementation;
//  - formats/sign-text.md in this repo;
//  - 11 real signs in GR-V1.03 levels (see vectors.json).
//
// Correction to sign-text.md: the file and network alphabets are the same.
//  - The "v*eUWf + high-bit byte" token is the escape #K(13) (a CR) followed by
//    code 96 (newline, byte 0x80). That is, a CRLF line break.
//  - "char + 89" only holds for letters. Space is code 89, byte 0x79.

'use strict';

const ALPHABET =
  'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789' +
  '!?-.,#>()#####"####\':/~&### <####;\n';

// Glyph codes: '#' + symbol <-> one or two alphabet codes.
const GLYPHS = {
  A: [91], B: [92], X: [93], Y: [94],
  u: [77], d: [78], l: [79], r: [80],
  h: [74, 75], x: [71], y: [72], z: [73],
  '4': [87, 88], '.': [67],
};
const HASH = 86;  // literal '#'
const K = 10;     // 'K'
const LPAREN = 69;
const RPAREN = 70;

// Reverse lookup for the decoder, two-code glyphs first.
const GLYPH_BY_CODES = Object.entries(GLYPHS)
  .sort((a, b) => b[1].length - a[1].length);

function toCodes(input) {
  // Accepts a Uint8Array/Buffer/array of bytes or a binary (latin-1) string.
  const bytes = typeof input === 'string'
    ? Array.from(input, (c) => c.charCodeAt(0) & 0xff)
    : Array.from(input);
  return bytes.map((b) => b - 32);
}

/**
 * Decode sign text (the payload after x and y).
 * opts.raw: keep "#K(n)" escapes instead of turning them into characters.
 * opts.keepCR: keep CR from #K(13); by default it is dropped (a newline follows).
 */
function decodeSignText(payload, opts = {}) {
  const codes = toCodes(payload);
  let out = '';
  for (let i = 0; i < codes.length; i++) {
    const c = codes[i];
    if (c < 0 || c >= ALPHABET.length) continue;  // control byte: not shown
    let glyph = null;
    for (const [sym, seq] of GLYPH_BY_CODES) {
      if (seq.every((v, k) => codes[i + k] === v)) { glyph = [sym, seq.length]; break; }
    }
    if (glyph) { out += '#' + glyph[0]; i += glyph[1] - 1; continue; }
    out += ALPHABET[c];
  }
  if (opts.raw) return out;
  return out.replace(/#K\((\d{1,3})\)/g, (m, n) => {
    const v = Number(n);
    if (v === 13 && !opts.keepCR) return '';
    return v < 256 ? String.fromCharCode(v) : m;
  });
}

/** Encode text to sign codes (array of bytes, each code + 32). */
function encodeSignText(text) {
  const codes = [];
  const emitEscape = (ch) => {
    codes.push(HASH, K, LPAREN);
    for (const d of String(ch.charCodeAt(0))) codes.push(ALPHABET.indexOf(d));
    codes.push(RPAREN);
  };
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === '#' && i + 1 < text.length && GLYPHS[text[i + 1]]) {
      codes.push(...GLYPHS[text[++i]]);
      continue;
    }
    if (ch === '#') { codes.push(HASH); continue; }
    if (ch === '\r') continue;
    const idx = ALPHABET.indexOf(ch);
    if (idx >= 0) codes.push(idx);
    else emitEscape(ch);
  }
  return codes.map((c) => c + 32);
}

/** Decode one sign record: GCHAR x, GCHAR y, then text. Works for a file line or a PLO_LEVELSIGN payload. */
function decodeSignRecord(line, opts) {
  const bytes = typeof line === 'string'
    ? Array.from(line, (c) => c.charCodeAt(0) & 0xff) : Array.from(line);
  return { x: bytes[0] - 32, y: bytes[1] - 32, text: decodeSignText(bytes.slice(2), opts) };
}

/**
 * Encode a sign record (no trailing "\n").
 * By default line breaks become CRLF (#K(13) then newline), as the editor wrote them.
 * A literal "#K(13)" in the text encodes to the same escape bytes.
 */
function encodeSignRecord(x, y, text, { crlf = true } = {}) {
  const t = crlf ? text.replace(/\r?\n/g, '#K(13)\n') : text;
  return [x + 32, y + 32, ...encodeSignText(t)];
}

const api = { ALPHABET, GLYPHS, decodeSignText, encodeSignText, decodeSignRecord, encodeSignRecord };
if (typeof module !== 'undefined' && module.exports) module.exports = api;
else if (typeof globalThis !== 'undefined') globalThis.signText = api;
