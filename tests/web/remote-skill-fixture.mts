import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
export const revision='d420d13051bffe4543ed39e30fa46b87148e47dd';
const gitHash=(value:string)=>execFileSync('git',['hash-object','--stdin'],{input:value,encoding:'utf8'}).trim();
export function fixtureFetch(withMetadata=false){
 const bodies=new Map<string,string>(),put=(text:string)=>{const sha=gitHash(text);bodies.set(sha,text);return sha;};
 const manifest=put(JSON.stringify({name:'superpowers',version:'6.3.0',skills:'./skills/',license:'MIT',hooks:{}})),license=put('MIT License\nCopyright Synthetic Fixture\nPermission is hereby granted, free of charge, to any person obtaining a copy.\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY.\n');
 const skill=put('---\nname: verification-before-completion\ndescription: Synthetic verification fixture\n---\nRead [guide](guide.md).\n'),resource=put('# Synthetic guide\n');
 const metadata=put('interface:\n  display_name: Synthetic skill\n  short_description: Read-only metadata fixture\n');
 const roots=['1','2','3'].map(x=>x.repeat(40)),calls:string[]=[];
 const tree=(sha:string,entries:any[])=>({sha,truncated:false,tree:entries}),entry=(path:string,type:string,sha:string,mode=type==='tree'?'040000':'100644')=>({path,type,sha,mode,...(bodies.has(sha)?{size:Buffer.byteLength(bodies.get(sha)!)}:{})});
 const data=new Map<string,unknown>([
  [`git/commits/${revision}`,{sha:revision,tree:{sha:roots[0]}}],
  [`git/trees/${roots[0]}`,tree(roots[0],[entry('plugins','tree',roots[1])])],
  [`git/trees/${roots[1]}`,tree(roots[1],[entry('superpowers','tree',roots[2])])],
  [`git/trees/${roots[2]}?recursive=1`,tree(roots[2],[entry('.codex-plugin/plugin.json','blob',manifest),entry('LICENSE','blob',license),entry('skills/verification-before-completion/SKILL.md','blob',skill),entry('skills/verification-before-completion/guide.md','blob',resource),...(withMetadata?[entry('skills/verification-before-completion/agents/openai.yaml','blob',metadata)]:[])])]
 ]);
 const fetcher:typeof fetch=async(url,init)=>{const text=String(url);calls.push(text);assert.equal(init?.credentials,'omit');assert.equal(new Headers(init?.headers).has('authorization'),false);const path=text.replace('https://api.github.com/repos/openai/plugins/','');let value=data.get(path);if(path.startsWith('git/blobs/')){const sha=path.slice(10),body=bodies.get(sha);if(body!==undefined)value={sha,encoding:'base64',size:Buffer.byteLength(body),content:Buffer.from(body).toString('base64')};}assert.ok(value,'unexpected fixed-source request '+path);return new Response(JSON.stringify(value),{headers:{'content-type':'application/json'}});};
 return {fetcher,calls,data,bodies};
}
