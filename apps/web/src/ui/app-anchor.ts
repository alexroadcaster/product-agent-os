type AppAnchor =
  | {section:'files';projectId:string;path:string;line:number}
  | {section:'database';projectId:string;table:string;tab:'schema'|'changes'|'usages'}
  | {section:'sessions';projectId:string;sessionId:string;messageId:string};

/** Resolve a fragment only within projects known to the current App session. */
export function parseAppAnchor(hash:string,projects:readonly {id:string}[]):AppAnchor|null{
  if(!hash.startsWith('#'))return null;
  const query=new URLSearchParams(hash.slice(1));
  const projectId=query.get('project');
  if(!projectId||!projects.some(project=>project.id===projectId))return null;

  const file=query.get('file');
  if(file&&file.length<=2048&&!/[\\\0\r\n:]/.test(file)){
    const requested=Number(query.get('line')??1);
    const line=Number.isSafeInteger(requested)&&requested>=1&&requested<=1000000?requested:1;
    return {section:'files',projectId,path:file,line};
  }

  const database=query.get('database');
  if(database!==null&&database.length<=256&&!/[\0\r\n]/.test(database)){
    const requested=query.get('dbtab');
    const tab=requested==='changes'||requested==='usages'?requested:'schema';
    return {section:'database',projectId,table:database,tab};
  }

  const sessionId=query.get('session'),messageId=query.get('message');
  if(!sessionId||!messageId||[sessionId,messageId].some(id=>id.length>200||/[\\\0\r\n]/.test(id)))return null;
  return {section:'sessions',projectId,sessionId,messageId};
}
