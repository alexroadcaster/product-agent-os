from pathlib import Path
from datetime import datetime, timezone
import json, shutil, hashlib, html, sys

root = Path('design/2026-11-13-v3')
receipt = Path(sys.argv[1])
report = json.loads((receipt/'result.json').read_text(encoding='utf-8'))
assert report['status'] == 'passed' and len(report['stateViews']) == 170
routes = [r for r in json.loads((root/'coverage.json').read_text(encoding='utf-8-sig'))['routes'] if r['id'] not in ['component-lab','motion-lab']]
out = root/'implementation-captures'
out.mkdir(exist_ok=True)
rows = []
for r in routes:
    row = dict(id=r['id'], title=r.get('title',r['id']), themes={})
    for theme in ['light','dark']:
        name = f"parity-{theme}-{r['id']}.png"
        shutil.copy2(receipt/name, out/name)
        row['themes'][theme] = dict(capture=f'implementation-captures/{name}', reference=f"screenshots/{theme}-{r['id']}.png", sha256=hashlib.sha256((out/name).read_bytes()).hexdigest(), review='visually_compared', audit=next(v['audit'] for v in report['stateViews'] if v['id']==r['id'] and v['theme']==theme))
    rows.append(row)
manifest = dict(reviewedAt=datetime.now(timezone.utc).isoformat(), context_mode='self_review', receipt=receipt.as_posix()+'/result.json', method='Pairwise visual review: reference and implementation, both themes; full-page captures plus lower sections of long forms. No pixel-identical claim.', productStates=85, themeCaptures=170, userAcceptance='pending', sourceHashes=report['sourceHashes'], visualMockSources=report.get('visualMockSources'), rows=rows)
(root/'implementation-visual-review.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
options=''.join(f'<option value="{html.escape(r["id"])}">{i+1:02d} · {html.escape(str(r.get("title",r["id"])))}</option>' for i,r in enumerate(routes))
gallery='''<!doctype html>
<html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>V3 — прототип и реализация</title><style>
*{box-sizing:border-box}body{margin:0;background:#10151e;color:#e7edf7;font:14px/1.5 system-ui}header{position:sticky;top:0;z-index:2;background:#19212e;padding:16px 24px;border-bottom:1px solid #46536a}h1{font-size:20px;margin:0 0 8px}p{max-width:1300px;margin:8px 0;color:#c1cbdc}nav{display:flex;gap:12px;align-items:center;flex-wrap:wrap}button,select{font:inherit;background:#26344b;color:#fff;border:1px solid #6b7d99;border-radius:6px;padding:8px 12px}button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid #9cbeff;outline-offset:3px}main{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:20px}figure{margin:0;min-width:0}figcaption{font-weight:600;padding:12px;background:#202b3d}img{display:block;width:100%;height:auto}a{color:#a9c6ff}.note{margin:16px 24px}label{display:flex;align-items:center;gap:8px}
</style><header><h1>V3 — прототип рядом с реализацией</h1><p>85 продуктовых экранов × 2 темы. Снимки локальной сборки на одноразовом синтетическом профиле. Это сравнение изображений; анимации проверяются в приложении.</p><nav><button id="prev" aria-label="Предыдущий экран">←</button><label>Экран <select id="screen">OPTIONS</select></label><button id="next" aria-label="Следующий экран">→</button><label>Тема <select id="theme"><option value="light">Светлая · Porcelain</option><option value="dark">Тёмная · Obsidian</option></select></label><a href="implementation-evidence.md">Проверки и ограничения</a></nav></header>
<p class="note" id="note"></p><main><figure><figcaption>Утверждённый V3</figcaption><a id="reference-link" target="_blank"><img id="reference" alt="Экран утверждённого V3"></a></figure><figure><figcaption>Работающая реализация</figcaption><a id="actual-link" target="_blank"><img id="actual" alt="Экран локальной реализации"></a></figure></main>
<script>
const screen=document.querySelector('#screen'),theme=document.querySelector('#theme');const query=new URLSearchParams(location.search);screen.value=query.get('screen')||'tasks-list';theme.value=query.get('theme')||'light';
function show(){const id=screen.value,t=theme.value;for(const [kind,path] of [['reference',`screenshots/${t}-${id}.png`],['actual',`implementation-captures/parity-${t}-${id}.png`]]){document.getElementById(kind).src=path;document.getElementById(kind+'-link').href=path;}document.getElementById('note').textContent=(/dashboard|analytics|usage|overview/.test(id)?'Числа и заполненность отличаются: приложение показывает существующие данные; отсутствующие tokens, стоимость и tool_use не заменяются демонстрационными значениями.':/graph|workflow-diagram/.test(id)?'Узлы и связи берутся из реальных fixtures: геометрия отличается от демонстрационного графа. Для больших схем доступны масштаб и локальная прокрутка.':/session|recipe|skills|skill-/.test(id)?'Доступность runtime и наличие записей влияют на состояние. Generated skill и recipe recovery в визуальном прогоне используют явно отмеченные fixtures без вызова провайдера.':'Сравнивайте расположение областей, полей и действий. Названия, количество записей и состояния отражают существующие API и отличаются от демонстрации.');history.replaceState(null,'','?screen='+id+'&theme='+t);}
screen.onchange=theme.onchange=show;document.querySelector('#prev').onclick=()=>{screen.selectedIndex=(screen.selectedIndex+screen.options.length-1)%screen.options.length;show()};document.querySelector('#next').onclick=()=>{screen.selectedIndex=(screen.selectedIndex+1)%screen.options.length;show()};show();
</script></html>'''.replace('OPTIONS',options)
(root/'implementation-gallery.html').write_text(gallery,encoding='utf-8')
print(json.dumps(dict(routes=len(routes),captures=len(rows)*2,gallery=str(root/'implementation-gallery.html'))))
