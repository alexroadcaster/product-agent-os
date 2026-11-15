import test from 'node:test';
import assert from 'node:assert/strict';
import {diagramSource} from '../../apps/web/src/features/graph/diagram-source.ts';
test('Mermaid labels preserve special identifier characters through decimal entities without directives',()=>{
 const names=['$foo','#private','a"b','%%{init: {securityLevel: "loose"}}%%','<script>alert(1)</script>'];
 const source=diagramSource(names.map((name,i)=>({id:String(i),name})) as any,[]);
 assert.ok(source.includes('#36;foo'));assert.ok(source.includes('#35;private'));assert.ok(source.includes('a#34;b'));assert.ok(!source.includes('%%{'));assert.ok(!source.includes('<script>'));
 for(const name of names){const encoded=[...name].map(c=>/[\p{L}\p{N} _.-]/u.test(c)?c:'#'+c.codePointAt(0)+';').join('');assert.ok(source.includes(encoded));}
});
