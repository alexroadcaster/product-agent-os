import {build} from 'esbuild';
import {readFile,writeFile,mkdir,readdir,copyFile,stat} from 'node:fs/promises';
import {dirname,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=dirname(fileURLToPath(import.meta.url));
await mkdir(join(root,'vendor'),{recursive:true});
const result=await build({entryPoints:[join(root,'runtime-entry.js')],bundle:true,write:false,format:'iife',platform:'browser',target:'es2024',minify:true,legalComments:'inline'});
const tiny=await readFile(join(root,'node_modules/@mermaid-js/tiny/dist/mermaid.tiny.js'),'utf8');
const runtime=tiny+'\n;\n'+result.outputFiles[0].text;
await writeFile(join(root,'vendor/runtime.js'),runtime);
// Retain installed package license files, including transitive libraries.
const notices=[];
for(const entry of await readdir(join(root,'node_modules'),{withFileTypes:true})){
 if(!entry.isDirectory()||entry.name.startsWith('.'))continue;
 const names=entry.name.startsWith('@')?(await readdir(join(root,'node_modules',entry.name))).map(name=>entry.name+'/'+name):[entry.name];
 for(const name of names){
  const dir=join(root,'node_modules',name);let pkg;try{pkg=JSON.parse(await readFile(join(dir,'package.json'),'utf8'));}catch{continue;}
  notices.push(`\n## ${pkg.name} ${pkg.version}\nLicense: ${pkg.license??'see package'}\n`);
  for(const f of await readdir(dir))if(/^(license|copying|notice)(\.|$)/i.test(f)&&(await stat(join(dir,f))).isFile())notices.push(await readFile(join(dir,f),'utf8'));
 }
}
await writeFile(join(root,'vendor/THIRD-PARTY-NOTICES.txt'),notices.join('\n'));
const receipt={command:'npm run build',runtimeBytes:Buffer.byteLength(runtime),sha256:createHash('sha256').update(runtime).digest('hex'),dependencies:JSON.parse(await readFile(join(root,'package.json'),'utf8')).dependencies,networkAtRuntime:false};
await writeFile(join(root,'build-report.json'),JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify(receipt,null,2));
