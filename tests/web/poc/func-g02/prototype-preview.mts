import {createServer} from 'node:http';
import {readFile,realpath,stat} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {pathToFileURL} from 'node:url';

/** Only generated synthetic files; no proxy, mutation or network clients. */
export async function createPreview(directory=resolve('.tmp/func-g02/prototype-dist')){
 const root=await realpath(directory);await stat(resolve(root,'data.json'));
 const server=createServer(async(req,res)=>{
  if(!['GET','HEAD'].includes(req.method??'')){res.writeHead(405);res.end();return;}
  try{
   const pathname=decodeURIComponent(new URL(req.url??'/','http://127.0.0.1').pathname);
   const candidate=resolve(root,'.'+(pathname==='/'?'/index.html':pathname));
   if(!candidate.startsWith(root+sep))throw Error('OUTSIDE_BUNDLE');
   const file=await realpath(candidate);
   if(!file.startsWith(root+sep)||!(await stat(file)).isFile())throw Error('OUTSIDE_BUNDLE');
   const bytes=await readFile(file);
   res.setHeader('Content-Type',({'.js':'application/javascript','.html':'text/html; charset=utf-8','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'} as Record<string,string>)[extname(file)]??'application/octet-stream');
   res.setHeader('Cache-Control','no-store');
   res.setHeader('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'");
   res.end(req.method==='HEAD'?undefined:bytes);
  }catch{res.writeHead(404);res.end('Not found');}
 });
 await new Promise<void>((done,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',()=>done());});
 return {server,url:'http://127.0.0.1:'+(server.address() as {port:number}).port};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 const {server,url}=await createPreview();console.log(`Synthetic FUNC-G02 preview: ${url}\nCtrl+C closes this local preview.`);
 const close=()=>server.close(()=>process.exit(0));process.once('SIGINT',close);process.once('SIGTERM',close);
}
