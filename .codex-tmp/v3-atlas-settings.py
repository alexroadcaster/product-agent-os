from pathlib import Path
p=Path('apps/web/src/features/tasks/Settings.tsx');s=p.read_text(encoding='utf-8')
s=s.replace("const t=(k:Word)=>label(locale,k),[board", "const t=(k:Word)=>label(locale,k),[board")
s=s.replace(" const [pane,setPane]=useState('components');", " const [pane,setPane]=useState('components'),[columnIndex,setColumnIndex]=useState(0);\n useEffect(()=>setColumnIndex(i=>Math.min(i,Math.max(0,board.columns.length-1))),[board.columns.length]);")
s=s.replace("setPane(release?'releasePolicy':'board');", "setPane(release?'releasePolicy':'board');const index=Number((e.target as HTMLInputElement).name.split('-').at(-1));if(Number.isInteger(index))setColumnIndex(index);")
s=s.replace("<h3>{t('board')}</h3>{board.columns.map((column,index)=><fieldset key={index}>", """<h3>{t('board')}</h3><div className="board-column-catalog"><div className="board-column-row quiet"><span>{t('column')}</span><span>{t('statuses')}</span><span>WIP</span></div>{board.columns.map((column,index)=><button type="button" className="board-column-row" key={index} aria-pressed={columnIndex===index} onClick={()=>setColumnIndex(index)}><strong>{statusText(locale,column.id)}</strong><span>{column.statuses.join(', ')}</span><span>{column.wipLimit??'—'} / {column.wipMode??'soft'}</span></button>)}</div>{board.columns.map((column,index)=><fieldset hidden={columnIndex!==index} key={index}>""")
s=s.replace("onClick={()=>patch({columns:[...board.columns,{id:`column-${board.columns.length+1}`,statuses:[]}]})}","onClick={()=>{setColumnIndex(board.columns.length);patch({columns:[...board.columns,{id:`column-${board.columns.length+1}`,statuses:[]}]});}}")
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/features/tasks/TaskManager.tsx');s=p.read_text(encoding='utf-8')
s=s.replace("[deleteAck,setDeleteAck]=useState(false)","[deleteAck,setDeleteAck]=useState(false),[deleteOpen,setDeleteOpen]=useState(false)")
s=s.replace("workspace==='settings'?t('settings')", "workspace==='settings'?(locale==='ru'?'Настройки задач':'Task settings')")
start=s.index('   <details data-testid="task-delete">');end=s.index('\n  </aside></DetailSurface>',start)
old=s[start:end];body=old[old.index('<label'):old.rindex('</details>')]
body=body.replace('<button className="danger"','<button className="danger"')
s=s[:start]+'''   <div className="task-delete-entry"><button className="danger" data-testid="task-delete-open" onClick={()=>{setDeleteAck(false);setDeleteOpen(true);}}>{t('remove')} · {t('tasks')}</button></div>
   {deleteOpen&&<Modal label={locale==='ru'?'Удалить задачу?':'Delete task?'} onDismiss={()=>setDeleteOpen(false)}><section data-testid="task-delete"><div className="section-heading"><h2>{locale==='ru'?'Удалить задачу?':'Delete task?'}</h2><button aria-label={t('close')} onClick={()=>setDeleteOpen(false)}>×</button></div><p>{task.publicKey??task.id} · {task.title}</p><p className="ui-notice warning">{locale==='ru'?'Связанные записи сохраняются. Удаление задачи не запускает каскадное удаление связанных объектов.':'Linked records are preserved. Deleting a task does not cascade to related records.'}</p>'''+body+'''<button onClick={()=>setDeleteOpen(false)}>{t('cancel')}</button></section></Modal>}
'''+s[end:]
# The Move dialog keeps exactly the existing submit contract, with V3 footer alignment.
s=s.replace("<button>{t('move')}</button><button type=\"button\" onClick={()=>setMove(undefined)}>{t('cancel')}</button>","<div className=\"modal-actions\"><button type=\"button\" onClick={()=>setMove(undefined)}>{t('cancel')}</button><button className=\"primary\">{t('move')}</button></div>")
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/features/tasks/Panels.tsx');s=p.read_text(encoding='utf-8')
s=s.replace("{changes.filter(c=>c.id===entity.id).map((change,i)=><section key={i}><p>","{changes.filter(c=>c.id===entity.id).map((change,i)=><details key={i}><summary>")
s=s.replace("` · omitted: ${change.omittedFields}`:''}</p>{((change.fields", "` · omitted: ${change.omittedFields}`:''}</summary>{((change.fields")
s=s.replace("</pre></dd></dl>)}</section>)}{Array.isArray(payload?.commentChanges)","</pre></dd></dl>)}</details>)}{Array.isArray(payload?.commentChanges)")
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/ui/App.tsx');s=p.read_text(encoding='utf-8')
s=s.replace("'documents','checks','search'].includes(section)","'documents','checks','search','settings'].includes(section)")
s=s.replace('<section className="settings-workspace">','''<section className="settings-workspace"><div className="settings-page-title"><h1>{settingsSection==='processes'?(preferences.locale==='ru'?'Процессы проекта':'Project workflows'):['execution','queue'].includes(settingsSection)?(preferences.locale==='ru'?'Выполнение цепочек':'Recipe execution'):uiLabel(preferences.locale,'nav.settings')}</h1><p className="quiet">{preferences.locale==='ru'?'Рабочая среда и параметры текущего проекта':'Workspace and current project preferences'}</p></div>''')
s=s.replace("{preferences.locale==='ru'?ru:en}</button>)}</div>","<Icon name={id==='projects'?'portfolio':id==='connection'?'agents':id==='processes'?'projectMap':id==='execution'?'autonomy':id==='queue'?'tasks':'settings'}/>{preferences.locale==='ru'?ru:en}</button>)}</div>",1)
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/features/workflows/WorkflowManager.tsx');s=p.read_text(encoding='utf-8')
s=s.replace('<section className="m2-manager workflow-workbench" data-testid="workflow-manager">','<section className="m2-manager workflow-workbench" data-surface={surface} data-testid="workflow-manager">')
s=s.replace("{oldStates.map(s=><label", "<div className=\"workflow-state-mapping\">{oldStates.map(s=><label")
s=s.replace("</select></label>)}<label>{label(locale,'reason')}", "</select></label>)}</div><label>{label(locale,'reason')}")
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/design/parity.css');s=p.read_text(encoding='utf-8')+'''
.settings-page-title{grid-column:1/-1;margin-bottom:4px}.settings-page-title h1{margin:0 0 8px}.settings-navigation button{justify-content:flex-start}.settings-navigation .duo-icon{width:16px;height:16px;flex:0 0 16px}
.workflow-workbench>h2{display:none}.workflow-workbench>p:first-of-type{margin:0 0 16px}.workflow-workbench>button{float:right;margin-bottom:12px}.workflow-navigation{clear:both}
.workflow-workbench[data-surface=execution]>p:first-of-type,.workflow-workbench[data-surface=queue]>p:first-of-type,.workflow-workbench[data-surface=execution]>button,.workflow-workbench[data-surface=queue]>button{display:none}
[data-definition-view=transitions] .workflow-master-detail{grid-template-columns:210px minmax(0,1fr)}[data-definition-view=transitions] .workflow-selection-list{max-height:650px;overflow:auto}[data-definition-view=transitions] .workflow-selection-list>button{min-height:48px;padding:10px 12px}
[data-definition-view=transitions] .workflow-master-detail .m2-fields{grid-template-columns:1fr 1fr}[data-definition-view=transitions] .workflow-master-detail fieldset{display:grid;grid-template-columns:1fr 1fr;gap:16px}[data-definition-view=transitions] .workflow-master-detail fieldset>.m2-fields{grid-column:1/-1}[data-definition-view=transitions] .workflow-master-detail label{margin:0}
.workflow-state-mapping{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:20px 0}.workflow-workbench [name=workflow-recipes]{min-height:280px}
.board-column-catalog{margin:20px 0 28px}.board-column-row{display:grid;grid-template-columns:1fr 1fr 100px;width:100%;text-align:left;gap:16px;padding:14px 8px;border:0;border-bottom:1px solid var(--line);border-radius:0;font-size:12px}.board-column-row[aria-pressed=true]{background:var(--accent-soft)}.board-column-row span{overflow-wrap:anywhere}
[data-settings-pane=releasePolicy]{display:grid;grid-template-columns:1fr 1fr;gap:20px}[data-settings-pane=releasePolicy]>h3,[data-settings-pane=releasePolicy]>label:last-child{grid-column:1/-1}[data-testid=board-settings]>button{float:right;margin:20px 0 0 8px}[data-testid=board-settings]:after{content:'';display:block;clear:both}
.m2-modal>section,.m2-modal>form{padding:24px;border-radius:10px;background:var(--surface);border:1px solid var(--line);box-shadow:var(--shadow-small)}.m2-modal h2{font-size:20px;margin:0}.m2-modal>form>h3{margin:0 0 24px}.modal-actions{display:flex;justify-content:flex-end;gap:12px;border-top:1px solid var(--line);padding-top:20px;margin-top:24px}.task-delete-entry{padding:12px 20px;border-top:1px solid var(--line)}[data-testid=task-delete]>.danger{float:right}[data-testid=task-delete]>.m2-check{margin:20px 0}
.ui-notice{padding:16px;border-radius:6px;background:var(--accent-soft);font-size:12px;line-height:1.65}.ui-notice.warning{background:color-mix(in srgb,var(--amber) 16%,var(--surface))}
[data-testid=task-history] .records>li{padding:12px 0;border-bottom:1px solid var(--line)}[data-testid=task-history] summary{font-size:12px;cursor:pointer}[data-testid=task-history] .m2-fields{margin-bottom:20px}
''';p.write_text(s,encoding='utf-8')
