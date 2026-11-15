from pathlib import Path
p=Path('apps/web/src/features/team/TeamManager.tsx')
s=p.read_text(encoding='utf-8').replace('(catalog?.assets??[]).map(a=>[a.id,a.name])','(catalog?.assets??[]).filter(a=>a.kind===\'agent\'&&!a.deleted).map(a=>[a.id,a.name])')
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/features/workflows/WorkflowManager.tsx')
s=p.read_text(encoding='utf-8').replace(" const oldStates=", " useEffect(()=>{setStateIndex(i=>Math.min(i,Math.max(0,draft.states.length-1)));setTransitionIndex(i=>Math.min(i,Math.max(0,draft.transitions.length-1)));},[draft.states.length,draft.transitions.length]);\n const oldStates=")
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/features/tasks/TaskManager.tsx')
s=p.read_text(encoding='utf-8').replace('defaultView,readView,','defaultView,hierarchyStats,readView,')
s=s.replace(" const hidden=snapshot.tasks.filter", " const totals=task?hierarchyStats(snapshot.tasks,task.id,snapshot.workflows):undefined;\n const hidden=snapshot.tasks.filter")
old="<dl><dt>{t('priority')}</dt><dd>{priorityText(locale,String(task.data?.priority??''))}</dd><dt>{t('estimate')}</dt><dd>{durationText(task.data?.estimateSeconds)}</dd><dt>{t('dueDate')}</dt><dd>{String(task.data?.dueDate??'—')}</dd></dl>"
new="""<dl><dt>{locale==='ru'?'Проект':'Project'}</dt><dd>{projectName??projectId}</dd><dt>ID / {locale==='ru'?'ключ':'key'}</dt><dd>{task.publicKey??task.id}</dd><dt>Revision</dt><dd>{task.revision}</dd><dt>{t('creator')}</dt><dd>{data?.creator.displayName??data?.creator.actorId??t('unknown')} · {data?.creator.kind}</dd><dt>{t('initiator')}</dt><dd>{data?.initiatedBy??'—'}</dd><dt>{t('created')}</dt><dd>{data?.createdAt??t('unknown')}</dd><dt>{locale==='ru'?'Начало actual':'Actual start'}</dt><dd>{data?.actual.startedAt??t('notStarted')}</dd><dt>{locale==='ru'?'Окончание':'Actual end'}</dt><dd>{data?.actual.endedAt??t('unknown')}</dd><dt>{t('actual')}</dt><dd>{durationText(data?.actual.durationSeconds)}</dd><dt>{t('timezone')}</dt><dd>{data?.timezone??'—'}</dd><dt>{t('rollup')}</dt><dd>{totals?.done} / {totals?.descendants}</dd><dt>{statusText(locale,'cancelled')}</dt><dd>{totals?.cancelled}</dd><dt>{t('ownEstimate')}</dt><dd>{durationText(totals?.ownEstimateSeconds)}</dd><dt>{locale==='ru'?'Сумма оценок':'Total estimate'}</dt><dd>{durationText(totals?.estimateSeconds)}{totals?.unknownEstimates?` + ${totals.unknownEstimates} ${t('unknown')}`:''}</dd></dl>"""
assert old in s
s=s.replace(old,new)
s=s.replace("<span className=\"badge\">{typeText(String(task.data?.type))}</span>    <label>","<span className=\"badge\">{typeText(String(task.data?.type))}</span><span className=\"badge\">{stateName(task,snapshot.workflows)??statusText(locale,task.status??'')}</span><label>")
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/design/parity.css')
s=p.read_text(encoding='utf-8')+'\n/* Keep SVG paint and computed color consistent for contrast inspection. */\n.ui-mermaid text,.ui-mermaid tspan{color:var(--ink)!important;fill:var(--ink)!important}\n.task-detail-status>label{white-space:nowrap;flex:none}.task-detail-status{flex-wrap:wrap}\n.task-detail-overlay .task-context{background:var(--surface)}.task-context dl{grid-template-columns:90px minmax(0,1fr);gap:14px 12px}.task-context dd{margin:0;overflow-wrap:anywhere}\n'
p.write_text(s,encoding='utf-8')
