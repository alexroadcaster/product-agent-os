from pathlib import Path
root=Path('apps/web/src')
def edit(path, fn):
 p=root/path;s=p.read_text(encoding='utf-8');p.write_text(fn(s),encoding='utf-8')
def usage(s):
 at=s.index('export function Metric(')
 s=s[:at]+'''/** Retain the approved analytical layout when the current service exposes no usage measurements. */
export function UsageDashboard({locale,scope}:{locale:Locale;scope?:string}){
 const w=(ru:string,en:string)=>locale==='ru'?ru:en;
 return <section className="usage-dashboard"><div className="ui-metrics">{[['Tokens','tasks'],[w('Стоимость','Cost'),'autonomy'],['tool_use','settings'],[w('Средний расход на run','Average per run'),'sessions']].map(([label,icon])=><Metric key={label} label={label} icon={icon as IconName} value="—" note={w('Измерения недоступны','Measurements unavailable')}/>)}</div><div className="usage-charts">{[w('Динамика расхода','Usage over time'),w('Распределение по инструментам','Usage by tool')].map(title=><section className="panel" key={title}><h2>{title}</h2><div className="dashboard-empty"><Icon name="overview"/><p>{w('Нет измерений для визуализации','No measurements to visualize')}</p></div></section>)}</div><section className="panel"><h2>{w('Расход по запускам','Usage by run')}</h2><div className="usage-table-head"><span>Run</span><span>Tokens</span><span>tool_use</span><span>{w('Стоимость','Cost')}</span></div><p className="quiet">{w('Источник PAOS пока не предоставляет измерения расхода. Неизвестное значение не равно нулю.','PAOS does not currently expose usage measurements. Unknown is not zero.')}{scope?' · '+scope:''}</p></section></section>;
}
''' + s[at:]
 return s
edit(Path('features/dashboard/Dashboard.tsx'),usage)
def app(s):
 s=s.replace('{Dashboard,Usage}', '{Dashboard,Usage,UsageDashboard}').replace('{ Dashboard, Usage }','{ Dashboard, Usage, UsageDashboard }')
 s=s.replace("'checks','search','settings'].includes(section)","'checks','search','settings','sessions'].includes(section)")
 s=s.replace('<div className="panel" hidden={overviewPane!==\'sources\'}>','<div hidden={overviewPane!==\'sources\'}>')
 s=s.replace('<Usage locale={preferences.locale}/>', '<UsageDashboard locale={preferences.locale}/>')
 return s
edit(Path('ui/App.tsx'),app)
def sessions(s):
 s=s.replace('import {Usage}', 'import {UsageDashboard}')
 nav=s[s.index('<div className="section-tabs"><button'):s.index("<div hidden={pane!=='usage'}>")]
 s=s.replace(nav,'')
 start=s.index('  <button className="primary"');end=s.index('\n  <details data-testid="session-filters"',start)
 button=s[start:end];s=s[:start]+s[end:]
 old='return <div data-testid="sessions-catalog"><p role="alert">{error}</p><div className="session-layout">'
 new='return <div data-testid="sessions-catalog" data-pane={pane}>'+nav+'<div className="section-heading"><h1>{w(\'Сессии\',\'Sessions\')}</h1>'+button+'</div><p role="alert">{error}</p><div className="session-layout">'
 s=s.replace(old,new).replace('<Usage locale=', '<UsageDashboard locale=')
 return s
edit(Path('features/sessions/SessionsCatalog.tsx'),sessions)
def operations(s):
 a=s.index('export function Sources(');b=s.index('export function ImportTasks(',a)
 part=s[a:b].replace('<section className="panel">','<section className="sources-workspace"><div className="panel sources-catalog">',1)
 part=part.replace('      {content && (','      </div><aside className="panel sources-context"><h2>{t("source")}</h2><p className="quiet">{projectId}</p><dl><dt>{t("available")}</dt><dd>{source?.sources.filter(item=>item.status===\'available\').length??\'—\'} / {source?.sources.length??\'—\'}</dd></dl>\n      {content && (',1)
 part=part.replace('    </section>\n  );','    </aside></section>\n  );')
 # AppLabel has no generic available label; keep the existing source-coverage label.
 part=part.replace('t("available")','t("source")')
 s=s[:a]+part+s[b:]
 return s
edit(Path('ui/Operations.tsx'),operations)
def recipes(s):
 s=s.replace(" const alive=useRef(true)"," const [pane,setPane]=useState('preview');\n const alive=useRef(true)")
 s=s.replace('<section className="panel" data-testid="recipe-runner">','<section className="recipe-workspace" data-testid="recipe-runner"><div className="section-tabs">{[[\'preview\',w(\'Предпросмотр\',\'Preview\')],[\'history\',w(\'История\',\'History\')],[\'recovery\',w(\'Восстановление\',\'Recovery\')]].map(([id,name])=><button key={id} data-recipe-pane={id} aria-pressed={pane===id} onClick={()=>setPane(id)}>{name}</button>)}</div>')
 s=s.replace('  <form onSubmit=', '  <div hidden={pane!==\'preview\'} className="panel recipe-proposal"><form onSubmit=',1)
 s=s.replace("  <h3>{w('История выполнения','Execution history')}</h3>","  </div><div hidden={pane==='preview'}><h3>{pane==='recovery'?w('Восстановление','Recovery'):w('История выполнения','Execution history')}</h3>")
 s=s.replace('data-testid="recipe-execution">','data-testid="recipe-execution" hidden={pane===\'recovery\'&&!e.recovery}>')
 s=s.replace(' </section>;\n}', ' </div></section>;\n}',1)
 return s
