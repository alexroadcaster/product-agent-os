from pathlib import Path
import json

base = Path('docs/planning/user-project-methodologies-2026-11-15')
canonical = base.with_suffix('.json')
payload = json.loads(canonical.read_bytes())
criterion = next(a for t in payload['tasks'] for a in t['acceptance_criteria'] if a['id'] == 'PAOS-PMETH-23-AC02')
revised = {
    'ru': 'Для заявленного Design пути проверены journey и states. Для заявленного FSD пути отдельно проверены migration proposal, выбранный incremental pilot и сохранение достаточно модульной архитектуры. Если заявлен target apply, проверены staged diff PMETH-16, compatibility, rollback и сохранность user files. Backend/CLI обходятся без FSD gates, AI quality остаётся eval/gap без скрытого provider call.',
    'en': 'Verify journeys and states when Design is claimed. For claimed FSD coverage separately verify the migration proposal, selected incremental pilot and retention of sufficiently modular architecture. For claimed target apply verify PMETH-16 staged diff, compatibility, rollback and user-file preservation. Omit FSD gates for backend/CLI and keep AI quality as eval/gap without hidden provider calls.',
}
for suffix, lang in (('.md', 'ru'), ('.en.md', 'en')):
    f = base.with_suffix(suffix)
    raw = f.read_bytes()
    old = criterion[lang].encode()
    assert raw.count(old) == 1
    out = raw.replace(old, revised[lang].encode(), 1)
    if lang == 'ru':
        out = out.replace('31 активных рёбер'.encode(), '31 активное ребро'.encode(), 1)
    f.write_bytes(out)
criterion.update(revised)
out = (json.dumps(payload, indent=2, ensure_ascii=False) + '\n').encode()
canonical.write_bytes(out)
base.with_suffix('.en.json').write_bytes(out)
