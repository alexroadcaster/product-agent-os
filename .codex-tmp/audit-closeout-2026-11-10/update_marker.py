import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

path = Path('.codex/product-agent-os/lifecycle-state.5c99647c868a7c5b35ccbe63d4101f8f26dfb07945c39ecb8bffd02a727f0273.json')
data = json.loads(path.read_text(encoding='utf-8-sig'))
assert data['session_id'] == '01a1bf93-9bba-7df0-b087-c43aaaf1f139'
assert data['task_id'] == 'PAOS-AUD-GAP06-ACCEPTANCE-TOOLING-FIX'
data['plan_path'] = 'research/product-agent-os-audit-closeout-tooling-2026-11-10.md'
data['brief_digest'] = 'sha256:' + hashlib.sha256(data['scope'].encode('utf-8')).hexdigest()
data['brief_digest_provenance'] = 'SHA256 of the current authorized maintenance scope'
data['updated_at'] = datetime.now(timezone.utc).isoformat()
if sys.argv[1:] == ['--complete']:
    receipts = Path('.codex-tmp/audit-closeout-2026-11-10')
    assert 'OK (skipped=1)' in (receipts/'full-final.log').read_text(encoding='utf-8')
    assert all(item['ok'] for item in json.loads((receipts/'fixtures-final.json').read_text(encoding='utf-8-sig')))
    saved = json.loads((receipts/'checked-source-hashes.json').read_text(encoding='utf-8'))
    assert all(hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest for name, digest in saved.items())
    data['status'] = 'ready_for_completion_ledger'
    data['completion_ready'] = True
    data['closure_level'] = 'implemented_locally_verified'
    data['owner_decision'] = 'All three GAP-06 local pilots accepted; T34 and fresh-session activation remain separate'
    data['residual_gaps'] = ['T34 no_go / preflight blocked', 'HOST-01/HOST-02 fresh-session activation separate', 'System TEMP permission boundary unchanged; workspace TEMP used']
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