edit(Path('features/workflows/recipes/RecipeRunner.tsx'),recipes)
def decisions(s):
 s=s.replace("[['list',w('Ожидают решения','Decisions')],['create'", "[['list',w('Ожидают решения','Decisions')],['history',w('История','History')],['create'")
 anchor='  <div hidden={!embedded&&pane!==\'list\'}>'
 history='''  {!embedded&&pane==='history'&&<section className="panel decision-history-table"><h2>{w('История решений','Decision history')}</h2><table><thead><tr><th>{w('Решение','Decision')}</th><th>{w('Событие','Event')}</th><th>{w('Автор','Actor')}</th><th>{w('Время','Time')}</th></tr></thead><tbody>{page?.items.flatMap(d=>d.history.map((h,i)=><tr key={d.id+':'+i}><td><button onClick={()=>{setSelectedId(d.id);setPane('list');}}>{d.title}</button></td><td>{h.event}<small>{h.detail}</small></td><td>{h.actor}</td><td>{new Date(h.at).toISOString()}</td></tr>))}</tbody></table></section>}
'''
 s=s.replace(anchor,history+anchor)
 return s
edit(Path('features/decisions/DecisionBoard.tsx'),decisions)
css='''
/* V3 secondary workspaces: same field handlers, explicit local navigation and bounded grids. */
.sources-workspace{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:24px;align-items:start}.sources-workspace>.panel{margin:0;min-width:0}.sources-catalog .source-row{display:grid;grid-template-columns:minmax(0,1fr) 100px auto;gap:12px;align-items:center;padding:14px 0}.sources-catalog .source-row>p{grid-column:1/-1;grid-row:2;margin:0}.sources-catalog .source-row>button{grid-column:3;grid-row:1}.sources-context pre{max-height:520px;overflow:auto}.sources-context>p{overflow-wrap:anywhere}
.usage-dashboard>.ui-metrics{margin:24px 0}.usage-charts{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:24px}.usage-charts .dashboard-empty{min-height:230px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--muted)}.usage-table-head{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;padding:12px 0;border-block:1px solid var(--line);font-size:12px;color:var(--muted)}
[data-testid=sessions-catalog]>.section-heading{margin:24px 0}[data-testid=sessions-catalog]>.section-heading h1{margin:0}[data-testid=sessions-catalog][data-pane=usage]>.session-layout{display:block}[data-testid=sessions-catalog][data-pane=usage] .session-list{display:none}[data-testid=sessions-catalog][data-pane=usage]>.session-layout>section{border:0;padding:0;background:transparent}.session-layout{grid-template-columns:200px minmax(0,1fr)}.session-list .records button{padding:12px;text-align:left}.session-list small{display:block;overflow-wrap:anywhere}.session-work-area{grid-template-columns:minmax(0,1fr) 240px}
[data-testid=import-workspace],.autonomy-workspace{display:grid;grid-template-columns:190px minmax(0,1fr);column-gap:24px;align-items:start}[data-testid=import-workspace]>.section-tabs,.autonomy-workspace>.section-tabs{grid-column:1;grid-row:1/30;display:flex;flex-direction:column;align-items:stretch;border:0;padding-right:20px;border-right:1px solid var(--line)}[data-testid=import-workspace]>.section-tabs>button,.autonomy-workspace>.section-tabs>button{text-align:left;border-radius:8px;justify-content:flex-start}[data-testid=import-workspace]>.section-tabs>button[aria-pressed=true],.autonomy-workspace>.section-tabs>button[aria-pressed=true]{background:var(--accent-soft)}[data-testid=import-workspace]>:not(.section-tabs),.autonomy-workspace>:not(.section-tabs){grid-column:2;min-width:0}[data-testid=import-workspace] .operation-form{grid-template-columns:minmax(0,1fr)}[data-testid=import-workspace] .operation-form input[type=file]{min-height:110px}.autonomy-policy-grid{display:block}.autonomy-policy-grid>aside{padding:20px;background:var(--accent-soft);border-radius:10px}.autonomy-policy-grid fieldset>.fields{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.autonomy-workspace>.actions{margin-bottom:20px}
.decision-columns{grid-template-columns:minmax(0,1fr) 360px}.decision-history-table table{width:100%;border-collapse:collapse}.decision-history-table td,.decision-history-table th{padding:12px;text-align:left;border-bottom:1px solid var(--line)}.decision-history-table small{display:block;color:var(--muted)}
.recipe-workspace>.section-tabs{margin-bottom:24px}.recipe-workspace>h2{display:none}.recipe-workspace>.recipe-proposal{margin-top:20px}.recipe-proposal fieldset{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.recipe-proposal fieldset>p,.recipe-proposal fieldset>label:has([name=recipe-reason]),.recipe-proposal fieldset>button{grid-column:1/-1}.recipe-proposal fieldset>button{justify-self:end}.recipe-proposal [data-testid=recipe-preview]{margin-top:24px;border-top:1px solid var(--line);padding-top:20px}
'''
p=root/'design/parity.css';p.write_text(p.read_text(encoding='utf-8')+css,encoding='utf-8')
