from pathlib import Path
def put(path,fn):
 p=Path('apps/web/src')/path;s=p.read_text(encoding='utf-8');s=fn(s);p.write_text(s,encoding='utf-8')
def operations(s):
 start=s.index('export function ImportTasks');end=s.index('export function Backup');a=s[start:end]
 a=a.replace('  return (','  const [pane,setPane]=useState(\'source\');\n  return (',1)
 a=a.replace('<section className="panel">','<section className="operations-workspace" data-testid="import-workspace"><div className="section-tabs">{[[\'source\',t(\'source\')],[\'preview\',t(\'preview\')],[\'export\',t(\'reverseExport\')]].map(([id,name])=><button key={id} aria-pressed={pane===id} onClick={()=>setPane(id)}>{name}</button>)}</div>',1)
 a=a.replace('<form\n','<form className="panel operation-form" hidden={pane!==\'source\'}\n',1)
 a=a.replace('setSourceFile(file);',"setSourceFile(file);setPane('preview');",1)
 a=a.replace('<div className="import-preview">',"<div className=\"panel import-preview\" hidden={pane!=='preview'}>",1)
 a=a.replace('<section>\n        <h3>{t("sourceStatus")}',"<section className=\"panel\" hidden={pane!=='source'}>\n        <h3>{t(\"sourceStatus\")}",1)
 a=a.replace('<section className="reverse-export">',"{!preview&&pane==='preview'&&<p className=\"panel\">{t('sourceBindingHint')}</p>}<section className=\"panel reverse-export\" hidden={pane!=='export'}>",1)
 s=s[:start]+a+s[end:];start=s.index('export function Backup');end=s.index('export function TaskHistory');a=s[start:end]
 a=a.replace('  return (',"  const [pane,setPane]=useState('create');\n  return (",1)
 a=a.replace('<section className="panel">',"<section className=\"operations-workspace\" data-testid=\"backup-workspace\"><div className=\"section-tabs\">{[['create',t('createBackup')],['restore',t('restore')]].map(([id,name])=><button key={id} aria-pressed={pane===id} onClick={()=>setPane(id)}>{name}</button>)}</div><div className=\"panel\" hidden={pane!=='create'}>",1)
 a=a.replace('<section className="restore">',"</div><section className=\"panel restore\" hidden={pane!=='restore'}>",1)
 # Keep errors visible in either panel without changing the request handlers.
 a=a.replace('<h3>{t("restore")}</h3>', '<h3>{t("restore")}</h3>{pane===\'restore\'&&<p role="alert">{error}</p>}',1)
 return s[:start]+a+s[end:]
put('ui/Operations.tsx',operations)
def settings(s):
 s=s.replace("const [componentName,setComponentName]","const [pane,setPane]=useState('components');\n const [componentName,setComponentName]",1)
 s=s.replace('<details data-testid="manager-settings" className="m2-settings"><summary>{t(\'settings\')}</summary>', '<section data-testid="manager-settings" className="task-settings-workspace"><nav className="settings-navigation" aria-label={t(\'settings\')}>{([\'components\',\'versions\',\'releasePolicy\',\'board\'] as const).map(id=><button key={id} aria-selected={pane===id} onClick={()=>setPane(id)}>{t(id)}</button>)}</nav><div className="panel">',1)
 s=s.replace("<section><h3>{t('components')}","<section hidden={pane!=='components'}><h3>{t('components')}",1)
 s=s.replace("<section><h3>{t('versions')}","<section hidden={pane!=='versions'}><h3>{t('versions')}",1)
 s=s.replace('<form data-testid="board-settings"','<form hidden={pane!==\'board\'&&pane!==\'releasePolicy\'} onInvalidCapture={e=>{const release=(e.target as HTMLElement).closest(\'[data-settings-pane="releasePolicy"]\');setPane(release?\'releasePolicy\':\'board\');}} data-testid="board-settings"',1)
 s=s.replace("<h3>{t('releasePolicy')}</h3>","<div data-settings-pane=\"releasePolicy\" hidden={pane!=='releasePolicy'}><h3>{t('releasePolicy')}</h3>",1)
 s=s.replace("<h3>{t('board')}</h3>","</div><div data-settings-pane=\"board\" hidden={pane!=='board'}><h3>{t('board')}</h3>",1)
 s=s.replace('<button disabled={busy} className="primary">', '</div><button disabled={busy} className="primary">',1)
 s=s.replace('</form><p role="alert">{error}</p>\n </details>','</form><p role="alert">{error}</p></div>\n </section>',1)
 s=s.replace('<details data-testid="manager-archive" className="m2-settings"><summary>{t(\'archive\')}</summary>', '<section data-testid="manager-archive" className="panel"><h2>{t(\'archive\')}</h2>',1)
 # Last details belonged to the archive surface.
 s=s.replace('\n </details>;','\n </section>;',1)
 return s
put('features/tasks/Settings.tsx',settings)
def decisions(s):
 s=s.replace(' const generation=useRef'," const [pane,setPane]=useState('list');\n const generation=useRef",1)
 s=s.replace('<section className="panel" data-testid="decision-board"><h2>', '<section className={embedded?\'panel\':\'decision-workspace\'} data-testid="decision-board">{!embedded&&<div className="section-tabs">{[[\'list\',w(\'Ожидают решения\',\'Decisions\')],[\'create\',w(\'Создать\',\'Create\')]].map(([id,name])=><button key={id} aria-pressed={pane===id} onClick={()=>setPane(id)}>{name}</button>)}</div>}<h2>',1)
 s=s.replace('<details open data-testid="autonomy-observation">','<details data-testid="autonomy-observation">',1)
 s=s.replace('<div className="actions"><label>', '<div hidden={!embedded&&pane!==\'list\'}><div className="actions decision-filters"><label>',1)
 s=s.replace('<ul className="decision-list">','<div className="decision-columns"><section><ul className="decision-list">',1)
 s=s.replace('{selected&&<article', '</section>{selected&&<article',1)
 s=s.replace('  <details><summary>{w(\'Создать', '  </div></div><details className="panel decision-create" open={!embedded} hidden={!embedded&&pane!==\'create\'}><summary>{w(\'Создать',1)
 return s
put('features/decisions/DecisionBoard.tsx',decisions)
