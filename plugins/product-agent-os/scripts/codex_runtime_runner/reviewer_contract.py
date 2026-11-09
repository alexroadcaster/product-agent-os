"""Independent reviewer gateway; live calls and owner approval are external."""
import hashlib
import json
import re
import secrets
from copy import deepcopy

from .promotion_contract import QuarantinedPrimaryResult, parse_primary_result

DIMENSIONS = ('correctness', 'minimality', 'readability', 'test_strength', 'maintainability', 'security_privacy', 'performance')


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def packet_digest(packet):
    return digest(json.dumps(packet, sort_keys=True, separators=(',', ':')))


def prepare_review(baseline, treatment, *, patches, evidence, material_change_required=True, task_context=''):
    """Build a blinded packet only from revalidated results and patch-bound checks.

    The caller owns trusted check execution. Receipts are not cryptographically
    authenticated. The returned private mapping must never be sent to a reviewer.
    Free-text arm leaks fail closed instead of silently rewriting code under review.
    """
    parsed = [parse_primary_result(p, material_change_required) for p in (baseline, treatment)]
    if any(isinstance(p, QuarantinedPrimaryResult) for p in parsed):
        raise ReviewerContractError('pair:invalid_primary_result')
    for field in ('task_id', 'corpus_id', 'corpus_version', 'schema_version', 'model_id', 'model_reasoning_effort'):
        if baseline[field] != treatment[field]:
            raise ReviewerContractError('pair:identity_mismatch')
    if baseline['arm'] != 'baseline' or treatment['arm'] != 'treatment':
        raise ReviewerContractError('pair:arm_mismatch')
    _blinded_text(task_context)
    mapping, candidates = {}, []
    for arm in ('baseline', 'treatment'):
        patch = patches.get(arm) if isinstance(patches, dict) else None
        _blinded_text(patch)
        receipt = evidence.get(arm) if isinstance(evidence, dict) else None
        if not isinstance(receipt, dict) or receipt.get('task_id') != baseline['task_id'] or receipt.get('patch_sha256') != digest(patch):
            raise ReviewerContractError('pair:missing_or_stale_evidence')
        checks = ('acceptance', 'regression', 'seeded_faults', 'dependency')
        if any(receipt.get(key) != 'passed' for key in checks):
            raise ReviewerContractError('pair:deterministic_gate_failed')
        candidate_id = secrets.token_hex(12)
        mapping[candidate_id] = arm
        candidates.append({'candidate_id': candidate_id, 'patch': patch,
                           'patch_sha256': digest(patch), 'checks': {key: 'passed' for key in checks}})
    secrets.SystemRandom().shuffle(candidates)
    return {'schema_version': 'blinded_review_v1', 'review_id': secrets.token_hex(16),
            'task_context': task_context, 'candidates': candidates}, mapping


def validate_review(packet, verdict):
    """Validate a response bound to this packet; critical findings outrank scores."""
    if not isinstance(verdict, dict) or set(verdict) != {'review_id', 'packet_sha256', 'candidates'}:
        raise ReviewerContractError('review:invalid_fields')
    if verdict['review_id'] != packet['review_id'] or verdict['packet_sha256'] != packet_digest(packet):
        raise ReviewerContractError('review:stale_packet')
    rows = verdict['candidates']
    if not isinstance(rows, list) or len(rows) != 2:
        raise ReviewerContractError('review:missing_candidates')
    expected = {item['candidate_id'] for item in packet['candidates']}
    seen, blockers = set(), []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'candidate_id', 'scores', 'findings'}:
            raise ReviewerContractError('review:invalid_candidate')
        candidate_id = row['candidate_id']
        if not isinstance(candidate_id, str) or candidate_id not in expected or candidate_id in seen:
            raise ReviewerContractError('review:unknown_or_duplicate_candidate')
        seen.add(candidate_id)
        scores = row['scores']
        if not isinstance(scores, dict) or set(scores) != set(DIMENSIONS):
            raise ReviewerContractError('review:missing_dimensions')
        if any(type(score) is not int or not 0 <= score <= 10 for score in scores.values()):
            raise ReviewerContractError('review:invalid_scores')
        if min(scores.values()) < 6:
            blockers.append(candidate_id + ':dimension_below_threshold')
        if not isinstance(row['findings'], list):
            raise ReviewerContractError('review:invalid_findings')
        for finding in row['findings']:
            if not isinstance(finding, dict) or set(finding) != {'severity', 'category', 'evidence'}:
                raise ReviewerContractError('review:invalid_finding')
            if finding['severity'] not in ('critical', 'high', 'medium', 'low') or finding['category'] not in (*DIMENSIONS, 'security', 'data_loss', 'regression'):
                raise ReviewerContractError('review:invalid_finding_class')
            if not isinstance(finding['evidence'], str) or not finding['evidence'].strip():
                raise ReviewerContractError('review:finding_without_evidence')
            if finding['severity'] in ('critical', 'high'):
                blockers.append(candidate_id + ':' + finding['category'])
    return {'status': 'passed', 'verdict': 'changes_requested' if blockers else 'approve',
            'blockers': blockers, 'candidates': deepcopy(rows), 'independence': 'requires_separate_execution_receipt'}


def _blinded_text(value):
    if not isinstance(value, str) or len(value.encode('utf-8')) > 256 * 1024:
        raise ReviewerContractError('review_input:invalid_text')
    if re.search(r'(?i)\b(baseline|treatment|behavior_score|dimension_scores|target_verdict)\b', value):
        raise ReviewerContractError('review_input:arm_or_score_leak')


class ReviewerContractError(ValueError):
    pass
