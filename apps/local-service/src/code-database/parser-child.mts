import {performance} from 'node:perf_hooks';
import {startChildWatchdog} from '../process/child-watchdog.mts';
// Wait for the independent watchdog before importing any native parser or consuming target input.
const started=performance.now(),watchdog=await startChildWatchdog(Number(process.argv[2]??10000),Number(process.argv[3]??process.ppid));
try{
 const chunks:string[]=[];let inputBytes=0;process.stdin.setEncoding('utf8');for await(const chunk of process.stdin){inputBytes+=Buffer.byteLength(chunk);if(inputBytes>20*1024*1024)throw Error('CODE_DATABASE_WORKER_INPUT_LIMIT');chunks.push(String(chunk));}
 const {files,options}=JSON.parse(chunks.join(''));
 if(!Array.isArray(files)||files.length>1000||files.some((f:any)=>typeof f.relativePath!=='string'||typeof f.text!=='string'||Buffer.byteLength(f.text)>512*1024)||files.reduce((sum:number,f:any)=>sum+Buffer.byteLength(f.text),0)>8*1024*1024)throw Error('CODE_DATABASE_WORKER_INPUT_LIMIT');
 const {analyzeCodeDatabase}=await import('./analyzer.mts');const result={...analyzeCodeDatabase(files,{...options,maxLinks:1000}),metrics:{parserMaxRssKiB:process.resourceUsage().maxRSS,parserMilliseconds:performance.now()-started,scope:'owned_parser_child_process_before_stdout_including_watchdog_thread',jsHeapLimitMiB:128,watchdogHeapLimitMiB:16}};
 if(result.links.length>1000||Buffer.byteLength(JSON.stringify(result))>1024*1024)throw Error('CODE_DATABASE_WORKER_OUTPUT_LIMIT');process.stdout.write(JSON.stringify({result}));
}catch(error){process.stdout.write(JSON.stringify({error:String((error as Error).message).startsWith('CODE_DATABASE_')?(error as Error).message:'CODE_DATABASE_PARSER_UNAVAILABLE'}));}
finally{await watchdog.terminate();}
