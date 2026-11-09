const assert=require('node:assert/strict'); const fs=require('node:fs'); const path=require('node:path'); const p=path.resolve(process.argv[2]); const m=require(p); const source=fs.readFileSync(p,'utf8');
assert.equal(m.label('  one  two  '),'one  two'); assert.equal(m.label('   '),'');
