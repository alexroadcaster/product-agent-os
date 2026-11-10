"""Explicit local compaction CLI; never schedules or automatically applies a plan."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from product_agent_os.control_plane_compaction import apply, propose, rollback


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('propose', 'apply', 'rollback'))
    parser.add_argument('workspace', type=Path)
    parser.add_argument('input', help='Moves/proposal JSON path, or workspace-relative recovery journal')
    parser.add_argument('--output', type=Path, help='Explicit private output destination for a proposal')
    parser.add_argument('--approve', help='Exact reviewed proposal digest; required for apply/rollback')
    parser.add_argument('--limit', type=int, default=40000)
    args = parser.parse_args()
    try:
        if args.action == 'propose':
            if args.output is None or args.output.exists():
                raise ValueError('new explicit private --output required; existing files are preserved')
            moves = json.loads(Path(args.input).read_text(encoding='utf-8'))
            result = propose(args.workspace, moves, hard_limit=args.limit)
            with args.output.open('x', encoding='utf-8', newline='\n') as output:
                output.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
            print(json.dumps({'status': 'proposal_only', 'digest': result['digest'],
                              'files': len(result['files']), 'review_required': True}))
        elif args.action == 'apply':
            plan = json.loads(Path(args.input).read_text(encoding='utf-8'))
            print(json.dumps(apply(args.workspace, plan, approved_digest=args.approve)))
        else:
            # Recovery authority is not implied by having access to a journal.
            if not args.approve or args.input != '.codex/product-agent-os/compaction/' + args.approve.removeprefix('sha256:') + '.json':
                raise ValueError('exact journal digest approval required')
            print(json.dumps(rollback(args.workspace, args.input)))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # Do not print source documents, recovery bytes or secrets on failures.
        print(json.dumps({'status': 'blocked', 'error_type': type(exc).__name__}))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
