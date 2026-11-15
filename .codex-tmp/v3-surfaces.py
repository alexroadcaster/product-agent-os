from pathlib import Path
root=Path('apps/web/src')
def edit(path,changes):
 p=root/path;s=p.read_text(encoding='utf-8')
 for old,new in changes:
  assert old in s,(path,old[:100])
  s=s.replace(old,new,1)
 p.write_text(s,encoding='utf-8')
edit(Path('ui/Sidebar.tsx'),[('[1,5,8,11]','[0,6,9,11]'),("i===1?w('Работа','Work'):i===5?w('Знания','Knowledge'):i===8?","i===0?w('Работа','Work'):i===6?w('Знания','Knowledge'):i===9?")])
edit(Path('features/team/TeamManager.tsx'),[
 ("import {AgentDashboard}","import {SkillGenerator} from '../skills/SkillGenerator.tsx';\nimport {AgentDashboard}"),
 ("['discover',w('Найти / импортировать','Discover / import')]]","['discover',w('Найти / импортировать','Discover / import')],['requirements',w('Создать скилл','Create skill')]]"),
 ('<p role="alert">{error}</p><p role="status">',"{kind==='skill'&&<div hidden={workspace!=='requirements'}><SkillGenerator api={api} projectId={projectId} locale={locale} onOpenAsset={onOpenAsset} onOpenSession={onOpenSession}/></div>}<p role=\"alert\">{error}</p><p role=\"status\">")])
p=root/'ui/App.tsx';s=p.read_text(encoding='utf-8');start=s.index("/>{section==='skills'&&<SkillGenerator");end=s.index('</>',start);s=s[:start]+'/>'+s[end:];s=s.replace("import {SkillGenerator} from '../features/skills/SkillGenerator.tsx';\n",'');p.write_text(s,encoding='utf-8')
edit(Path('features/sessions/SessionsCatalog.tsx'),[
 ("useState<'work'|'history'>('work')","useState<'work'|'history'|'usage'>('work')"),
 ('<form data-testid="session-history-search"','<details className="session-history-search"><summary>{w(\'Поиск по истории\',\'Search history\')}</summary><form data-testid="session-history-search"'),
 ("{w('Найти в истории','Search history')}</button></form>","{w('Найти в истории','Search history')}</button></form></details>"),
 ('{entity?<><h2>{entity.title??entity.id}</h2><form','{entity?<><div className="session-title-row"><h2>{entity.title??entity.id}</h2><span className="badge">{entity.status}</span></div><details className="session-properties"><summary>{w(\'Свойства сессии\',\'Session properties\')}</summary><form'),
 ("<div className=\"tabs\"><button aria-pressed={pane==='work'}","</details><div className=\"section-tabs\"><button aria-pressed={pane==='work'}"),
 ("{w('Полная доступная история','Full available history')}</button></div>","{w('Полная доступная история','Full available history')}</button><button aria-pressed={pane==='usage'} onClick={()=>setPane('usage')}>Tokens / tool_use</button></div>"),
 ("<Usage locale={locale} scope={entity.title??entity.id}/>{pane==='work'?renderSession(entity):<Transcript", "<div hidden={pane!=='usage'}><Usage locale={locale} scope={entity.title??entity.id}/></div><div className=\"session-work-area\" hidden={pane!=='work'}>{renderSession(entity)}</div>{pane==='history'&&<Transcript")])
edit(Path('features/tasks/TaskManager.tsx'),[
 ('<div id="task-panel" role="tabpanel"','<div className="task-detail-body"><div id="task-panel" role="tabpanel"'),
 ('    </div>\n   </>}','    </div><aside className="task-context" hidden={!expanded}><h3>{locale===\'ru\'?\'Контекст задачи\':\'Task context\'}</h3><dl><dt>{t(\'priority\')}</dt><dd>{priorityText(locale,String(task.data?.priority??\'\'))}</dd><dt>{t(\'estimate\')}</dt><dd>{durationText(task.data?.estimateSeconds)}</dd><dt>{t(\'dueDate\')}</dt><dd>{String(task.data?.dueDate??\'—\')}</dd></dl><h3>{locale===\'ru\'?\'Связанные сессии\':\'Linked sessions\'}</h3>{data?.sessionIds.length?data.sessionIds.map(id=><button key={id} disabled={!onOpenSession} onClick={()=>onOpenSession?.(id)}>{id}</button>):<p className="quiet">{locale===\'ru\'?\'Сессии не связаны\':\'No linked sessions\'}</p>}<p className="quiet">{locale===\'ru\'?\'Изменения сохраняются после проверки формы.\':\'Changes are saved after form validation.\'}</p></aside></div>\n   </>}')])
