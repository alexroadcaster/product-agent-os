from pathlib import Path
p=Path('apps/web/src/ui/App.tsx');s=p.read_text(encoding='utf-8')
composer=s.index('              className="composer"')
a=s.index('              <label>\n                {t("mode")}',composer);b=s.index('              {messages.hasMore && <p role="status">',a)
controls=s[a:b];s=s[:a]+'              {sessionRunFields}\n'+s[b:]
connect=s.index('{t("connect")}',composer);a=s.rfind('                <button',composer,connect);b=s.index('              </div>\n              <p role="status">{notice',a)
actions=s[a:b];s=s[:a]+'                {sessionRunActions}\n'+s[b:]
before=s.rfind('  return (',0,s.index('      <section className="chat-panel">'))
s=s[:before]+'  const sessionRunFields=<div className="session-run-fields">'+controls+'</div>;\n  const sessionRunActions=<>'+actions+'</>;\n'+s[before:]
s=s.replace('<div hidden={pane!==\'run\'}>\n        <RuntimeSummary', '<div hidden={pane!==\'run\'}><h2>{locale===\'ru\'?\'Запуск и профиль\':\'Run and profile\'}</h2>{pane===\'run\'&&sessionRunFields}<div className="actions">{pane===\'run\'&&sessionRunActions}</div>\n        <RuntimeSummary')
p.write_text(s,encoding='utf-8')
p=Path('apps/web/src/design/parity.css');p.write_text(p.read_text(encoding='utf-8')+'\n.session-run-fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-bottom:20px}.session-run-fields>p,.session-run-fields>.m2-check{grid-column:1/-1}.session-run-fields label{align-content:start}.session-run-fields>button{justify-self:start}.session-runtime-detail>.actions{margin-bottom:20px}\n',encoding='utf-8')
