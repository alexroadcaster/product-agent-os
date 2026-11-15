from pathlib import Path
p=Path('apps/web/src/features/team/TeamManager.tsx');s=p.read_text(encoding='utf-8')
a=s.index('<aside className="panel"><ul className="records">');b=s.index('</aside>',a)+len('</aside>');catalog=s[a:b]
s=s[:a]+'{catalogPanel}'+s[b:]
# Share the same catalog presentation across profile, proposal and discovery workspaces.
catalog=catalog.replace('<aside className="panel">','<aside className="panel team-source-catalog"><h3>{kind===\'agent\'?w(\'Профили / источники\',\'Profiles / sources\'):w(\'Скиллы / источники\',\'Skills / sources\')}</h3>')
catalog=catalog.replace("onClick={()=>{setSelected(a.id);setPane('profile');}}", "onClick={()=>{setSelected(a.id);setPane('profile');setWorkspace('profiles');}}")
a=s.index('  <details><summary>');b=s.index('</details>',a)+len('</details>');details=s[a:b];s=s[:a]+s[b:]
catalog=catalog.replace('</aside>',details+'</aside>')
pos=s.index(' return <section');s=s[:pos]+' const catalogPanel='+catalog+';\n'+s[pos:]
s=s.replace('className="m2-manager" data-testid={kind', 'className="m2-manager" data-workspace={workspace} data-testid={kind',1)
s=s.replace('<div className="resource-toolbar">','<div className="resource-toolbar team-profile-toolbar">',1)
s=s.replace("{kind==='agent'&&<section hidden={workspace!=='generate'}", "<div className=\"team-proposal-layout\" hidden={workspace!=='generate'&&workspace!=='discover'}>{catalogPanel}{kind==='agent'&&<section hidden={workspace!=='generate'}",1)
s=s.replace('  </section>}\n </section>;', '  </section>}</div>\n </section>;',1)
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/features/dashboard/Dashboard.tsx');s=p.read_text(encoding='utf-8').replace("w('Динамика расхода','Usage over time')","w('Tokens по агентам','Tokens by agent')").replace("w('Распределение по инструментам','Usage by tool')","w('Вызовы инструментов','Tool calls')");p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/features/workflows/WorkflowManager.tsx');s=p.read_text(encoding='utf-8');a=s.index('<ul>{record.versions.map');b=s.index('</ul>',a)+5
s=s[:a]+'''<table className="dashboard-data-table"><thead><tr><th>{w('Версия','Version')}</th><th>{w('Название','Name')}</th><th>{w('Состояние','State')}</th><th>{w('Действие','Action')}</th></tr></thead><tbody>{record.versions.map(v=><tr key={v.version}><td>v{v.version}</td><td>{v.definition.name}<small>{v.publishedAt??w('Дата неизвестна','Date unknown')}</small></td><td><span className="badge">{v.version===record.activeVersion?w('Для новых задач','For new tasks'):w('Опубликована','Published')}</span></td><td><button disabled={busy||dirty||v.version===record.activeVersion} onClick={()=>void run(()=>action('workflow-rollback',{version:v.version}))}>{w('Использовать для новых задач','Use for new tasks')}</button></td></tr>)}</tbody></table><h4>{w('Архивирование процесса','Archive workflow')}</h4><p>{w('Исторические версии задач и запусков сохраняются.','Historical task and run versions are preserved.')}</p>'''+s[b:]
p.write_text(s,encoding='utf-8')
