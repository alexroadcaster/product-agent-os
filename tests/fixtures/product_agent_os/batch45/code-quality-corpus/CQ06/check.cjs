const assert=require('node:assert/strict'); const fs=require('node:fs'); const path=require('node:path'); const p=path.resolve(process.argv[2]); const m=require(p); const source=fs.readFileSync(p,'utf8');
assert.equal(m.format('x','y'),'x:y'); assert(!source.includes('unusedCache'));
