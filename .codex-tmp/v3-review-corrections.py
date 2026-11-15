from pathlib import Path
root=Path('apps/web/src')
def edit(path,fn):
 p=root/path;p.write_text(fn(p.read_text(encoding='utf-8')),encoding='utf-8')
def modal(s):
 s=s.replace('if(expanded)dialog.showModal();else dialog.show();','if(expanded){dialog.showModal();dialog.scrollTop=0;dialog.querySelector<HTMLElement>(\'[data-testid="task-expand"]\')?.focus({preventScroll:true});}else dialog.show();')
 return s
edit(Path('ui/Modal.tsx'),modal)
def task(s):
 s=s.replace('</label><button className="danger" disabled={busy||!deleteAck}', '</label><div className="modal-actions"><button className="danger" disabled={busy||!deleteAck}')
 s=s.replace("{t('cancel')}</button></section></Modal>","{t('cancel')}</button></div></section></Modal>")
 s=s.replace("onClick={()=>setTab(k)}>{t(k)}", "onClick={()=>setTab(k)}>{({history:locale==='ru'?'История':'History',links:locale==='ru'?'Связи':'Links',sessions:locale==='ru'?'Сессии':'Sessions'} as Partial<Record<Word,string>>)[k]??t(k)}")
 s=s.replace("[workspace,setWorkspace]=useState('tasks');", "[workspace,setWorkspace]=useState('tasks'),[settingsPane,setSettingsPane]=useState('components');")
 s=s.replace('<ManagerSettings snapshot={snapshot} command={command} locale={locale}/>', '<ManagerSettings snapshot={snapshot} command={command} locale={locale} selectedPane={settingsPane} onSelectPane={setSettingsPane} onArchive={()=>setWorkspace(\'archive\')}/>')
 s=s.replace("<div hidden={workspace!=='archive'}><FullArchive", "<div hidden={workspace!=='archive'} className=\"task-settings-workspace\"><nav className=\"settings-navigation\">{(['components','versions','releasePolicy','board'] as const).map(id=><button key={id} onClick={()=>{setSettingsPane(id);setWorkspace('settings');}}>{t(id)}</button>)}<button aria-selected=\"true\">{locale==='ru'?'Полный архив':'Full archive'}</button></nav><FullArchive")
 return s
edit(Path('features/tasks/TaskManager.tsx'),task)
def settings(s):
 s=s.replace(" const item=draft.item", " const [editing,setEditing]=useState(false);\n const item=draft.item",1)
 s=s.replace(' return <form className="m2-catalog-row"', ' return <div className="catalog-item"><div className="catalog-item-summary"><strong>{value.name}</strong><span className="badge">{t(value.status as Word)}</span><button type="button" aria-expanded={editing} onClick={()=>setEditing(!editing)}>{locale===\'ru\'?\'Изменить\':\'Edit\'}</button></div><form hidden={!editing} className="m2-catalog-row"',1)
 s=s.replace(' </form>;\n}', ' </form></div>;\n}',1)
 s=s.replace('ManagerSettings({snapshot,command,locale}:{snapshot:ManagerSnapshot<StoredEntity>;command:Command;locale:Locale})', 'ManagerSettings({snapshot,command,locale,selectedPane,onSelectPane,onArchive}:{snapshot:ManagerSnapshot<StoredEntity>;command:Command;locale:Locale;selectedPane?:string;onSelectPane?:(pane:string)=>void;onArchive?:()=>void})')
 s=s.replace(" const [componentName", " useEffect(()=>{if(selectedPane)setPane(selectedPane);},[selectedPane]);\n const [componentName",1)
 s=s.replace('onClick={()=>setPane(id)}>{t(id)}</button>)}</nav>', 'onClick={()=>{setPane(id);onSelectPane?.(id);}}>{t(id)}</button>)}{onArchive&&<button onClick={onArchive}>{locale===\'ru\'?\'Полный архив\':\'Full archive\'}</button>}</nav>')
 return s
edit(Path('features/tasks/Settings.tsx'),settings)
def panels(s):
 s=s.replace('<section key={i}><h4>{String(change.kind)} · {String(change.id)}</h4>', '<details key={i}><summary>{String(change.kind)} · {String(change.id)}</summary>')
 s=s.replace('JSON.stringify({previous:change.previous,current:change.current,redacted:change.redacted},null,2)}</pre></section>', 'JSON.stringify({previous:change.previous,current:change.current,redacted:change.redacted},null,2)}</pre></details>')
 return s
