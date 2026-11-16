import {test} from 'node:test';
import assert from 'node:assert/strict';
import {fileLineWindow,fileDirectory,projectFileAnchor} from '../../apps/web/src/features/files/model.ts';
test('source-line navigation clamps missing anchors and renders a bounded text window with exact CRLF lines',()=>{
 const content=Array.from({length:1000},(_v,i)=>'line '+(i+1)).join('\r\n');
 const window=fileLineWindow(content,500);assert.equal(window.rows.length,80);assert.deepEqual(window.rows[0],{line:500,text:'line 500'});assert.equal(window.last,579);assert.equal(window.total,1000);
 assert.equal(fileLineWindow(content,2000).line,1000);assert.equal(fileLineWindow(content,NaN).line,1);assert.equal(fileLineWindow('',1).rows[0].text,'');
});
test('file navigation anchors preserve Unicode, spaces and project identity without embedding source bytes',()=>{
 assert.equal(fileDirectory('данные/мой файл.ts'),'данные');const anchor=projectFileAnchor('project-b','данные/мой файл.ts',42),params=new URLSearchParams(anchor.slice(1));
 assert.equal(params.get('project'),'project-b');assert.equal(params.get('file'),'данные/мой файл.ts');assert.equal(params.get('line'),'42');
 assert.equal(new URLSearchParams(projectFileAnchor('p','file',Infinity).slice(1)).get('line'),'1');
});
