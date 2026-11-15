from pathlib import Path

def edit(path, fn):
    p=Path(path); old=p.read_text(encoding='utf-8'); new=fn(old)
    if old==new: raise RuntimeError('No change: '+path)
    p.write_text(new,encoding='utf-8')

def editor(s):
    s=s.replace('<div className="m2-fields">{textField(\'title\',\'title\')}', '<div className="m2-fields task-identity-fields">{textField(\'title\',\'title\')}')
    s=s.replace('  </div>\n  <label>{locale===\'ru\'?\'Процесс\':\'Workflow\'}','  <label>{locale===\'ru\'?\'Процесс\':\'Workflow\'}',1)
    s=s.replace('</select>}</label>\n  {textField', '</select>}</label></div>\n  {textField',1)
    s=s.replace('  <div className="m2-fields">\n   <label>{t(\'estimate\')}', '  <section className="task-planning"><h3>{locale===\'ru\'?\'Планирование\':\'Planning\'}</h3><div className="m2-fields">\n   <label>{t(\'estimate\')}')
    s=s.replace("snapshot.versions)}\n  </div>","snapshot.versions)}\n  </div></section>",1)
    s=s.replace("  <label>{t('risks')}","  <details className=\"task-risks\"><summary>{t('risks')}</summary><label>{t('risks')}",1)
    s=s.replace("{t('noneRisk')}</label>","{t('noneRisk')}</label></details>",1)
    s=s.replace('<details open><summary>', '<details><summary>',1)
    preview="  {entity&&<button type=\"button\" disabled={busy} onClick={()=>void run(true)}>{t('preview')}</button>}\n"
    s=s.replace(preview,'')
    s=s.replace('<div className="m2-actions"><button disabled={busy} className="primary">','<div className="m2-actions task-form-actions">{entity&&<button type="button" disabled={busy} onClick={()=>void run(true)}>{t(\'preview\')}</button>}<button disabled={busy} className="primary">',1)
    return s
edit('apps/web/src/features/tasks/Editor.tsx',editor)

def tasks(s):
    s="import {Icon} from '../../ui/Icon.tsx';\n"+s
    s=s.replace("const [deleteAck,setDeleteAck]", "const [workspace,setWorkspace]=useState('tasks');\n const [deleteAck,setDeleteAck]",1)
    s=s.replace("function open(id:string,nextTab:Word='summary',expand=false){", "function open(id:string,nextTab:Word='summary',expand=false){setWorkspace('tasks');",1)
    s=s.replace('<span className="mono">{item.publicKey??item.id}</span><strong>{item.title}</strong>', '<Icon name="tasks"/><span className="task-row-title"><strong>{item.title}</strong><span className="mono">{item.publicKey??item.id}</span></span>',1)
    s=s.replace('<small>{view.cardFields.includes(\'priority\')?', '<small className="task-row-meta">{view.cardFields.includes(\'priority\')?',1)
    s=s.replace('<small>{view.cardFields.includes(\'estimate\')?', '<small className="task-row-extra">{view.cardFields.includes(\'estimate\')?',1)
    s=s.replace('<div className="section-heading"><h2>{t(\'tasks\')} · {shown.length}/{snapshot.tasks.length}</h2>', '<div className="section-tabs task-workspace-tabs">{[["tasks",t("tasks")],["settings",locale===\'ru\'?\'Настройки задач\':\'Task settings\'],["archive",locale===\'ru\'?\'Полный архив\':\'Full archive\']].map(([id,name])=><button key={id} aria-pressed={workspace===id} onClick={()=>setWorkspace(id)}>{name}</button>)}</div><div className="section-heading task-page-title"><div><h1>{creating?t(\'create\'):workspace===\'tasks\'?t(\'tasks\'):workspace===\'settings\'?t(\'settings\'):(locale===\'ru\'?\'Полный архив\':\'Full archive\')}</h1><small>{shown.length} / {snapshot.tasks.length}</small></div>',1)
    s=s.replace('<button className="primary" disabled={busy} onClick={()=>{setCreating(true);', '<button className="primary" disabled={busy} onClick={()=>{setWorkspace(\'tasks\');setCreating(true);',1)
    s=s.replace("}}>{t('create')}</button></div></div>","}}><Icon name=\"tasks\"/>{t('create')}</button></div></div>",1)
    # Keep all fields mounted while switching local pages. Search remains directly accessible.
    start=s.index('  <details className="m2-filters"')
    end=s.index('  <div className="task-layout m2-task-layout">',start)
    controls=s[start:end]
    search='<label>{t(\'query\')}<input name="filter-query" value={view.query} onChange={e=>patchView({query:e.target.value})}/></label>'
    controls=controls.replace(search,'')
    tabsstart=controls.index('  <div className="tabs">')
    tabs=controls[tabsstart:].replace('className="tabs"','className="segmented"',1)
    controls=controls[:tabsstart]
    toolbar='<div className="task-toolbar">'+tabs+'<label className="task-search"><Icon name="search"/><input aria-label={t(\'query\')} placeholder={t(\'query\')} name="filter-query" value={view.query} onChange={e=>patchView({query:e.target.value})}/></label></div>'
    s=s[:start]+'  <div hidden={workspace!==\'tasks\'}><div hidden={creating}>'+toolbar+controls+'</div>\n'+s[end:]
    s=s.replace('<section className="panel task-list">','<section className={\'task-list \'+(creating?\'panel task-create\':\'\')} data-view={view.view}>',1)
    s=s.replace("{creating&&<><h3>{t('create')}</h3>","{creating&&<><button className=\"task-back\" onClick={()=>setCreating(false)}>{locale==='ru'?'← К списку задач':'← Back to tasks'}</button>",1)
    s=s.replace("   {!shown.length&&", "   <div hidden={creating}>{!shown.length&&",1)
    s=s.replace("  </section>\n  {task&&", "  </div></section>\n  {task&&",1)
    # Compact summary and full editor share the same task identity and draft mount.
    s=s.replace("{tab==='summary'&&<TaskEditor", "{tab==='summary'&&<><section className=\"task-compact-summary\" hidden={expanded}><p>{String(task.data?.summary??task.body??'')}</p><h3>{t('criteria')}</h3><ul>{((task.data?.acceptanceCriteria??[]) as string[]).map((c,i)=><li key={i}>{c}</li>)}</ul><dl className=\"task-summary-properties\"><dt>{t('priority')}</dt><dd>{priorityText(locale,String(task.data?.priority??''))}</dd><dt>{t('estimate')}</dt><dd>{durationText(task.data?.estimateSeconds)}</dd><dt>{t('dueDate')}</dt><dd>{String(task.data?.dueDate??'—')}</dd></dl><button onClick={()=>setExpanded(true)}>{locale==='ru'?'Открыть полностью':'Open full task'}</button></section><div hidden={!expanded}><TaskEditor",1)
    s=s.replace("previewDigest}:{})});}}/>}\n    {tab==='files'", "previewDigest}:{})});}}/></div></>}\n    {tab==='files'",1)
    s=s.replace("  <ManagerSettings snapshot={snapshot} command={command} locale={locale}/><FullArchive api={api} projectId={projectId} locale={locale}/>","  </div><div hidden={workspace!=='settings'}><ManagerSettings snapshot={snapshot} command={command} locale={locale}/></div><div hidden={workspace!=='archive'}><FullArchive api={api} projectId={projectId} locale={locale}/></div>",1)
    return s