edit(Path('features/tasks/Panels.tsx'),panels)
def workflows(s):
 s=s.replace("[newId,setNewId]=useState('')", "[newId,setNewId]=useState(''),[newName,setNewName]=useState('')")
 s=s.replace('setDraft(empty());','setDraft({...empty(),...(newName.trim()?{name:newName.trim()}:{})});')
 s=s.replace('setDraft(structuredClone(draft));','setDraft({...structuredClone(draft),...(newName.trim()?{name:newName.trim()}:{})});')
 s=s.replace('value={newId} onChange={e=>setNewId(e.target.value)}/></label></div>', 'value={newId} onChange={e=>setNewId(e.target.value)}/></label><label>{label(locale,\'name\')}<input name="workflow-new-name" value={newName} onChange={e=>setNewName(e.target.value)}/></label></div>')
 s=s.replace("{w('Создать копию','Create copy')}</button>", "{w('Создать копию','Create copy')}</button><table className=\"dashboard-data-table\"><thead><tr><th>{w('Процесс','Workflow')}</th><th>{w('Активная версия','Active version')}</th><th>{w('Название','Name')}</th></tr></thead><tbody>{registry.workflows.map(row=><tr key={row.id}><td><button disabled={dirty||busy} onClick={()=>choose(row.id)}>{row.id}</button></td><td>{row.activeVersion??'—'}</td><td>{row.versions.find(version=>version.version===row.activeVersion)?.definition.name??'—'}</td></tr>)}</tbody></table>")
 s=s.replace("<h3>{w('Публикация','Publication')}</h3><button", "<h3>{w('Публикация','Publication')}</h3><dl className=\"task-summary-properties\"><dt>{w('Процесс','Workflow')}</dt><dd>{selected}</dd><dt>{w('Активная версия','Active version')}</dt><dd>{record?.activeVersion??'—'}</dd><dt>{w('Черновик','Draft')}</dt><dd>{record?.draft?w('Сохранён','Saved'):w('Не сохранён','Not saved')}</dd></dl><p className=\"ui-notice\">{w('Старые задачи и запуски сохраняют закреплённую версию. Публикация требует отдельного предпросмотра.','Existing tasks and runs retain the pinned version. Publication requires a separate preview.')}</p><button")
 return s
edit(Path('features/workflows/WorkflowManager.tsx'),workflows)
def operations(s):
 s=s.replace('className="sources-context"><h2>{t("source")}</h2>', 'className="sources-context"><h2>{t("root")}</h2>')
 s=s.replace('<aside className="panel sources-context"><h2>{t("source")}</h2>', '<aside className="panel sources-context"><h2>{t("root")}</h2>')
 # Compact immutable receipt metadata; retain the full manifest in an explicit disclosure.
 s=s.replace('<pre className="diff">\n            {JSON.stringify(receipt.manifest, null, 2)}\n          </pre>', '<details><summary>Manifest</summary><pre className="diff">{JSON.stringify(receipt.manifest, null, 2)}</pre></details>')
 marker='data-testid="backup-workspace"><div className="section-tabs">'
 s=s.replace(marker, 'data-testid="backup-workspace"><aside className="backup-boundary"><h3>{t("backup")}</h3><p>{t("backupHint")}</p><h3>{t("restore")}</h3><p>{t("restoreHint")}</p></aside><div className="section-tabs">')
 s=s.replace('<form className="panel operation-form" hidden=', '<form className="panel operation-form" hidden=')
 s=s.replace('          <p className="quiet">{t("importSafety")}</p>', '          <p className="ui-notice">{t("importSafety")}</p>')
 return s
edit(Path('ui/Operations.tsx'),operations)
def app(s):
 s=s.replace('<div hidden={overviewPane!==\'sources\'}><Sources', '<div hidden={overviewPane!==\'sources\'}><h1>{t(\'source\')}</h1><Sources')
 s=s.replace('["service","Локальный сервис","Local service"],','').replace('["queue","Очередь","Queue"],','["queue","Очередь","Queue"],["service","Завершение сервиса","Quit service"],')
 s=s.replace('<h2>{t("quit")}</h2>', '<h2>{t("quit")}</h2><p className="ui-notice warning">{t("quitConfirm")}. {t("restartRequired")}</p>') if False else s
 return s
edit(Path('ui/App.tsx'),app)
def autonomy(s):
 s=s.replace("<h3>{w('Предпросмотр','Preview')}</h3>", "<h3>{w('Предпросмотр','Preview')}</h3><dl className=\"task-summary-properties\"><dt>{w('Задачи','Tasks')}</dt><dd>{draft.allowedTaskIds.map(id=>tasks.find(task=>task.id===id)?.publicKey??id).join(', ')}</dd><dt>{w('Максимум запусков','Maximum runs')}</dt><dd>{draft.maxRuns}</dd><dt>{w('Команд на запуск','Commands per run')}</dt><dd>{draft.maxCommandsPerRun}</dd><dt>{w('Лимит, секунды','Limit, seconds')}</dt><dd>{draft.maxRunSeconds}</dd></dl><p className=\"ui-notice\">{w('Права host не меняются. Сохранение не запускает работу.','Host permissions are unchanged. Saving does not start work.')}</p>")
 return s
