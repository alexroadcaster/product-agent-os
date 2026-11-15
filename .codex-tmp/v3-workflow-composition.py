from pathlib import Path
p=Path('apps/web/src/features/workflows/WorkflowManager.tsx');s=p.read_text(encoding='utf-8')
s=s.replace('locale,onOpenSession}:{api:M1Api;','locale,onOpenSession,surface=\'processes\'}:{surface?:string;api:M1Api;',1)
s=s.replace("useState('definition'),[definitionTab,setDefinitionTab]=useState('states');", "useState('catalog'),[definitionTab,setDefinitionTab]=useState('states');\n const [stateIndex,setStateIndex]=useState(0),[transitionIndex,setTransitionIndex]=useState(0);\n useEffect(()=>{if(surface!=='processes')setSection(surface);else setSection('catalog');},[surface]);",1)
s=s.replace("const visible=(id:string)=>section===id||section==='all';", "const visible=(id:string)=>section===id||(id==='definition'&&['states','transitions','diagram','recipes'].includes(section));",1)
start=s.index(' const sections=');end=s.index(';',start)+1
s=s[:start]+" const sections=[['catalog','Каталог','Catalog'],['assignments','Назначения','Assignments'],['states','Состояния','States'],['transitions','Переходы','Transitions'],['diagram','Схема','Diagram'],['recipes','Recipes','Recipes'],['publication','Публикация','Publication'],['migration','Миграция','Migration'],['versions','Версии','Versions']];"+s[end:]
s=s.replace('<section className="panel m2-manager workflow-workbench"','<section className="m2-manager workflow-workbench"',1)
s=s.replace('<div className="workflow-navigation"','<div hidden={surface!==\'processes\'} className="workflow-navigation"',1)
s=s.replace('onClick={()=>setSection(id)}','onClick={()=>{setSection(id);if([\'states\',\'transitions\',\'diagram\',\'recipes\'].includes(id))setDefinitionTab(id);}}',1)
s=s.replace('<div hidden={!visible(\'definition\')} className="workflow-definition">','<div className="workflow-definition">',1)
s=s.replace('<div className="m2-fields"><label>{w(\'Процесс\'', '<div hidden={!visible(\'catalog\')} className="panel workflow-catalog"><div className="m2-fields"><label>{w(\'Процесс\'',1)
s=s.replace('<details><summary>{w(\'Назначения процессов\',\'Workflow assignments\')}</summary>', '</div><section hidden={!visible(\'assignments\')} className="panel workflow-assignments"><h3>{w(\'Назначения процессов\',\'Workflow assignments\')}</h3>',1)
start=s.index('   </details>\n   <div className="section-tabs workflow-definition-tabs">');end=s.index('   <form data-definition-view=',start)
s=s[:start]+'   </section>\n'+s[end:]
s=s.replace('<form data-definition-view=', '<form hidden={!visible(\'definition\')} data-definition-view=',1)
s=s.replace("setDefinitionTab(field.name.startsWith('workflow-transition-')?'transitions':'states');", "const next=field.name.startsWith('workflow-transition-')?'transitions':'states';setSection(next);setDefinitionTab(next);const index=Number(field.name.split('-').at(-1));if(Number.isInteger(index)){if(next==='states')setStateIndex(index);else setTransitionIndex(index);}",1)
start=s.index('    <button type="button" className="workflow-expand-rows"');end=s.index('\n',start);s=s[:start]+s[end:]
s=s.replace('<label>{label(locale,\'name\')}<input name="workflow-name"', '<details className="workflow-properties"><summary>{w(\'Свойства процесса\',\'Workflow properties\')}</summary><label>{label(locale,\'name\')}<input name="workflow-name"',1)
s=s.replace("onChange={e=>patch({name:e.target.value})}/></label>","onChange={e=>patch({name:e.target.value})}/></label></details>",1)
for kind,index_var,collection,item in [('state','stateIndex','states','state'),('transition','transitionIndex','transitions','tr')]:
 start=s.index(f'<div className="workflow-{kind}-list">');mapstart=s.index(f'{{draft.{collection}.map',start);fieldstart=s.index('<fieldset>',mapstart);fieldend=s.index('</fieldset></details>)}</div>',fieldstart)
 fields=s[fieldstart:fieldend+len('</fieldset>')]
 title=f"{item}.name||{item}.id||w('Новая запись','New item')"
 setter='setStateIndex' if kind=='state' else 'setTransitionIndex'
 row=f"<div className=\"workflow-master-detail\"><div className=\"workflow-selection-list\">{{draft.{collection}.map(({item},index)=><button type=\"button\" key={{index}} aria-pressed={{{index_var}===index}} onClick={{()=>{setter}(index)}}><strong>{{{title}}}</strong><small>{{{item}.id}}</small></button>)}}</div><div>{{draft.{collection}.map(({item},index)=><div key={{index}} hidden={{{index_var}!==index}}>{fields}</div>)}}</div></div>"
 s=s[:start]+row+s[fieldend+len('</fieldset></details>)}</div>'):]
 # New rows select their own editor; selecting an index is presentation state only.
 marker=f'data-testid="workflow-add-{kind}" onClick={{()=>patch('
 s=s.replace(marker,f'data-testid="workflow-add-{kind}" onClick={{()=>{{{setter}(draft.{collection}.length);patch(',1)
 start=s.index(f'data-testid="workflow-add-{kind}"');end=s.index('</button>',start);chunk=s[start:end];chunk=chunk.replace('})}>','});}}>');s=s[:start]+chunk+s[end:]
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/ui/App.tsx');s=p.read_text(encoding='utf-8')
s=s.replace('processes={projectId?<WorkflowManager','processes={surface=>projectId?<WorkflowManager surface={surface}',1)
s=s.replace('processes: ReactNode;', 'processes: (surface:string)=>ReactNode;',1)
s=s.replace('["processes","Процессы","Processes"],["all","Все разделы","All sections"]','["processes","Процессы","Processes"],["execution","Выполнение цепочек","Recipe execution"],["queue","Очередь","Queue"],["all","Все разделы","All sections"]',1)
s=s.replace("hidden={!visible('processes')} aria-labelledby=\"settings-tab-processes\">{processes??", "hidden={!visible('processes')&&!['execution','queue'].includes(settingsSection)} aria-labelledby=\"settings-tab-processes\">{processes(['execution','queue'].includes(settingsSection)?settingsSection:'processes')??",1)
p.write_text(s,encoding='utf-8')