edit('apps/web/src/features/tasks/TaskManager.tsx',tasks)

def app(s):
    s="import {Icon} from './Icon.tsx';\n"+s
    s=s.replace('<main id="main" tabIndex={-1}>','<main id="main" data-section={section} tabIndex={-1}>',1)
    s=s.replace('<div className="page-heading">','<div className="page-heading" hidden={ready&&section===\'tasks\'}>',1)
    s=s.replace('            <span className="quiet">\n              {ready ? t("local") : t("unverified")}\n            </span>','',1)
    s=s.replace('          <button onClick={() => void initialise()} disabled={busy}>','          <div className="top-actions"><button className="global-search" disabled={!ready} onClick={()=>setSection(\'search\')}><Icon name="search"/>{t(\'search\')}</button><span className="connection-chip"><span className={\'connection-dot \'+(connection?.verified?\'verified\':\'\')}/>{connection?.verified?t(\'verified\'):t(\'unverified\')}</span><button onClick={() => void initialise()} disabled={busy}>',1)
    s=s.replace('            {t("reload")}\n          </button>','            {t("reload")}\n          </button></div>',1)
    s=s.replace('        <form onSubmit={save}>','        <form className="appearance-form" onSubmit={save}>',1)
    s=s.replace('          <button disabled={busy} className="primary">\n            {uiLabel(preferences.locale, "preferences.save")}\n          </button>','          <div className="form-actions"><button type="button" disabled={busy} onClick={()=>setDraft(preferences)}>{preferences.locale===\'ru\'?\'Отменить\':\'Cancel\'}</button><button disabled={busy} className="primary">\n            {uiLabel(preferences.locale, "preferences.save")}\n          </button></div>',1)
    return s
edit('apps/web/src/ui/App.tsx',app)

def sidebar(s):
    s=s.replace("import {useEffect,useRef,useState}","import {Fragment,useEffect,useRef,useState}",1)
    s=s.replace('<label className="sidebar-project" hidden={!expanded}>{w(\'Проект\',\'Project\')}','<label className="sidebar-project" hidden={!expanded}><span className="project-avatar"><Icon name="portfolio"/></span><span className="project-picker-label">{w(\'Проект\',\'Project\')}</span>',1)
    s=s.replace('{items.map((item,i)=><button key={item.id}',"{items.map((item,i)=><Fragment key={item.id}>{([1,5,8,11].includes(i))&&<span className=\"nav-group-label sidebar-label\">{i===1?w('Работа','Work'):i===5?w('Знания','Knowledge'):i===8?w('Управление','Management'):w('Среда','Workspace')}</span>}<button",1)
    s=s.replace('</span></button>)}</nav>','</span></button></Fragment>)}</nav>',1)
    return s
edit('apps/web/src/ui/Sidebar.tsx',sidebar)
