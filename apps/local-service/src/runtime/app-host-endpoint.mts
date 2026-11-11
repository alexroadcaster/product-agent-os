import {lstat,realpath} from 'node:fs/promises';
import {isAbsolute,join,resolve} from 'node:path';

export type AppHostEndpointInspection=Readonly<{
 status:'unavailable'|'unverified';
 reason:'app_host_endpoint_missing'|'app_host_endpoint_invalid'|'app_host_endpoint_inspection_failed'|'app_host_endpoint_unverified';
 transport:'websocket_over_stdio_proxy';
}>;
const result=(reason:AppHostEndpointInspection['reason']):AppHostEndpointInspection=>({
 status:reason==='app_host_endpoint_unverified'?'unverified':'unavailable',reason,transport:'websocket_over_stdio_proxy',
});
const identity=(path:string)=>process.platform==='win32'?resolve(path).toLowerCase():resolve(path);

/** Metadata-only snapshot of the documented daemon endpoint; no profile reads, socket connect or startup.
 * A Windows AF_UNIX endpoint may look like a regular file. Its existence never proves a live App host.
 * Protocol source: openai/codex rust-v0.167.0, cli/src/main.rs (Proxy), stdio-to-uds/src/lib.rs,
 * app-server-transport/src/transport/unix_socket.rs: the proxy relays raw WebSocket bytes, not JSONL.
 */
export async function inspectAppHostEndpoint(options:Readonly<{codexHome:string}>):Promise<AppHostEndpointInspection> {
 if(typeof options.codexHome!=='string'||!isAbsolute(options.codexHome))return result('app_host_endpoint_invalid');
 const home=resolve(options.codexHome),parent=join(home,'app-server-control');
 try {
  for(const directory of [home,parent]) {
   const before=await lstat(directory);
   if(!before.isDirectory()||before.isSymbolicLink()||identity(await realpath(directory))!==identity(directory))return result('app_host_endpoint_invalid');
   const after=await lstat(directory);
   if(after.isSymbolicLink()||after.dev!==before.dev||after.ino!==before.ino)return result('app_host_endpoint_invalid');
  }
  const endpoint=await lstat(join(parent,'app-server-control.sock'));
  if(endpoint.isSymbolicLink()||endpoint.isDirectory()||endpoint.nlink>1||(!endpoint.isFile()&&!endpoint.isSocket()))return result('app_host_endpoint_invalid');
  return result('app_host_endpoint_unverified');
 } catch(error) {
  const code=(error as {code?:string}).code;
  if(code==='ENOENT')return result('app_host_endpoint_missing');
  if(code==='ENOTDIR'||code==='EINVAL')return result('app_host_endpoint_invalid');
  return result('app_host_endpoint_inspection_failed');
 }
}

/** Supply a fresh inspection from the same failed connection attempt, never a cached earlier snapshot.
 * WSA10050 alone does not establish either a missing endpoint or a general network failure.
 */
export function classifyAppHostConnectFailure(code:unknown,inspection:AppHostEndpointInspection):'app_host_endpoint_missing'|'app_host_connect_failed' {
 if(code===10050&&inspection.status==='unavailable'&&inspection.reason==='app_host_endpoint_missing')return 'app_host_endpoint_missing';
 return 'app_host_connect_failed';
}
