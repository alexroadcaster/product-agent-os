/* Deterministic synthetic receipts. A run belongs to one task, project and agent; cache tokens are a subset of input. */
(() => {
  const projects = [
    {id:'demo-ui',name:'Product Workspace',description:'Рабочий интерфейс и задачи',module:'ui'},
    {id:'demo-docs',name:'Knowledge Studio',description:'Документы и источники',module:'knowledge'},
    {id:'demo-data',name:'Data Pipeline',description:'Контракты и обработка данных',module:'data'}
  ];
  const agents=[{id:'demo-builder',name:'Builder',role:'Реализация',color:'blue'},{id:'demo-reviewer',name:'Reviewer',role:'Проверка',color:'violet'},{id:'demo-docs',name:'Docs',role:'Документация',color:'sage'}];
  const tasks=[
    ['DEMO-104','Обновить навигацию проекта','demo-ui','in_progress','demo-builder',3600],
    ['DEMO-105','Согласовать состояния подключения','demo-ui','in_progress','demo-builder',1800],
    ['DEMO-106','Проверить доступность форм','demo-ui','verification','demo-reviewer',2400],
    ['DEMO-107','Проверить перенос длинных названий','demo-ui','verification','demo-reviewer',1200],
    ['DEMO-108','Подготовить каталог компонентов','demo-ui','ready','demo-docs',1800],
    ['DEMO-109','Уточнить критерии задачи','demo-ui','ready','demo-docs',900],
    ['DEMO-110','Собрать исходные материалы','demo-ui','done','demo-docs',600],
    ['DOC-201','Проверить реестр источников','demo-docs','done','demo-docs',900],
    ['DOC-202','Обновить руководство проекта','demo-docs','in_progress','demo-reviewer',1200],
    ['DOC-203','Согласовать оглавление','demo-docs','done','demo-docs',600],
    ['DATA-301','Проверить контракты импорта','demo-data','in_progress','demo-builder',2400],
    ['DATA-302','Проверить обратный экспорт','demo-data','ready','demo-builder',1800]
  ].map(([id,title,projectId,status,agentId,estimateSeconds])=>({id,title,projectId,status,agentId,estimateSeconds}));
  const raw=[
    ['run-01','DEMO-104','demo-reviewer',12000,3400,2000,28500,1800,[5,5,2],'completed'],
    ['run-02','DEMO-104','demo-builder',18000,5200,4000,46900,2400,[6,8,4],'running'],
    ['run-03','DEMO-105','demo-builder',8000,1900,1000,15400,1600,[3,4,2],'completed'],
    ['run-04','DEMO-106','demo-reviewer',14000,3200,3200,31600,1500,[4,8,2],'completed'],
    ['run-05','DEMO-108','demo-docs',9000,2100,2000,19000,1800,[2,7,2],'completed'],
    ['run-06','DOC-201','demo-docs',7000,1200,1000,11500,900,[1,5,1],'completed'],
    ['run-07','DOC-202','demo-reviewer',6000,1200,600,10800,800,[2,3,1],'running'],
    ['run-08','DATA-301','demo-builder',10000,2600,1800,21800,2000,[3,5,2],'running'],
    ['run-09','DEMO-107','demo-reviewer',null,null,null,null,null,null,'interrupted'],
    ['run-10','DOC-203','demo-docs',0,0,0,0,0,[0,0,0],'completed']
  ];
  const runs=raw.map(([id,taskId,agentId,inputTokens,outputTokens,cachedInputTokens,costMicros,durationSeconds,tools,status],index)=>({
    id,taskId,projectId:tasks.find(t=>t.id===taskId).projectId,agentId,sessionId:`session-${id}`,
    inputTokens,outputTokens,cachedInputTokens,costMicros,durationSeconds,tools:tools?{shell:tools[0],read:tools[1],edit:tools[2]}:null,
    toolUse:tools?tools.reduce((sum,v)=>sum+v,0):null,status,
    totalTokens:inputTokens===null||outputTokens===null?null:inputTokens+outputTokens,
    provenance:'synthetic_receipt',currency:'USD',profileVersion:'v2',day:['2026-11-11','2026-11-13','2026-11-11','2026-11-12','2026-11-12','2026-11-11','2026-11-12','2026-11-13','2026-11-13','2026-11-13'][index]
  }));
  const queue=[{id:'queue-01',taskId:'DEMO-105',projectId:'demo-ui',agentId:'demo-builder',state:'На паузе',reason:'Очередь новых запусков на паузе'},
    {id:'queue-02',taskId:'DATA-302',projectId:'demo-data',agentId:'demo-builder',state:'Ожидает',reason:'Workspace занят текущим writer'}];
  function selectedRuns(scope={}){return runs.filter(r=>Object.entries(scope).every(([key,value])=>!value||r[key]===value));}
  function summarize(scope={}){
    const selected=selectedRuns(scope);const sum=key=>{const known=selected.filter(r=>r[key]!==null);return{value:known.reduce((s,r)=>s+r[key],0),known:known.length,unknown:selected.length-known.length,available:known.length>0};};
    return{runCount:selected.length,activeRuns:selected.filter(r=>r.status==='running').length,totalTokens:sum('totalTokens'),inputTokens:sum('inputTokens'),outputTokens:sum('outputTokens'),cachedInputTokens:sum('cachedInputTokens'),costMicros:sum('costMicros'),durationSeconds:sum('durationSeconds'),toolUse:sum('toolUse'),runs:selected};
  }
  function byScope(key,items,parent={}){return items.map(item=>({id:item.id,label:item.name||item.title,...summarize({...parent,[key]:item.id})}));}
  function progress(projectId){const selected=tasks.filter(t=>!projectId||t.projectId===projectId);const done=selected.filter(t=>t.status==='done').length;return{total:selected.length,done,remaining:selected.length-done,percent:selected.length?Math.round(done/selected.length*100):0};}
  window.DesignFixtures={projects,agents,tasks,runs,queue,selectedRuns,summarize,byScope,progress,
    invariant:{leaf:'Each receipt is counted once per scope',tokenTotal:'input + output; cached input is already included in input',cost:'Stored synthetic USD receipt amount, no provider price inference',unknown:'null is unknown; explicit 0 is measured zero'}};
})();
