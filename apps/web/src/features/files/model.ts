/** Reader navigation keeps a bounded DOM even for a permitted 512KiB text file. */
export function fileLineWindow(content:string,requested:number,size=80){
 const lines=content.split(/\r?\n/),line=Math.min(lines.length,Math.max(1,Number.isSafeInteger(requested)?requested:1));
 const first=Math.max(1,Math.min(line,Math.max(1,lines.length-size+1))),rows=lines.slice(first-1,first-1+size).map((text,index)=>({line:first+index,text}));
 return {line,first,last:first+rows.length-1,total:lines.length,rows};
}
export const fileDirectory=(path:string)=>path.split('/').slice(0,-1).join('/');
export function projectFileAnchor(projectId:string,path:string,line=1){const bounded=Number.isSafeInteger(line)&&line>=1&&line<=1000000?line:1;return '#'+new URLSearchParams({project:projectId,file:path,line:String(bounded)}).toString();}
