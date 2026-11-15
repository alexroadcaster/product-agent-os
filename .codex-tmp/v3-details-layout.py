from pathlib import Path
root=Path('apps/web/src')
p=root/'ui/App.tsx';s=p.read_text(encoding='utf-8')
s=s.replace("  const [inspectorPane,setInspectorPane]=useState('run');",'')
a=s.index('      <aside className="inspector"><div className="section-tabs inspector-tabs">');b=s.index('      </aside>',a)+len('      </aside>')
old=s[a:b];content=old[old.index('<div hidden={inspectorPane'):old.rindex('      </aside>')].replace('inspectorPane','pane')
aside='''      <aside className="inspector"><h3>{locale==='ru'?'Запуск и контекст':'Run and context'}</h3><div className="section-tabs inspector-tabs">{[['run',locale==='ru'?'Запуск и профиль':'Run and profile'],['checks',locale==='ru'?'Проверки':'Checks'],['question',locale==='ru'?'Вопрос':'Question']].map(([id,name])=><button key={id} data-inspector-pane={id} aria-pressed={pane===id} onClick={()=>setPane(id)}>{name}</button>)}</div><p className="quiet">{entity.id}</p><p>{t('connection')}: {connection?.verified?t('verified'):t('unverified')}</p><p>{t('approval')}: {snapshot?.pendingApprovals?.length??0}</p><p>{t('changes')}: {snapshot?.fileChanges?.length??0}</p></aside>'''
s=s[:a]+aside+s[b:]
s=s.replace('{pane === "chat" ? (',"{['run','checks','question'].includes(pane)?<section className=\"session-runtime-detail\">"+content+"</section>:pane === \"chat\" ? (",1)
s=s.replace("'settings','sessions'].includes(section)","'settings','sessions','projectMap'].includes(section)")
p.write_text(s,encoding='utf-8')
p=root/'features/graph/GraphExplorer.tsx';s=p.read_text(encoding='utf-8');s=s.replace("}</button>)}</div><p>{w('Статические", "}</button>)}</div><h1>{w('Карта проекта','Project map')}</h1><p>{w('Статические",1);p.write_text(s,encoding='utf-8')
p=root/'features/tasks/TaskManager.tsx';s=p.read_text(encoding='utf-8');s="import {UsageDashboard} from '../dashboard/Dashboard.tsx';\n"+s
s=s.replace('setDeleteAck(false);}', 'setDeleteAck(false);setDeleteOpen(false);}')
s=s.replace('<section className="task-usage" data-testid="task-usage"', '<section className="task-usage" data-testid="task-usage"')
needle="Usage is not measured: token, cost and tool call data is currently unavailable.'}</p></section>"
s=s.replace(needle,"Usage is not measured: token, cost and tool call data is currently unavailable.'}</p><button data-testid=\"task-usage-open\" onClick={()=>{setExpanded(false);setWorkspace('usage');}}>{locale==='ru'?'Аналитика расхода':'Usage analytics'}</button></section>")
s=s.replace("workspace==='settings'?(locale", "workspace==='usage'?(locale==='ru'?'Расход задачи':'Task usage'):workspace==='settings'?(locale")
s=s.replace('</div><div hidden={workspace!==\'settings\'}>', '</div><section hidden={workspace!==\'usage\'}><button onClick={()=>setWorkspace(\'tasks\')}>{locale===\'ru\'?\'Вернуться к задаче\':\'Back to task\'}</button><UsageDashboard locale={locale} scope={task?.publicKey??task?.id}/></section><div hidden={workspace!==\'settings\'}>')
p.write_text(s,encoding='utf-8')
p=root/'features/dashboard/Dashboard.tsx';s=p.read_text(encoding='utf-8')
s=s.replace('[work,setWork]=useState<Record<string,string[]>>()','[work,setWork]=useState<Record<string,string[]>>(),[assignedTasks,setAssignedTasks]=useState<StoredEntity[]>([])')
s=s.replace('if(!ignore)setWork(assignedWork(snapshot));','if(!ignore){setWork(assignedWork(snapshot));setAssignedTasks(snapshot.tasks);}')
anchor='<div className="dashboard-columns"><div className="dashboard-main"><section><h3>'
replacement='''{agentId?<><div className="usage-charts"><section className="panel"><h2>{w('Назначенные задачи','Assigned tasks')}</h2><ul className="records">{assignedTasks.filter(task=>work?.[agentId]?.includes(task.id)).map(task=><li key={task.id}><strong>{task.title}</strong><small>{task.publicKey??task.id} · {statusText(locale,task.status??'')}</small></li>)}</ul>{!work?.[agentId]?.length&&<p className="dashboard-empty">{w('Назначенных задач нет','No assigned tasks')}</p>}</section><section className="panel"><h2>{w('Tokens по проектам','Tokens by project')}</h2><p className="dashboard-empty">{w('Измерения расхода недоступны','Usage measurements unavailable')}</p></section></div><section className="panel"><h2>{w('Наблюдаемые запуски','Observed runs')}</h2><table className="dashboard-data-table"><thead><tr><th>Run</th><th>Tokens</th><th>tool_use</th></tr></thead><tbody>{agents.flatMap(agent=>agent.runIds.map(id=><tr key={id}><td>{id}</td><td>—</td><td>—</td></tr>))}</tbody></table>{!agents.some(agent=>agent.runIds.length)&&<p>{w('За период нет наблюдаемых запусков','No observed runs in this period')}</p>}</section></>:<div className="dashboard-columns"><div className="dashboard-main"><section><h3>'''
s=s.replace(anchor,replacement)
s=s.replace('<Usage locale={locale}/></aside></div></section>;','<Usage locale={locale}/></aside></div>}</section>;')
p.write_text(s,encoding='utf-8')
p=root/'ui/Sidebar.tsx';s=p.read_text(encoding='utf-8').replace('<div className="brand sidebar-label">Product-Agent OS','<div className="brand sidebar-label"><span className="brand-mark" aria-hidden="true">P</span>Product-Agent OS');p.write_text(s,encoding='utf-8')
p=root/'design/parity.css';p.write_text(p.read_text(encoding='utf-8')+'''
.session-runtime-detail{padding:24px 0;min-height:480px}.session-work-area>.inspector .inspector-tabs{flex-direction:column;align-items:stretch;border:0}.session-work-area>.inspector .inspector-tabs button{text-align:left;justify-content:flex-start}.session-runtime-detail>div>h2:first-child{margin-top:0}.session-runtime-detail dl{display:grid;grid-template-columns:180px minmax(0,1fr);gap:12px}
[data-testid=graph-explorer]>h1{margin:24px 0 16px}[data-testid=graph-explorer]>p{font-size:12px;margin:8px 0}[data-testid=graph-explorer]>.m2-actions{justify-content:flex-end;margin-top:-40px;margin-bottom:28px}[data-testid=graph-explorer]>.graph-module{max-width:300px}.brand-mark{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:7px;background:var(--accent);color:var(--on-accent,#fff);margin-right:8px;font-size:13px}.brand:has(.brand-mark){font-size:12px}.brand:has(.brand-mark)>span:not(.brand-mark){margin-left:32px}
''',encoding='utf-8')