edit(Path('features/autonomy/AutonomyManager.tsx'),autonomy)
css='''
/* Corrections from paired V3 review, not overflow suppression. */
.ui-notice.warning{background:#fff0cd;color:#563b08}[data-theme=dark] .ui-notice.warning{background:#40331b;color:#ffe2a1}
.modal-actions>.danger{order:2}.modal-actions>button{margin:0}.task-detail-overlay .task-detail-heading{position:sticky;top:0;background:var(--surface);z-index:4}.task-detail-overlay .task-detail-status{position:sticky;top:76px;background:var(--surface);z-index:3}.task-detail-overlay .task-detail>[role=tablist]{position:sticky;top:130px;background:var(--surface);z-index:3}.task-detail-overlay .task-detail{overflow:visible}
.catalog-item-summary{display:grid;grid-template-columns:minmax(0,1fr) 120px auto;gap:16px;align-items:center;padding:12px 0;border-bottom:1px solid var(--line)}.catalog-item-summary button{font-size:12px}.catalog-item .m2-catalog-row{padding:20px;background:var(--recess);border-radius:8px}.task-settings-workspace .panel>section>form:last-child{margin-top:24px}
.chat-panel .sources-workspace{display:block}.chat-panel .sources-context{margin-top:16px}.chat-panel .sources-catalog .source-row{grid-template-columns:minmax(0,1fr) auto}.chat-panel .sources-catalog .source-row>button{grid-column:1/-1;grid-row:auto;justify-self:start}.chat-panel .sources-catalog .source-row>strong{overflow-wrap:break-word}.sources-catalog .source-row{padding:10px 0}.sources-catalog .source-row>p{font-size:11px}.sources-catalog h2{font-size:16px}
.workflow-workbench{display:flex;flex-direction:column}.workflow-workbench>.workflow-navigation{order:-3;margin-top:0}.workflow-workbench>p:empty{display:none}.workflow-workbench>h2+p{font-size:12px;margin:0 0 12px}.workflow-workbench>button{align-self:flex-end;margin:0 0 16px}.workflow-catalog>.m2-fields>label:first-child{grid-column:1/-1}.workflow-catalog>.dashboard-data-table{margin-top:24px}.workflow-workbench [data-testid=workflow-editor]>fieldset>h3{font-size:16px;margin:0}.workflow-workbench [data-testid=workflow-editor]>fieldset>p{display:inline-block;margin:8px 16px 8px 0;font-size:11px}.workflow-properties{display:inline-block;margin:8px 0;font-size:12px}.workflow-workbench fieldset fieldset{border:0;padding:0}.workflow-master-detail .m2-fields{align-items:start}.workflow-workbench label{align-content:start}
.session-runtime-detail .task-metadata{display:grid;grid-template-columns:120px minmax(0,1fr)}.session-runtime-detail .task-metadata dd{margin:0}.autonomy-policy-grid .m2-fields{grid-template-columns:repeat(3,minmax(0,1fr))}.autonomy-policy-grid fieldset{border:0;padding:0}.autonomy-policy-grid fieldset>button{display:flex;margin-left:auto}.autonomy-workspace>button{justify-self:end}.autonomy-workspace>p{font-size:12px;margin:8px 0}
[data-testid=backup-workspace]{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:24px}[data-testid=backup-workspace]>.section-tabs{grid-column:1/-1;grid-row:1}[data-testid=backup-workspace]>.backup-boundary{grid-column:2;grid-row:2/8;font-size:12px;padding:16px 0}[data-testid=backup-workspace]>:not(.section-tabs):not(.backup-boundary){grid-column:1;min-width:0}[data-testid=backup-workspace]>.panel{width:100%;max-width:none}[data-testid=project-onboarding]>form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:24px}[data-testid=project-onboarding]>form>button{grid-column:1/-1;justify-self:end}
[data-testid=skill-generation-editor] label{align-content:start}[data-testid=skill-generation-editor] input{height:40px}[data-testid=skill-generation-editor] textarea[name=generated-skill-description]{min-height:40px;height:40px}[data-testid=skill-generation-preview] .diff{min-height:160px}.ui-mermaid{max-height:520px;overflow:auto}.ui-mermaid>div{min-width:0}.ui-mermaid svg{min-height:350px;max-height:500px;width:100%;height:auto}
'''
p=root/'design/parity.css';p.write_text(p.read_text(encoding='utf-8')+css,encoding='utf-8')
