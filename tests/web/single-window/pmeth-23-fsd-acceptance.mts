import assert from 'node:assert/strict';
import {execFile} from 'node:child_process';
import {createHash} from 'node:crypto';
import {mkdir,mkdtemp,readFile,realpath,rm,writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {dirname,join,resolve} from 'node:path';
import {promisify} from 'node:util';

assert.deepEqual(process.argv.slice(2),['--synthetic-pilot']);
const exec=promisify(execFile);
const temp=await realpath(tmpdir());
const root=await mkdtemp(join(temp,'paos-pmeth23-fsd-'));
const workspace=join(root,'workspace');
const page='src/pages/orders.ts';
const retained='src/pages/help.ts';
const files={
 [page]:"export {show as route} from '../features/checkout/internal';\n",
 [retained]:"export {show as help} from '../features/checkout';\n",
 'src/features/checkout/index.ts':"export {show} from './internal';\n",
 'src/features/checkout/internal.ts':"export const show='fixture-orders';\n",
 'AGENTS.md':'# User-authored fixture\r\n',
};
const boundaries=[
 {root:'src/pages',layer:'pages',owner:'orders'},
 {root:'src/features/checkout',layer:'features',owner:'checkout',publicApi:'src/features/checkout/index.ts'},
];
const checks:string[]=[];
const sha=(bytes:Uint8Array)=>createHash('sha256').update(bytes).digest('hex');
const snapshot=async()=>Object.fromEntries(await Promise.all(Object.keys(files).map(async path=>[
 path,sha(await readFile(join(workspace,path))),
])));

async function architecture(path:string) {
 const request=join(root,'request.json');
 await writeFile(request,JSON.stringify({surface:'frontend',pages:[{path,owner:'orders'}],boundaries,
  changeFrequency:'frequent',migrationCost:'low',exceptions:[]}));
 const result=await exec(process.execPath,[resolve('tools/project-methodology.mts'),'architecture',workspace,request],
  {timeout:30_000});
 return JSON.parse(result.stdout);
}

async function buildAndCheck(name:string) {
 const out=join(root,name);
 await exec(process.execPath,[resolve('apps/web/node_modules/typescript/bin/tsc'),'--strict','--target','ES2022',
  '--module','commonjs','--rootDir',join(workspace,'src'),'--outDir',out,join(workspace,page),join(workspace,retained)],
  {timeout:30_000});
 const observed=await exec(process.execPath,['-e',`
  const assert = require('node:assert/strict');
  const [page, help, legacy] = process.argv.slice(1);
  assert.equal(require(page).route, 'fixture-orders');
  assert.equal(require(help).help, 'fixture-orders');
  assert.equal(require(legacy).show, 'fixture-orders');
  console.log('BEHAVIOR_AND_LEGACY_ENTRY_OK');
 `,join(out,'pages/orders.js'),join(out,'pages/help.js'),join(out,'features/checkout/internal.js')],{timeout:10_000});
 assert.equal(observed.stdout.trim(),'BEHAVIOR_AND_LEGACY_ENTRY_OK');
 return sha(await readFile(join(out,'pages/orders.js')));
}

let receipt:Record<string,unknown>={};
try {
 for(const [path,content] of Object.entries(files)){
  const destination=join(workspace,path);
  await mkdir(dirname(destination),{recursive:true});
  await writeFile(destination,content);
 }
 const original=await snapshot();
 const baseline=await architecture(page);
 assert.equal(baseline.coverage,'observed');
 assert.equal(baseline.recommendation,'gradual_fsd');
 assert.equal(baseline.migration.firstPage,page);
 assert.equal(baseline.migration.ownerDecisionRequired,true);
 assert.deepEqual(baseline.findings.map((row:{rule:string})=>row.rule),['private_entry']);
 assert.deepEqual(await snapshot(),original);
 checks.push('current F14 proposal selects one page and preserves target bytes');
 const buildBefore=await buildAndCheck('before');

 // The automatic recommendation is read-only. This is a reviewed fixture edit.
 const after=files[page].replace('/checkout/internal','/checkout');
 const plan={path:baseline.migration.firstPage,beforeHash:original[page],
  afterHash:sha(Buffer.from(after)),sourceRevision:baseline.revision};
 const stage=join(root,'reviewed-stage.json');
 const bytes=JSON.stringify(plan);
 await writeFile(stage,bytes);
 const approval=sha(Buffer.from(bytes));
 assert.equal(sha(await readFile(stage)),approval);
 assert.equal((await architecture(page)).revision,plan.sourceRevision);
 assert.equal((await snapshot())[page],plan.beforeHash);
 await writeFile(join(workspace,plan.path),after);
 const applied=await snapshot();
 assert.deepEqual(applied,{...original,[page]:plan.afterHash});
 checks.push('reviewed fixture edit changes only the selected page');
 const candidate=await architecture(page);
 assert.notEqual(candidate.revision,baseline.revision);
 assert.equal(candidate.coverage,'observed');
 assert.equal(candidate.recommendation,'retain_modular_boundaries');
 assert.deepEqual(candidate.findings,[]);
 assert.equal(candidate.migration,null);
 const unchangedModular=await architecture(retained);
 assert.equal(unchangedModular.recommendation,'retain_modular_boundaries');
 assert.deepEqual(await snapshot(),applied);
 checks.push('F14 reports no new boundary violations and retains a modular page');
 const buildAfter=await buildAndCheck('after');
 assert.notEqual(buildBefore,buildAfter);
 checks.push('both builds preserve page behavior and legacy entry point');

 assert.deepEqual(await snapshot(),applied);
 await writeFile(join(workspace,page),files[page]);
 assert.deepEqual(await snapshot(),original);
 assert.equal(await buildAndCheck('rollback'),buildBefore);
 assert.equal((await architecture(page)).recommendation,'gradual_fsd');
 checks.push('fixture rollback restores source and compiled output');
 receipt={fixtureApproval:approval,sourceBefore:baseline.revision,sourceAfter:candidate.revision,buildBefore,buildAfter};
} finally {
 assert.equal(dirname(await realpath(root)),temp);
 await rm(root,{recursive:true});
}
console.log(JSON.stringify({status:'passed',checks,fixtureCleaned:true,...receipt},null,2));
