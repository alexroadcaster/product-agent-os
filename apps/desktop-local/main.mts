import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {packDistribution,verifyDistribution,installDistribution,selectInstallation,readSelection,backupProfile,restoreProfile,startSelection} from './distribution.mts';
/** Explicit local CLI; importing creates no server, GUI, provider or installation. */
export async function desktopCommand(args:string[]){
 const [command,...rest]=args;if(rest.length%2!==0)throw Error('ARGUMENTS_INVALID');const flags:Record<string,string>={};for(let i=0;i<rest.length;i+=2){if(!rest[i].startsWith('--')||flags[rest[i]]!==undefined)throw Error('ARGUMENTS_INVALID');flags[rest[i]]=rest[i+1];}
 const get=(name:string)=>{const v=flags['--'+name];if(!v)throw Error('ARGUMENT_REQUIRED_'+name);return v;};const allowed:Record<string,string[]>={pack:['source','output'],verify:['package','expected-id'],install:['package','destination','expected-id'],select:['state','install','expected-id','profile','expected-selection'],status:['state'],start:['state'],backup:['install','expected-id','profile','output'],restore:['install','expected-id','backup','profile']};if(!allowed[command]||Object.keys(flags).some(k=>!allowed[command].includes(k.slice(2))))throw Error('ARGUMENTS_INVALID');
 if(command==='pack')return packDistribution(get('source'),get('output'));
 if(command==='verify')return verifyDistribution(get('package'),get('expected-id'));
 if(command==='install')return installDistribution(get('package'),get('destination'),get('expected-id'));
 if(command==='select')return selectInstallation(get('state'),get('install'),get('expected-id'),get('profile'),get('expected-selection')==='none'?null:get('expected-selection'));
 if(command==='status')return readSelection(get('state'));
 if(command==='start')return startSelection(get('state'));
 if(command==='backup')return backupProfile(get('install'),get('expected-id'),get('profile'),get('output'));
 return restoreProfile(get('install'),get('expected-id'),get('backup'),get('profile'));
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))try{const result=await desktopCommand(process.argv.slice(2));console.log(JSON.stringify(result));if(result&&typeof result==='object'&&'status' in result&&result.status!=='opened')process.exitCode=1;}catch(e){console.error(JSON.stringify({error:(e as {code?:string}).code??(e as Error).message}));process.exitCode=1;}
