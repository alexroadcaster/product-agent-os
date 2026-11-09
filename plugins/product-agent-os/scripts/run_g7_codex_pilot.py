"""Bounded, explicitly invoked Codex generation pilot; never executes candidate code.

This is an observational CLI pilot, not an attestation of tools=[] or hidden-context
isolation. Any observed tool activity makes that chain ineligible for comparison.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path

from codex_runtime_runner.g7_quality_eval import evidence_fingerprint, render_generation_context


def collect_events(output: str) -> dict:
    """Keep final code and usage only; even an incomplete tool attempt invalidates a pair."""
    messages, kinds, usage, diagnostics = [], [], None, []
    for line in output.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            kinds.append('malformed_event')
            continue
        if not isinstance(event, dict) or not isinstance(event.get('item', {}), dict):
            kinds.append('malformed_event')
            continue
        item = event.get('item', {})
        if event.get('type') in ('item.started', 'item.completed'):
            kind = item.get('type', 'unknown')
            if kind == 'error' and str(item.get('message', '')).startswith('Codex is ignoring 6 unrecognized configuration settings.'):
                kind = 'config_warning'
            kinds.append(kind)
            if kind in ('error', 'config_warning'):
                message = str(item.get('message', ''))
                message = re.sub(r'(?i)(?:[A-Z]:[\\/][^\s]+|sk-[\w-]+)', '[redacted]', message)
                diagnostics.append(message[:400])
            if kind == 'agent_message' and event.get('type') == 'item.completed':
                messages.append(item.get('text', ''))
        if event.get('type') == 'turn.completed':
            usage = event.get('usage')
        if event.get('type') in ('error', 'turn.failed'):
            kinds.append('runtime_error')
    if not isinstance(usage, dict) or any(type(usage.get(k)) is not int for k in ('input_tokens', 'output_tokens')):
        kinds.append('missing_turn_completion')
    return {'candidate': messages[-1] if messages else '', 'event_kinds': kinds, 'diagnostics': diagnostics,
            'usage': usage, 'tool_activity': any(k not in ('agent_message', 'reasoning', 'config_warning') for k in kinds)}


def run(root: Path, executable: str) -> dict:
    """Freeze prompts before calls, stop on setup/tool failure, and retain every attempt."""
    design_path = root / 'docs/superpowers/specs/paos-aud-g7-code-quality-eval-design.json'
    design = json.loads(design_path.read_text(encoding='utf-8'))
    pilot = design['codex_observational_pilot']
    if hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != pilot['runner_sha256']:
        raise ValueError('pilot runner drift')
    manifest = json.loads((root / design['manifest_path']).read_text(encoding='utf-8'))
    destination = root / '.docs-tools/reports/g7-codex-pilot'
    destination.mkdir(exist_ok=True)
    if (destination / 'receipt.json').exists():
        old = (destination / 'receipt.json').read_bytes()
        archive = destination / ('attempt-' + hashlib.sha256(old).hexdigest()[:16] + '.json')
        if not archive.exists():
            archive.write_bytes(old)
    receipt = {'design_digest': evidence_fingerprint(design), 'kind': 'observational_codex_cli',
               'strict_AB_eligible': False, 'owner_acceptance': None, 'calls': [],
               'limits': pilot['limits'], 'candidate_execution': 'not_performed'}
    command = [executable, 'exec', '--ephemeral', '--json', '--sandbox', 'read-only',
               '--model', pilot['model'], '-c', 'model_reasoning_effort="medium"',
               '-c', 'features.shell_tool=false', '-c', 'agents.enabled=false',
               '-c', 'features.apps=false', '-c', 'web_search="disabled"',
               '-c', 'allow_browser_and_computer_use=false', '-']
    receipt['command'] = ['codex', *command[1:]]
    def save():
        (destination / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    stop = False
    for chain in manifest['future_generation_chains']:
        for arm in ('baseline', 'treatment'):
            previous = None
            for index, step in enumerate(chain['steps']):
                packet = render_generation_context(root, arm, chain['id'], index, previous)
                record = {'arm': arm, 'chain': chain['id'], 'step': step['id'], 'prompt_digest': packet['prompt_digest']}
                started = time.monotonic()
                try:
                    completed = subprocess.run(command, input=packet['prompt'], cwd=root,
                        capture_output=True, text=True, encoding='utf-8', timeout=180)
                    parsed = collect_events(completed.stdout)
                    record.update({k:v for k,v in parsed.items() if k != 'candidate'})
                    record['exit_code'] = completed.returncode
                    record['stderr_digest'] = hashlib.sha256(completed.stderr.encode()).hexdigest()
                    record['permission_denied'] = 'Access is denied' in completed.stderr or 'Permission denied' in completed.stderr
                    record['configuration_error'] = 'configuration' in completed.stderr.lower() and completed.returncode != 0
                    if parsed['candidate']:
                        filename = f"{chain['id']}-{arm}-{index}.txt"
                        (destination / filename).write_text(parsed['candidate'], encoding='utf-8')
                        record['candidate_file'] = filename
                    if completed.returncode or parsed['tool_activity'] or not parsed['candidate']:
                        record['status'] = 'setup_error' if completed.returncode else 'ineligible'
                        # Persist only a bounded diagnostic, never raw ambient context or tool output.
                        record['diagnostic'] = 'Codex failed or produced tool activity/no final candidate; no correctness claim'
                        stop = True
                    else:
                        previous = parsed['candidate']
                        filename = f"{chain['id']}-{arm}-{index}.txt"
                        (destination / filename).write_text(previous, encoding='utf-8')
                        record.update(status='generated_unverified', candidate_file=filename,
                                      candidate_digest=hashlib.sha256(previous.encode()).hexdigest())
                except subprocess.TimeoutExpired:
                    record['status'] = 'timeout'
                    stop = True
                record['elapsed_seconds'] = round(time.monotonic()-started, 3)
                receipt['calls'].append(record)
                save()
                print(chain['id'], arm, step['id'], record['status'], flush=True)
                if stop:
                    return receipt
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-executable', required=True)
    args = parser.parse_args()
    result = run(Path(__file__).resolve().parents[3], args.codex_executable)
    raise SystemExit(0 if len(result['calls']) == 12 and all(c['status']=='generated_unverified' for c in result['calls']) else 1)
