// Tiny test for signText.js. Run: node test.js
'use strict';
const assert = require('assert');
const s = require('./signText.js');
const vectors = require('./vectors.json');

let n = 0;
const t = (name, fn) => { fn(); n++; console.log('ok', n, name); };

// Real signs from GR-V1.03 levels: decode, and re-encode back to the exact bytes.
for (const v of vectors) {
  const bytes = Buffer.from(v.hex, 'hex');
  t(`${v.level} (${v.x},${v.y}) decodes`, () => assert.strictEqual(s.decodeSignText(bytes), v.text));
  t(`${v.level} (${v.x},${v.y}) round-trips`, () =>
    assert.deepStrictEqual(Buffer.from(s.encodeSignText(s.decodeSignText(bytes, { raw: true }))), bytes));
}

t('alphabet has 97 slots', () => assert.strictEqual(s.ALPHABET.length, 97));
t('space is code 89 (byte 0x79)', () => assert.deepStrictEqual(s.encodeSignText(' '), [0x79]));
t('newline is code 96 (byte 0x80)', () => assert.deepStrictEqual(s.encodeSignText('\n'), [0x80]));
t('"v*eUWf" is #K(13)', () => assert.strictEqual(s.decodeSignText('v*eUWf', { raw: true }), '#K(13)'));
t('CRLF break decodes to \\n', () => assert.strictEqual(s.decodeSignText(' v*eUWf\x80!'), 'A\nB'));
t('glyphs round-trip', () => {
  const txt = '#A#B#X#Y#u#d#l#r#h#x#y#z#4#.';
  assert.strictEqual(s.decodeSignText(s.encodeSignText(txt)), txt);
});
t('literal # survives', () => assert.strictEqual(s.decodeSignText(s.encodeSignText('a#b')), 'a#b'));
t('char outside alphabet uses #K(n)', () => {
  assert.strictEqual(s.decodeSignText(s.encodeSignText('50%'), { raw: true }), '50#K(37)');
  assert.strictEqual(s.decodeSignText(s.encodeSignText('50%')), '50%');
});
t('record encode/decode', () => {
  const rec = s.encodeSignRecord(30, 51, 'Welcome\nTo WaterWorld.');
  assert.deepStrictEqual(s.decodeSignRecord(rec), { x: 30, y: 51, text: 'Welcome\nTo WaterWorld.' });
});
t('control bytes (<32) are skipped', () => assert.strictEqual(s.decodeSignText('\x01 '), 'A'));

console.log(`\n${n} passed`);
