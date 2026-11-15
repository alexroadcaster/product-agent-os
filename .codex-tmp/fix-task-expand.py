from pathlib import Path
p=Path('apps/web/src/features/tasks/TaskManager.tsx');s=p.read_text(encoding='utf-8')
s=s.replace('aria-label=<span aria-hidden="true">{expanded?\'↙\':\'↗\'}</span>',"aria-label={expanded?(locale==='ru'?'Свернуть':'Collapse'):(locale==='ru'?'Открыть в окне':'Open in overlay')}",1)
s=s.replace("onClick={()=>setExpanded(value=>!value)}>{expanded?(locale==='ru'?'Свернуть':'Collapse'):(locale==='ru'?'Открыть в окне':'Open in overlay')}","onClick={()=>setExpanded(value=>!value)}><span aria-hidden=\"true\">{expanded?'↙':'↗'}</span>",1)
p.write_text(s,encoding='utf-8')
