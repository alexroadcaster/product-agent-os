from pathlib import Path
def edit(path,fn):
 p=Path(path);s=p.read_text(encoding='utf-8');n=fn(s)
 if n==s:raise RuntimeError(path)
 p.write_text(n,encoding='utf-8')

def team(s):
 s=s.replace(" const [catalog,setCatalog]", " const [workspace,setWorkspace]=useState(kind==='agent'&&!initialAssetId?'dashboard':'profiles');\n const [catalog,setCatalog]",1)
 s=s.replace("if(initialAssetId", "if(initialAssetId",1)
 s=s.replace("if(matches.length===1)setSelected(matches[0].id);", "if(matches.length===1){setSelected(matches[0].id);setWorkspace('profiles');}",1)
 s=s.replace("function edit(action:AssetAction='update',copy=false){", "function edit(action:AssetAction='update',copy=false){setWorkspace('profiles');",1)
 head='<h2>{kind===\'agent\'?w(\'Агенты проекта\',\'Project agents\'):w(\'Скиллы проекта\',\'Project skills\')}</h2>'
 nav='''<div className="section-tabs resource-workspace-tabs">{(kind==='agent'?[['dashboard',w('Общий dashboard','Dashboard')],['agent',w('Агент','Agent')],['profiles',w('Профили','Profiles')],['generate',w('Предложения','Proposals')]]:[['profiles',w('Каталог','Catalog')],['discover',w('Найти / импортировать','Discover / import')]]).map(([id,name])=><button key={id} data-resource-section={id} aria-pressed={workspace===id} onClick={()=>setWorkspace(id)}>{name}</button>)}</div>'''
 s=s.replace(head,nav,1)
 s=s.replace("{kind==='agent'&&<AgentDashboard", "<div hidden={workspace!=='dashboard'}>{kind==='agent'&&<AgentDashboard",1)
 s=s.replace("onAgent={id=>{setSelected(id);setPane('profile');}}/>","onAgent={id=>{setSelected(id);setPane('profile');setWorkspace('agent');}}/>",1)
 s=s.replace("setWorkspace('agent');}}/>}\n", "setWorkspace('agent');}}/>}</div><div hidden={workspace!=='agent'}>{kind==='agent'&&(selected?<AgentDashboard api={api} projectId={projectId} locale={locale} agentId={selected} names={Object.fromEntries((catalog?.assets??[]).map(a=>[a.id,a.name]))}/>:<p>{w('Выберите агента в общем dashboard или профилях','Select an agent in Dashboard or Profiles')}</p>)}</div>\n <div hidden={workspace!=='profiles'}>",1)
 s=s.replace('<div className="m2-fields"><label>{label(locale,\'query\')}', '<div className="resource-toolbar"><label>{label(locale,\'query\')}',1)
 # New/manual buttons and proposals keep existing commands, change only local navigation.
 s=s.replace("onClick={()=>{previewSequence.current++;setSelected('');", "onClick={()=>{setWorkspace('profiles');previewSequence.current++;setSelected('');",1)
 s=s.replace("  {runDetail&&", "  </div>{runDetail&&",1)
 s=s.replace("{kind==='agent'&&<section className=\"panel\" data-testid=\"agent-generator\">", "{kind==='agent'&&<section hidden={workspace!=='generate'} className=\"panel\" data-testid=\"agent-generator\">",1)
 s=s.replace("const proposal=generation.proposal as Proposal;", "setWorkspace('profiles');const proposal=generation.proposal as Proposal;",1)
 s=s.replace("{kind==='skill'&&<section className=\"panel\" data-testid=\"skill-discovery\">", "{kind==='skill'&&<section hidden={workspace!=='discover'} className=\"panel\" data-testid=\"skill-discovery\">",1)
 s=s.replace("setSelected(c.id);setPane('profile');", "setWorkspace('profiles');setSelected(c.id);setPane('profile');",1)
 s=s.replace("setSelected('');const next={proposal:importPreview", "setWorkspace('profiles');setSelected('');const next={proposal:importPreview",1)
 # Per-agent dashboard is a distinct workspace, not a large block ahead of profile metadata.
 s=s.replace("{kind==='agent'&&<AgentDashboard key={asset.id} api={api} projectId={projectId} locale={locale} agentId={asset.id} names={{[asset.id]:asset.name}}/>}","",1)
 return s
edit('apps/web/src/features/team/TeamManager.tsx',team)

def graph(s):
 s=s.replace('<h2>{w(\'Карта исходников\',\'Source map\')}</h2>', '<div className="section-tabs resource-workspace-tabs">{([\'graph\',\'mermaid\',\'list\'] as const).map(id=><button key={id} data-graph-view={id} aria-pressed={layout===id} onClick={()=>setLayout(id)}>{id===\'graph\'?w(\'Граф\',\'Graph\'):id===\'mermaid\'?\'Mermaid\':w(\'Список с клавиатуры\',\'Keyboard list\')}</button>)}</div>',1)
 a=s.index('   <div className="tabs"><button aria-pressed={layout');b=s.index('   <label className="graph-module">',a);s=s[:a]+s[b:]
 s=s.replace('<ul className="records" data-testid="graph-node-list">','<ul hidden={layout!==\'list\'} className="records" data-testid="graph-node-list">',1)
 s=s.replace("Полный доступный список ниже.","Полный доступный список — во вкладке «Список». ").replace("The complete loaded list is below.","The complete loaded list is in the List tab.")
 return s
