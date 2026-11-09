"""Compile frozen, synthetic evaluation inputs without starting a model or tool."""
import hashlib
import json
from pathlib import Path


class EvalDesignError(ValueError):
    """Frozen inputs changed or the requested arm/task is outside the design."""


def render_eval_prompt(root: Path, arm: str, task_id: str) -> dict:
    """Verify hashes before reading generation inputs; oracle files stay excluded."""
    root = root.resolve()
    design = json.loads((root/'docs/superpowers/specs/batch45-code-quality-eval-design.json').read_text())
    if arm not in ('baseline', 'treatment'):
        raise EvalDesignError('arm:unknown')
    row = design['arms'][arm]
    for relative, expected in {**design['context_sha256'], row['prompt_path']: row['prompt_sha256']}.items():
        path = _path(root, relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise EvalDesignError('freeze:source_drift')
    corpus = json.loads(_path(root, design['corpus_path']).read_text())
    digest = hashlib.sha256(json.dumps(corpus['tasks'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    if digest != corpus['content_sha256'] or digest != row['corpus_sha256']:
        raise EvalDesignError('freeze:corpus_drift')
    matches = [task for task in corpus['tasks'] if task['task_id'] == task_id]
    if len(matches) != 1:
        raise EvalDesignError('task:unknown')
    task = matches[0]
    folder = _path(root, task['path'])
    # Check evaluator assets too, but only task/initial source enters the prompt.
    for name, expected in task['sha256'].items():
        path = _path(root, (folder/name).relative_to(root).as_posix())
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise EvalDesignError('freeze:fixture_drift')
    context = {'intent': task['intent'], 'acceptance': task['acceptance'],
               'input_source': (folder/task['input_file']).read_text(encoding='utf-8')}
    template = _path(root, row['prompt_path']).read_text(encoding='utf-8')
    text = template.replace('{{task_context_json}}', json.dumps(context, ensure_ascii=False, sort_keys=True))
    if '{{' in text or '}}' in text:
        raise EvalDesignError('prompt:unresolved_variable')
    return {'prompt': text, 'prompt_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'task_id': task_id, 'arm': arm, 'model': row['model'], 'reasoning_effort': row['reasoning_effort'],
            'provider_call_performed': False, 'approval_required': True}


def _path(root: Path, relative: str) -> Path:
    path = root/relative
    if Path(relative).is_absolute() or not path.resolve().is_relative_to(root) or path.is_symlink():
        raise EvalDesignError('path:outside_contract')
    return path
