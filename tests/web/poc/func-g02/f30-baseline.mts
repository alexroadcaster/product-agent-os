import {readFile} from 'node:fs/promises';
import {Worker} from 'node:worker_threads';
const files=JSON.parse(await readFile(process.argv[2],'utf8'));
const worker=new Worker(new URL('../../../../apps/local-service/src/code-index/parser-worker.mts',import.meta.url),{workerData:{files}});
worker.once('message',value=>{console.log(JSON.stringify(value));void worker.terminate();});
worker.once('error',error=>{console.error(String(error));process.exitCode=1;});