edit('apps/web/src/features/graph/GraphExplorer.tsx',graph)

def artifacts(s):
 s=s.replace('<section className="m2-manager" data-testid="artifact-explorer"><h2>{title}</h2>', '<section className="m2-manager" data-mode={mode} data-testid="artifact-explorer"><p className="quiet artifact-intro">{title}</p>',1)
 s=s.replace('<span>{item.preview}</span>', '<span className="artifact-excerpt">{item.preview}</span>',1)
 s=s.replace('<small>{item.source.path??item.source.origin} · {item.source.version}</small>', '<small className="artifact-source-path" title={item.source.version}>{item.source.path??item.source.origin}</small>',1)
 # Hash remains in the reader; the catalogue uses the source path instead of a 64-byte hash column.
 return s
edit('apps/web/src/features/artifacts/ArtifactExplorer.tsx',artifacts)

def workflow(s):
 s=s.replace("const [section,setSection]=useState('definition');", "const [section,setSection]=useState('definition'),[definitionTab,setDefinitionTab]=useState('states');",1)
 marker='   <form data-testid="workflow-editor"'
 s=s.replace(marker,'''   <div className="section-tabs workflow-definition-tabs">{[['states',w('Состояния','States')],['transitions',w('Переходы','Transitions')],['diagram',w('Схема','Diagram')],['recipes',w('Recipes','Recipes')]].map(([id,name])=><button type="button" key={id} data-definition-tab={id} aria-pressed={definitionTab===id} onClick={()=>setDefinitionTab(id)}>{name}</button>)}</div>
   <form data-definition-view={definitionTab} data-testid="workflow-editor"''',1)
 s=s.replace("    <h4>{w('Состояния','States')}</h4>", "    <div hidden={definitionTab!=='states'}><h4>{w('Состояния','States')}</h4>",1)
 s=s.replace("    <h4>{w('Переходы','Transitions')}</h4>", "    </div><div hidden={definitionTab!=='transitions'}><h4>{w('Переходы','Transitions')}</h4>",1)
 s=s.replace("    <details><summary>{w('Схема переходов','Transition map')}", "    </div><details open hidden={definitionTab!=='diagram'}><summary>{w('Схема переходов','Transition map')}",1)
 s=s.replace("    <details><summary>{w('Определения recipes", "    <details open hidden={definitionTab!=='recipes'}><summary>{w('Определения recipes",1)
 return s
edit('apps/web/src/features/workflows/WorkflowManager.tsx',workflow)

def autonomy(s):
 s=s.replace(" const commands=draft.allowedActions.includes('command');", " const [pane,setPane]=useState('policy');\n const commands=draft.allowedActions.includes('command');",1)
 s=s.replace('<section className="panel" data-testid="autonomy-manager"><h2>{w(\'Автономная работа\',\'Autonomous work\')}</h2>', '<section className="autonomy-workspace" data-testid="autonomy-manager"><div className="section-tabs resource-workspace-tabs">{[[\'policy\',w(\'Политика\',\'Policy\')],[\'preview\',w(\'Предпросмотр\',\'Preview\')],[\'runs\',w(\'Запуски\',\'Runs\')]].map(([id,name])=><button key={id} data-autonomy-pane={id} aria-pressed={pane===id} onClick={()=>setPane(id)}>{name}</button>)}</div>',1)
 s=s.replace("if(alive.current)setPreview(value);", "if(alive.current){setPreview(value);setPane('preview');}",1)
 s=s.replace("   <form onSubmit=", "   <div className=\"autonomy-policy-grid\" hidden={pane!=='policy'}><form className=\"panel\" onSubmit=",1)
 s=s.replace("   </ul></aside>","   </ul></aside></div>",1)
 s=s.replace('{preview&&<section data-testid="autonomy-preview">','{pane===\'preview\'&&!preview&&<p className="panel">{w(\'Заполните политику и выполните предпросмотр.\',\'Complete the policy and request a preview.\')}</p>}{preview&&<section hidden={pane!==\'preview\'} className="panel" data-testid="autonomy-preview">',1)
 s=s.replace("   <h3>{w('Учтённые запуски'", "   <section hidden={pane!=='runs'} className=\"panel\"><h3>{w('Учтённые запуски'",1)
 s=s.replace("  </>}\n </section>","  </section></>}\n </section>",1)
 return s
edit('apps/web/src/features/autonomy/AutonomyManager.tsx',autonomy)
