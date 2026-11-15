from pathlib import Path
p=Path('apps/web/src/features/artifacts/ArtifactExplorer.tsx');s=p.read_text(encoding='utf-8')
s="import {Icon} from '../../ui/Icon.tsx';\n"+s
s=s.replace(" const sequence=useRef(0)"," const [pane,setPane]=useState('list');\n const sequence=useRef(0)")
s=s.replace('setSelected(item);}',"setSelected(item);setPane('reader');}")
s=s.replace('data-mode={mode} data-testid="artifact-explorer"><p', '''data-mode={mode} data-artifact-pane={pane} data-testid="artifact-explorer"><div className="section-tabs artifact-tabs">{[['list',mode==='checks'?w('Все проверки','All checks'):w('Каталог','Catalog')],['reader',mode==='checks'?w('Результат и приёмка','Result and acceptance'):w('Документ','Document')],...(mode==='documents'?[['proposal',w('Предложение','Proposal')]]:[])].map(([id,name])=><button key={id} data-artifact-pane={id} aria-pressed={pane===id} disabled={id!=='list'&&!selected} onClick={()=>setPane(id)}>{name}</button>)}</div><h1>{pane==='proposal'?w('Предложение изменения','Change proposal'):pane==='reader'&&selected?selected.title:mode==='documents'?w('Документы','Documents'):mode==='checks'?w('Проверки','Checks'):w('Поиск по проекту','Project search')}</h1><p''')
s=s.replace('<form data-testid="artifact-filters"','<form hidden={mode!==\'all\'&&pane!==\'list\'} data-testid="artifact-filters"')
s=s.replace('{page&&<p>{page.items.length}',"{page&&<p hidden={mode!=='all'&&pane!=='list'}>{page.items.length}")
s=s.replace('<section className="panel" style={{minWidth:0}}><ul className="records" data-testid="artifact-list">', '<section hidden={mode!==\'all\'&&pane!==\'list\'} className="panel artifact-catalog" style={{minWidth:0}}><ul className="records" data-testid="artifact-list">')
s=s.replace('<strong>{item.title}</strong><small>', '<Icon name={item.kind===\'check\'||item.kind===\'acceptance\'?\'checks\':\'documents\'}/><strong>{item.title}</strong><small>')
s=s.replace('<aside className="panel" data-testid="artifact-reader"', '<aside hidden={mode!==\'all\'&&pane===\'list\'} className="panel" data-testid="artifact-reader"')
s=s.replace('<h3>{document.item.title}</h3><p>', '<div className="artifact-document-grid" hidden={pane===\'proposal\'}><aside className="artifact-origin"><h3>{w(\'Источник\',\'Source\')}</h3><p>')
s=s.replace('{links(document.item)}\n', '{links(document.item)}</aside><div className="artifact-content"><h3>{document.item.title}</h3>\n')
s=s.replace("setDraft(next);drafts.set(draftKey,next);setPreview(undefined);}}>{w('Предложить изменение'", "setDraft(next);drafts.set(draftKey,next);setPreview(undefined);setPane('proposal');}}>{w('Предложить изменение'")
s=s.replace('    {draft&&<form data-testid="document-proposal-editor"', '    </div></div><div hidden={pane!==\'proposal\'}>{draft&&<form data-testid="document-proposal-editor"')
s=s.replace("   </>:<p>{w('Выберите документ", "   </div></>:<p>{w('Выберите документ")
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/features/skills/SkillGenerator.tsx');s=p.read_text(encoding='utf-8')
s=s.replace(' const sequence=useRef(0)', " const [pane,setPane]=useState('requirements');\n const sequence=useRef(0)")
s=s.replace('data-testid="skill-generator"><h2>', '''data-testid="skill-generator" data-generator-pane={pane}><div className="segmented generator-steps">{[['requirements',w('1. Основание','1. Grounding')],['draft',w('2. Черновик','2. Draft')],['diff','3. Diff + Apply']].map(([id,name])=><button type="button" key={id} data-generator-step={id} aria-pressed={pane===id} disabled={id==='draft'&&!draft||id==='diff'&&!preview} onClick={()=>setPane(id)}>{name}</button>)}</div><h2>''')
s=s.replace('  <details><summary>', '  <details hidden={pane!==\'requirements\'}><summary>',1)
s=s.replace('  <form onSubmit=', '  <form hidden={pane!==\'requirements\'} onSubmit=',1)
s=s.replace('<section data-testid="skill-generation-result">', '<section hidden={pane!==\'requirements\'} data-testid="skill-generation-result">')
s=s.replace('setDraft(structuredClone(generation.proposal));',"setDraft(structuredClone(generation.proposal));setPane('draft');")
s=s.replace('<form data-testid="skill-generation-editor"','<form hidden={pane!==\'draft\'} data-testid="skill-generation-editor"')
s=s.replace('setPreview(value);setAck(false);',"setPreview(value);setAck(false);setPane('diff');")
s=s.replace('<section data-testid="skill-generation-preview">','<section hidden={pane!==\'diff\'} data-testid="skill-generation-preview">')
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/features/team/TeamManager.tsx');s=p.read_text(encoding='utf-8')
s=s.replace('</div>{kind===\'skill\'&&', '''</div><div className="section-heading resource-heading"><h1>{kind==='agent'?w('Агенты проекта','Project agents'):workspace==='requirements'?w('Генератор скиллов','Skill generator'):w('Скиллы проекта','Project skills')}</h1><button className="primary" onClick={()=>setWorkspace(kind==='agent'?'generate':'requirements')}>{kind==='agent'?w('Предложить агента','Propose agent'):w('Рекомендовать скилл','Recommend skill')}</button></div>{kind==='skill'&&''',1)
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/design/parity.css');s=p.read_text(encoding='utf-8')+'''
/* Atlas review: profile content on the left, source catalog on the right. */
[data-testid=agent-manager] .m2-task-layout,[data-testid=skill-manager] .m2-task-layout{grid-template-columns:minmax(0,1fr) 280px}
[data-testid=agent-manager] .m2-task-layout>aside,[data-testid=skill-manager] .m2-task-layout>aside{grid-column:2;grid-row:1;background:none;border:0;padding:0}
[data-testid=agent-manager] .m2-task-layout>section,[data-testid=skill-manager] .m2-task-layout>section{grid-column:1;grid-row:1}
.resource-heading{margin:24px 0}.resource-heading h1{margin:0}
[data-testid=asset-profile] .task-metadata{display:grid;grid-template-columns:160px minmax(0,1fr);gap:12px;font-size:12px}
[data-testid=asset-profile] .task-metadata dd{margin:0;overflow-wrap:anywhere}
[data-testid=asset-editor] fieldset>p{grid-column:1/-1}[data-testid=asset-editor] [name=asset-content]{min-height:260px}
[data-testid=artifact-explorer]>.artifact-intro{margin-bottom:20px}[data-testid=artifact-explorer]>h1{margin:24px 0 8px}
[data-testid=artifact-explorer]:not([data-mode=all]) .m2-task-layout{grid-template-columns:minmax(0,1fr)}
[data-testid=artifact-explorer][data-mode=all] .m2-task-layout{grid-template-columns:minmax(0,1fr) 320px}
[data-testid=artifact-list] button{display:grid!important;grid-template-columns:24px minmax(0,1fr) 160px!important;align-items:start;gap:6px 12px;padding:18px 8px}
[data-testid=artifact-list] button>.duo-icon{grid-column:1;grid-row:1/4}[data-testid=artifact-list] button>strong{grid-column:2;overflow-wrap:anywhere}
[data-testid=artifact-list] button>small{grid-column:2;font-size:11px}[data-testid=artifact-list] button>small:first-of-type{grid-column:3;grid-row:1/3;text-align:right}
[data-testid=artifact-list] button>span:not(.duo-icon){grid-column:2/-1}.artifact-source-path{white-space:normal}
.artifact-document-grid{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:28px}.artifact-content{grid-row:1;grid-column:1;min-width:0}.artifact-origin{grid-row:1;grid-column:2;border-left:1px solid var(--line);padding-left:24px;font-size:12px;overflow-wrap:anywhere}
[data-testid=artifact-explorer][data-mode=all] .artifact-document-grid{display:block}.artifact-content h3{margin:0 0 24px}.artifact-origin .mono{font-size:10px}
[data-testid=document-proposal-editor] textarea{min-height:240px}.artifact-catalog{padding:0!important;border:0!important;background:none!important}
.generator-steps{margin-bottom:28px}.generator-steps button{font-size:12px}[data-testid=skill-generator]{padding:24px!important}[data-testid=skill-generation-editor] fieldset{display:grid;grid-template-columns:1fr 1fr;gap:20px}[data-testid=skill-generation-editor] label:has([name=generated-skill-content]),[data-testid=skill-generation-editor] label:has([name=generated-skill-reason]){grid-column:1/-1}[data-testid=skill-generation-editor] [name=generated-skill-content]{min-height:320px;font-family:var(--font-mono)}[data-testid=skill-generation-editor] button{grid-column:1/-1;justify-self:end}
''';p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/ui/App.tsx');s=p.read_text(encoding='utf-8').replace("['tasks','overview','portfolio'].includes(section)","['tasks','overview','portfolio','agents','skills','documents','checks','search'].includes(section)");p.write_text(s,encoding='utf-8')
